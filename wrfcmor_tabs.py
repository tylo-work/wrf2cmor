# ------------------------------------------------------------------------
# wrfcmor_tabs.py
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

import yaml
import wrfcmor_cli as cli

def full_vname(var, plev_num):
    return var + str(constants['plevels'][plev_num - 1]) if plev_num > 0 else var


def src_file_pattern(filetype, domain_num, year, month): # wrfpress, wrfcdx, wrfxtrm
    return '%s_d%02d_%d-%02d-??_00?00?00' % (filetype, domain_num, year, month)


def dst_file_month(var, domain_num, year, month, plev_num=0):
    return '%s_%s_%s_1hr_%d-%02d.nc' % (full_vname(var, plev_num), constants['domains'][domain_num], 
                                                                   constants['mainstring'], year, month)

    
def dst_file_month_pattern(var, domain_num, year, plev_num=0):
    return dst_file_month(var, domain_num, year, 9999, plev_num).replace('9999', '??', 1)
   

def dst_file_year(var, domain_num, year, plev_num=0):
    return '%s_%s_%s_1hr_%d%s-%d%s.nc' % (full_vname(var, plev_num), constants['domains'][domain_num],
                                                                     constants['mainstring'],
                                                                     year, constants['from_date'],
                                                                     year, constants['to_date'])

with open(cli.args.constfile) as yaml_file:
    constants = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Remap back 3d vars to basename
pvars3d = {'%s%s' % (v, p): v for v in constants['pvars3d'] for p in constants['plevels']}

# Flatten the file_vars-map to varmap only
varmap = {k: v for m, d in constants['file_vars'].items() for k, v in d.items()}

compress = constants['compress']
