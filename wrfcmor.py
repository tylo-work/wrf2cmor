# ------------------------------------------------------------------------
# wrfcmor.py
# ------------------------------------------------------------------------
# Copyright (c) 2020
#   Tyge Løvset, tylo@norceresearch.no
#
# NORCE Climate 
# https://www.norceresearch.no/en/research-area/klima
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------

import os
import glob
import netCDF4
import wrfcmor_tabs as tabs
import numpy as np
from datetime import datetime
import signal
import sys

current_file = None

def signal_handler(sig, frame):
    print(' - you pressed ctrl-c!')
    if current_file:
        print('  removing file:', current_file)
        os.remove(current_file)
    sys.exit(0)

def bytes2str(arr):
    #return np.ma.MaskedArray.tostring(arr).decode('ascii')
    return arr.tostring().decode('ascii')


def process_values(vname: str, plev_num: int, values, dst):
    if vname == tabs.constants['dst_timevar']:
        values = [datetime.strptime(bytes2str(s), tabs.src_timeformat) for s in values]
        values = netCDF4.date2num(values, units=tabs.constants['dst_reftime'])
    elif vname == 'evspsblpot':
        values[np.isnan(values)] = tabs.constants['missing_value']  # replaces all NaN with missing value
    elif plev_num > 0 and len(values.shape) == 4: # pressure 3d fields
        values = values[:, plev_num - 1, :, :]
        values[values == -999] = tabs.constants['missing_value']
        var_out = dst.createVariable('plev', np.float32)  # scalar, no dimension
        var_out[:] = np.array([tabs.constants['plevels'][plev_num - 1] * 100])
    return values


def process_dimensions(src_var, src, dst):
    dst_dims = []
    for src_dname in src_var.dimensions:
        try:
            dname = tabs.constants['dimensions'][src_dname]
        except KeyError:
            continue
        dst_dims.append(dname)
        if dname not in dst.dimensions:
            dim = src.dimensions[src_dname]
            size = (len(dim) if not dim.isunlimited() else None)
            dst.createDimension(dname, size)
    return tuple(dst_dims)
    
def global_attributes(vname: str, domain_num: int, year: int, plev_num: int):
    return {
        **tabs.constants['global_attr'],
        'startdate': 'S%d01010000' % year,
        'CORDEX_domain': tabs.constants['domains'][domain_num]
    }

def open_rlatrlon(domain_num: int):
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    rlatrlon = '%s/essentials/rlatrlon_%s_nc4classic.nc' % (scriptdir, tabs.constants['domains'][domain_num])
    return netCDF4.Dataset(rlatrlon)
    
    
def add_rlatrlon(src, dst):
    for vname, var_in in src.variables.items():
        for dname in var_in.dimensions:
            if dname not in dst.dimensions:
                dim = src.dimensions[dname]
                dst.createDimension(dname, (len(dim) if not dim.isunlimited() else None))
        values = var_in[:]
        var_out = dst.createVariable(vname, values.dtype, var_in.dimensions,
                                     zlib=(tabs.compress > 0), complevel=tabs.compress)
        var_out[:] = values
        var_out.setncatts({k: var_in.getncattr(k) for k in var_in.ncattrs()})


def get_plevels_range(vname):
    if vname in tabs.constants['pvars3d']:
        return 1, len(tabs.constants['plevels']) + 1
    else:
        return 0, 1


def split_to_monthly_vars(src_root: str, dst_root: str, filetype: str, domain_num: int, 
                         year: int, month: int, included_vars=None, included_plev_nums=None):
    """Split and convert a netCDF Classic (3/4) file to CMOR specs"""
    global current_file
    infiles = os.path.join(src_root, tabs.src_file_pattern(filetype, domain_num, year, month))
    
    with netCDF4.MFDataset(infiles) as src:
        print('CMORize split:', src_root, '-->', dst_root)
        print('inputs:', os.path.basename(infiles))
        time_values = None
        # loop source variables
        for src_vname, src_var in src.variables.items():
            if src_vname not in tabs.varmap:
                continue
            vname = tabs.varmap[src_vname]
            if included_vars and vname not in included_vars:
                continue
            print('', src_vname, src_var.dimensions, end='', flush=True)
            values = None
            # Loop through possible plevels
            start, finish = get_plevels_range(vname)
            if start > 0: print('')
            for plev_num in range(start, finish):
                if plev_num and included_plev_nums and (plev_num not in included_plev_nums):
                    continue
                outfile = os.path.join(dst_root, tabs.dst_file_month(vname, domain_num, year, month, plev_num))
                outfinal = os.path.join(dst_root, tabs.dst_file_year(vname, domain_num, year, plev_num))
                if os.path.isfile(outfile) or os.path.isfile(outfinal):
                    print('skipping existing', outfile)
                    continue
                if values is None:
                    values = src_var[:]
                current_file = outfile
                with netCDF4.Dataset(outfile, 'w', format='NETCDF4_CLASSIC') as dst:
                    # Create missing dimensions required by variable and return destination dimensions
                    dst_dims = process_dimensions(src_var, src, dst)
                    
                    # Filter the main variable values
                    dst_values = process_values(vname, plev_num, values, dst)
                    
                    vname_full = tabs.full_vname(vname, plev_num)
                    print(' -->', vname_full, tabs.constants['domains'][domain_num], year, month, dst_dims, dst_values.dtype, end='', flush=True)
                    # Add the main variable
                    var_out = dst.createVariable(vname_full, dst_values.dtype, dst_dims, fill_value=tabs.constants['missing_value'],
                                                 zlib=(tabs.compress > 0), complevel=tabs.compress)
                    var_out[:] = dst_values

                    # Add time variable
                    if time_values is None:
                        time_values = process_values(tabs.constants['dst_timevar'], 0, src.variables[tabs.src_time_var][:], None)
                    var_out = dst.createVariable(tabs.constants['dst_timevar'], time_values.dtype, (tabs.constants['dst_timedim'],),
                                                 zlib=(tabs.compress > 0), complevel=tabs.compress)
                    var_out[:] = time_values
                    print('')
                current_file = None


