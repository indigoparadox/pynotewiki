#!/usr/bin/env python

'''
This file is part of PyNoteWiki.

PyNoteWiki is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

PyNoteWiki is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more 
details.

You should have received a copy of the GNU General Public License along
with PyNoteWiki.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
from distutils.core import setup

# Parse CLI arguments.

with_hg = True 
filtered_args = [] 
for arg in sys.argv: 
   if arg == "--without-hg": 
      with_hg = False
   else: 
      filtered_args.append( arg ) 
sys.argv = filtered_args

# Assemble the parsers and pixmaps.

# TODO: Compile the parsers into *.pycs.

data_files = [
   ('/usr/share/pixmaps',['pynotewiki.png']),
   ('/usr/lib/pynotewiki/parsers',['parsers/nbk.py']),
   ('/usr/lib/pynotewiki/parsers',['parsers/nbk.yapsy-plugin']),
]

if with_hg:
   data_files.append( ('/usr/lib/pynotewiki/parsers',['parsers/hg.py']) )
   data_files.append(
      ('/usr/lib/pynotewiki/parsers',['parsers/hg.yapsy-plugin'])
   )
   data_files.append(
      ('/usr/lib/pynotewiki/formatters',['formatters/markdown.py'])
   )
   data_files.append(
      ('/usr/lib/pynotewiki/formatters',['formatters/markdown.yapsy-plugin'])
   )

# TODO: Make an XDG desktop definition.

setup(
   name='pynotewiki',
   # TODO: Figure out a way to grab the repo revision or something.
   version='0.1',
   packages=['pynotewiki'],
   scripts=['pnw.py'],
   data_files=data_files,
)

