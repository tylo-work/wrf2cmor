# ------------------------------------------------------------------------
# wrfcmor_cli.py
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

import glob
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('FILE', help='source CSV file(s)')
parser.add_argument('-o', '--out', help='destination CSV file')
parser.add_argument('-d', '--out_dir', help='destination directory')
parser.add_argument('-s', '--step_size', help='depth step size', type=float, default=0.5)
parser.add_argument('-z', '--zero_depth', help='set reference DEPTH. Default uses minimum depth', type=float)

files = glob.glob(args.FILE)

parser.add_argument(
    '-f', '--files', dest='globfiles',
    help='Regular expression to be parsed by python to get the input files to process', metavar='REGEXP'
)
parser.add_argument(
    '--from-file', dest='filelist', default='',
    help='Text file containing the input files. One per row', metavar='FILELIST.txt'
)
parser.add_argument(
    '--previous-file', dest='prevfile', default='',
    help='Extra input file to be prepended to the input files ONLY for BACKWARD deaccumulations', metavar='WRFNCFILE.nc'
)
parser.add_argument(
    '--next-file', dest='nextfile', default='',
    help='Extra input file to be prepended to the input files ONLY for FORWARD deaccumulations', metavar='WRFNCFILE.nc'
)
parser.add_argument(
    '-v', '--variables', dest='vars',
    help='Variables to extract. Apart from those defined in the file, you can ask for any of the following derived variables: MSLP, U10ER, V10ER, WIND', metavar='VAR1[,VAR2,...]'
)
parser.add_argument(
    '-d', '--discard-criteria', dest='discard',
    help='Enable discarding files. Currently only the uncommon_size criteria is implemented', metavar='uncommon_size'
)
parser.add_argument(
    '-t', '--variable-table', dest='vtable',
    help='Table for translating WRF names into IPCC standard names', metavar='variable.table'
)
parser.add_argument(
    '-a', '--attributes', dest='attributes',
    help='Table for setting the global attributes of the file', metavar='atributes.file'
)
parser.add_argument(
    '-q', '--quiet', action='store_true', default = False,
    help='Run quietly'
)
parser.add_argument(
    '--single-record', action='store_true', dest='singlerec',
    help='Save only one record. Useful to extract fixed fields (LANDMASK, LANDUSE, ...)'
)
parser.add_argument(
    '-z', action='store_true', default=False, dest='zaxis',
    help='Create Z axis information'
)
parser.add_argument(
    '-s', action='store_true', default=False, dest='saxis',
    help='Create soil layer axis information'
)
parser.add_argument(
    '-p', action='store_true', default=False, dest='paxis',
    help='Create pressure level axis information'
)
parser.add_argument(
    '-m', action='store_true', default=False, dest='maxis',
    help='Create height (meters) level axis information'
)
parser.add_argument(
    '--time-bounds', dest='tbounds', metavar='H1,H2',
    help='Create a time_bnds variable to specify the period of time considered in each time record. H1 is the start time in hours from the current time record and H2 is the ending time'
)
parser.add_argument(
    '-r', '--reference-date', dest='refdate',
    help='Reference date for the files'
)
parser.add_argument(
    '--time-units', dest='time_units', default='hours since 1950-01-01_00:00:00',
    help='Units for the time axis', metavar='Days/Hours since YYYY-MM-DD_hh:mm:ss (T or space as separator also work)'
)
parser.add_argument(
    '-o', '--output', dest='OFILE', metavar='OUTPUTFILE.nc',
    help='Output file name'
)
parser.add_argument(
    '--output-pattern', dest='OUTPUT_PATTERN', metavar='[varcf]_[varwrf]_[level]_[firsttime]_[lasttime]_experiment.nc',
    help='Output pattern to use if the option --split-in-variables is activated. Patterns recognized are currently of the form '[varcf]_[varwrf]_[firsttime]_[lasttime]_experiment.nc. Firsttime and lasttime are replaced by datetimes of the form YYYYmmddHH'
)
parser.add_argument(
    '-g', '--geofile', metavar='geo_em.d0X.nc', dest='geofile',
    help='geo_em file to be used. For instance if you already removed geographic variables from the input files'
)
parser.add_argument(
    '--fullfile', metavar='wrfout_d0X_allvars.nc', dest='fullfile',
    help='wrfout file to be used for variables not found in the data files. For instance if you removed variables as the eta or soil levels.'
)
parser.add_argument(
    '--split-variables', action='store_true', dest='splitvars',
    help='Write a separated file for each variable.'
)
parser.add_argument(
    '--split-levels', action='store_true', dest='splitlevs',
    help='Write a separated file for each variable and level. (Use always with --split-variables)'
)
parser.add_argument(
    '--temp-dir', dest='TEMPDIR',
    help='Temporary directory to write the files while running. They are copied to the folfer specified by -o or --output-pattern when the program finishes.'
)
parser.add_argument(
    '--plevs-filter', dest='selected_plevs',
    help='Comma separated list of the pressure levels that we want to save, in hPa.'
)
parser.add_argument(
    '--slevs-filter', dest='selected_slevs',
    help='Comma separated list of the soil levels that we want to save, in meters. They must be in .2f format.'
)
parser.add_argument(
    '--output-format', dest='oformat', default='NETCDF3_CLASSIC',
    help='Format of the output files. Available possibilities: NETCDF4_CLASSIC, NETCDF3 (default). If using NETCDF4_CLASSIC, the deflate level is 4 by default.'
)
parser.add_argument(
    '--filter-times', dest='ftimes', default=False, metavar='%Yi%mi%di%Hi,%Yf%mf%df%Hf',
    help='Filter the output files so only times between the two selected are retained.'
)

args = parser.parse_args()