def merge_monthly_to_oneyear_vars(src_root: str, dst_root: str, domain_num: int, year: int, included_vars=None, included_plev_nums=None):
    """Merge year"""
    global current_file
    print('CMORize merge:', src_root, '-->', dst_root)
    for vname in tabs.constants['variable_attr']:
        if included_vars and vname not in included_vars:
            continue
        # Loop through possible plevels
        start, finish = get_plevels_range(vname)
        for plev_num in range(start, finish):
            if plev_num and included_plev_nums and (plev_num not in included_plev_nums):
                continue
            outfile = os.path.join(dst_root, tabs.dst_file_year(vname, domain_num, year, plev_num))
            if os.path.isfile(outfile):
                print('skipping existing', outfile)
                continue
            infiles_pattern = os.path.join(src_root, tabs.dst_file_month_pattern(vname, domain_num, year, plev_num))
            infiles = glob.glob(infiles_pattern)
            if infiles == []:
                #print('skipping non-existing', infiles_pattern)
                continue
            print('output:', os.path.basename(outfile))
            current_file = outfile
            with netCDF4.MFDataset(infiles) as src,\
                 open_rlatrlon(domain_num) as cor,\
                 netCDF4.Dataset(outfile, 'w', format='NETCDF4_CLASSIC') as dst:
                # Add dimensions
                for dname, dim in src.dimensions.items():
                    dst.createDimension(dname, (len(dim) if not dim.isunlimited() else None))
                # Add global attrs and rlatrlon coords. 
                dst.setncatts(global_attributes(vname, domain_num, year, plev_num))
                add_rlatrlon(cor, dst)
                # Add variables
                for vname_full, var_in in src.variables.items():
                    print(' var:', vname_full, end='...', flush=True)
                    values = var_in[:]
                    var_out = dst.createVariable(vname_full, values.dtype, var_in.dimensions,
                                                 zlib=(tabs.compress > 0), complevel=tabs.compress)
                    print(' write', end='...', flush=True)
                    var_out[:] = values
                    vn = tabs.pvars3d[vname_full] if vname_full in tabs.pvars3d else vname_full
                    var_out.setncatts(tabs.constants['variable_attr'][vn])
                    print('')
            current_file = None
            for f in infiles:
                os.remove(f)


def cmorize(inroot, outroot, ftype, domain_num, year, vars=None, plevs=None):
    for month in range(1, 12+1):
        split_to_monthly_vars(inroot, outroot, ftype, domain_num, year, month, included_vars=vars, included_plev_nums=plevs)
    merge_monthly_to_oneyear_vars(outroot, outroot, domain_num, year, included_vars=vars, included_plev_nums=plevs)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    #signal.pause()

    inroot = '/nird/projects/NS9001K/tyge/RAW/2014'
    outroot = '/nird/projects/NS9001K/tyge/wrf_cmor/2014'

    #split_to_monthly_vars(inroot, outroot, 'wrfpress', 1, 2014, 1, included_vars=['tas', 'zg']) # , 'pr', 'wsgsmax', 'uas', 'vas', 'ua100m', 'va100m'])
    #split_to_monthly_vars(inroot, outroot, 'wrfcdx', 1, 2014, 1, included_vars=['ts', 'ps'])

    #vars = ['evspsblpot'] # , 'ts']
    #vars = ['ts', 'ps']
    #ftype = 'wrfcdx'
    
    vars = None # ['hus', 'ua']
    plevs = None # [1, 2, 3]
    
    cmorize(inroot, outroot, 'wrfpress', 1, 2014)
