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

import markdown
from yapsy.IPlugin import IPlugin

class MarkdownFormatter( IPlugin ):

   name = "Markdown Text Formatter"

   def sniff_page( self, page ):
      # TODO: Use a more thorough test.
      if 'hg' == page.get( 'parser' ):
         return True
      return False

   def get_html( self, page_contents, parser ):
      return markdown.markdown( page_contents )

