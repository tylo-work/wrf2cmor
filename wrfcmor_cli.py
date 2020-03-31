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
    '-i', '--indir',
    help='Input file directory'
)
parser.add_argument(
    '-o', '--outdir',
    help='Output file directory'
)
parser.add_argument(
    '-c', '--constfile', default='constants.yml',
    help='Yaml text file containing all input settings',
)
parser.add_argument(
    '-y', '--year',
    help='Year to be cmorized'
)
parser.add_argument(
    '-f', '--filebase',
    help='Input file base names. Default all. Use multiple -f for more names.'
)
parser.add_argument(
    '-d', '--domain',
    help='Input domains numbers to use. Default all. Use multiple -d for more domains.'
)
parser.add_argument(
    '-v', '--variables', dest='vars',
    help='Variable to extract. Default all. Use comma separated list without space for multiple vars.'
)
parser.add_argument(
    '-q', '--quiet', action='store_true', default = False,
    help='Run quietly'
)

args = parser.parse_args()
