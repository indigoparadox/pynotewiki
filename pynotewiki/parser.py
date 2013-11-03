#!/usr/bin/env python

'''
This file is part of PyNoteWiki.

PyNoteWiki is free software: you can redistribute it and/or modify it under 
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

PyNoteWiki is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more 
details.

You should have received a copy of the GNU Lesser General Public License along
with PyNoteWiki.  If not, see <http://www.gnu.org/licenses/>.
'''

import re

class PyNoteWikiParser:

   contents = None

   def __init__( self, wiki_file ):
      self.contents = wiki_file.read()

   def get_page( self, page_title ):

      # Break out the requested page.
      page_match = re.search(
         '^#--------------------------------------------------\n# {}\n\n^page .?{}.? (.+?) [0-9]+?\n\n\n'.format(
            page_title, page_title
         ),
         self.contents,
         re.MULTILINE | re.DOTALL
      )

      return page_match.groups()[0]

   def get_page_html( self, page_title ):

      ''' Return the contents of the requested page formatted in HTML. '''

      page_contents = self.get_page( page_title )

      # TODO: Parse wiki markup to HTML.

      return page_contents
   
