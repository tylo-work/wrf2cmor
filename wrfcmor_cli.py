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

import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    '-f', '--files', dest='globfiles',
    help='Regular expression to be parsed by python to get the input files to process', metavar='REGEXP'
)
parser.add_argument(
    '--from-file', dest='filelist', default='',
    help='Text file containing the input files. One per row', metavar='FILELIST.txt'
)
parser.add_argument(
    '-v', '--variables', dest='vars',
    help='Variables to extract. Apart from those defined in the file, you can ask for any of the following derived variables: MSLP, U10ER, V10ER, WIND', metavar='VAR1[,VAR2,...]'
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
    '--time-units', dest='time_units', default='days since 1999-01-01_00:00:00',
    help='Units for the time axis', metavar='Days/Hours since YYYY-MM-DD_hh:mm:ss'
)
parser.add_argument(
    '-o', '--output', dest='OFILE', metavar='OUTPUTFILE.nc',
    help='Output file name'
)
parser.add_argument(
    '--output-pattern', dest='OUTPUT_PATTERN', metavar='[varcf]_[varwrf]_[level]_[firsttime]_[lasttime]_experiment.nc',
    help='Output pattern. Patterns recognized are currently of the form "[varcf]_[varwrf]_[firsttime]_[lasttime]_experiment.nc". Firsttime and lasttime are replaced by datetimes of the form YYYYmmddHH'
)

args = parser.parse_args()
