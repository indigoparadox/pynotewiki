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
import urllib
from yapsy.IPlugin import IPlugin

class NotebookFormatter( IPlugin ):

   name = "Notebook Text Formatter"
   
   _parser = None

   def sniff_page( self, page ):
      if 'nbk' == page.get( 'parser' ):
         return True
      return False

   def get_html( self, page_contents, parser ):

      ''' Return the contents of the requested page formatted in HTML. '''

      self._parser = parser

      # TODO: Parse wiki markup to HTML.

      # = * = -> <h*>
      page_contents = re.sub(
         r'^([=]+)(.+?)([=]+)',
         lambda m: '<h' + str( len( m.group( 1 ) ) ) + '>' + m.group( 2 ) + \
            '</h' + str( len( m.group( 1 ) ) ) + '>',
         page_contents,
         flags=re.MULTILINE
      )

      # [] -> <a>
      page_contents = re.sub(
         r'[^\\]\[(.+?[^\\])\]',
         self._format_link,
         page_contents
      )

      # Newline -> <br />
      page_contents = re.sub( r'\n', r'<br />', page_contents )

      # #pre -> <pre>
      page_contents = page_contents.replace( '#pre', '<pre>' )
      page_contents = page_contents.replace( '#unpre', '</pre>' )

      return page_contents

   def _format_link( self, target_title ):
      
      # Get the page name as a string.
      try:
         target_title = target_title.group( 1 )
      except:
         # Must've been a string to start.
         pass

      link_classes = []
      
      # See if the page name exists.
      if '' == self._parser.get_page( target_title ).get( 'body' ):
         link_classes.append( 'missing' )

      return r'<a class="' + ' '.join( link_classes ) + r'" href="wiki:///' + \
         urllib.quote_plus( target_title  ) + r'">' + target_title + r'</a>'

