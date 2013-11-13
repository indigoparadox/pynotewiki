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

import os
from mercurial import ui, hg
from yapsy.IPlugin import IPlugin

class HGParser( IPlugin ):
	
   name = 'Mercurial Wiki Parser'

   _wiki_path = None
   _wiki_repo = None

   def sniff_wiki( self, wiki_path ):
      wiki_dir_path = os.path.dirname( wiki_path )
      try:
         # Try to open the containing directory as an hg repo.
         wiki_repo = hg.repository( ui.ui(), wiki_dir_path )
         self._wiki_path = wiki_dir_path
         self._wiki_repo = wiki_repo
         return True
      except:
         return False
   
   def load_wiki( self, wiki_path ):
      pass
   
   def get_page( self, page_title ):

      # Try to open the markdown file in the repo root.
      page_path = os.path.join( self._wiki_path, '{}.md'.format( page_title ) )
      page = {}
      with open( page_path, 'r' ) as page_file:
         page_contents = page_file.read()
         page.update( { 'body': page_contents } )

      page.update( {
         'parser': 'hg',
         # TODO: Implement updated time.
         'updated': str( 0 ),
      } )

      return page
