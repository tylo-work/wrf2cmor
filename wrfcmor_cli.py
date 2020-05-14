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
print('wrf2cmor - convert wrf climate model output data to CMORized format')
print('ex input: /nird/projects/NS9001K/tyge/RAW/2014')
print('ex output: /nird/projects/NS9001K/tyge/wrf_cmor/2014')
print('')

parser.add_argument(
    '-i', '--indir', required=True,
    help='Input file directory'
)
parser.add_argument(
    '-o', '--outdir', required=True,
    help='Output file directory'
)
parser.add_argument(
    '-c', '--constfile', default='constants.yml',
    help='Yaml text file containing all input settings',
)

parser.add_argument(
    '-y', '--year', required=True,
    help='Year to be cmorized'
)
parser.add_argument(
    '-b', '--filebase',
    help='Input file base names. Default all. Single or comma separated list without space, e.g: wrfxtrm,wrfcdx'
)
parser.add_argument(
    '-d', '--domain',
    help='Input domains numbers to use. Default all. Single or comma separated list without space'
)
parser.add_argument(
    '-v', '--variables',
    help='Variable to extract. Default all. Single or comma separated list without space.'
)
parser.add_argument(
    '-q', '--quiet', action='store_true', default = False,
    help='Run quietly'
)

args = parser.parse_args()
