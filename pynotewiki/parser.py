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
import logging

class PyNoteWikiParser:

   contents = None
   logger = None

   def __init__( self, wiki_file ):

      self.logger = logging.getLogger( 'pynotewiki.parser' )

      self.contents = wiki_file.read()

   def get_page( self, page_title ):

      page = { 'body': '', 'updated': 0 }

      # Break out the requested page.
      page_match = re.search(
         '^#--------------------------------------------------\n' + \
         '# {}\n\n^page {{?{}}}? ([{{]?)(.+?)([}}]?) ([0-9]+?)\n\n\n'.format(
            re.escape( page_title ), re.escape( page_title )
         ),
         self.contents,
         re.MULTILINE | re.DOTALL
      )

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

         page.update( { 'updated': page_match.groups()[3] } )

      return page

   def get_page_html( self, page_title ):

      ''' Return the contents of the requested page formatted in HTML. '''

      page_contents = self.get_page( page_title ).get( 'body' )

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
         self.format_link,
         page_contents
      )

      # Newline -> <br />
      page_contents = re.sub( r'\n', r'<br />', page_contents )

      # #pre -> <pre>
      page_contents = page_contents.replace( '#pre', '<pre>' )
      page_contents = page_contents.replace( '#unpre', '</pre>' )

      return page_contents

   def format_link( self, page_name ):
      
      # Get the page name as a string.
      try:
         page_name = page_name.group( 1 )
      except:
         # Must've been a string to start.
         pass

      link_classes = []
      
      # See if the page name exists.
      if '' == self.get_page( page_name ):
         link_classes.append( 'missing' )

      return r'<a class="' + ' '.join( link_classes ) + r'" href="wiki:///' + \
         urllib.quote_plus( page_name  ) + r'">' + page_name + r'</a>'
   
