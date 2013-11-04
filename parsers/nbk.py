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
from yapsy.IPlugin import IPlugin

class NBKParser( IPlugin ):

   name = 'Notebook Wiki Parser'
   contents = None

   def sniff_wiki( self, wiki_path ):
      with open( wiki_path, 'r' ) as wiki_file:
         print wiki_path
         # TODO: Make sure this is a valid notebook file.
         return True

   def load_wiki( self, wiki_path ):
      with open( wiki_path, 'r' ) as wiki_file:
         self.contents = wiki_file.read()

   def get_page( self, page_title ):
      # Break out the requested page.
      page_match = re.search(
         '^#--------------------------------------------------\n' + \
         '# {}\n\n^page {{?{}}}? ([{{]?)(.+?)([}}]?) ([0-9]+?)\n\n\n'.format(
            re.escape( page_title ), re.escape( page_title )
         ),
         self.contents,
         re.MULTILINE | re.DOTALL
      )

      page = {}

      if None != page_match:
         page.update( { 'body': page_match.groups()[1] } )
         if '{' != page_match.groups()[0]:
            # No curly brace present, so do extra parsing to remove escaped
            # whitespace.
            page_body = page.get( 'body' )
            page_body = page.get( 'body' ).decode( 'string_escape' )
            page_body = page.get( 'body' ).replace( '\\ ', ' ' )
            page_body = page.get( 'body' ).replace( '\\{', '{' )
            page_body = page.get( 'body' ).replace( '\\}', '}' )
            page.update( { 'body': page_body } )

         page.update( {
            'parser': 'nbk',
            'updated': page_match.groups()[3],
         } )

      return page

