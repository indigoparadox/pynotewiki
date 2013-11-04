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

import logging
from yapsy.PluginManager import PluginManager

class PyNoteWikiParser:

   logger = None
   
   _parser = None

   def __init__( self, wiki_path ):

      self.logger = logging.getLogger( 'pynotewiki.parser' )

      # Load the parser plugins and find one that can open the requested wiki.
      plugins = PluginManager()
      plugins.setPluginPlaces(
         # TODO: Look in home directory, as well.
         ['./parsers','/usr/lib/pynotewiki/parsers']
      )
      plugins.collectPlugins()
      for plugin in plugins.getAllPlugins():
         self.logger.debug( 'Found parser "{}".'.format( plugin.name ) )
         if plugin.plugin_object.sniff_wiki( wiki_path ):
            self.logger.info( 'Parser "{}" can read "{}".'.format(
               plugin.name, wiki_path
            ) )
            self._parser = plugin.plugin_object
            self._parser.load_wiki( wiki_path )
            break

      if None == self._parser:
         raise Exception( 'No valid parser found.' )

   def get_page( self, page_title ):

      page = { 'body': '', 'updated': 0 }
      
      # Fill in the defaults with data from the parser plugin.
      new_page = self._parser.get_page( page_title )
      if None != new_page:
         page.update( new_page )

      return page

   def get_page_html( self, page_title ):

      page = self.get_page( page_title )

      # Load the formatter plugins and find one that can open the requested
      # page.
      plugins = PluginManager()
      plugins.setPluginPlaces(
         # TODO: Look in home directory, as well.
         ['./formatters','/usr/lib/pynotewiki/formatters']
      )
      plugins.collectPlugins()
      for plugin in plugins.getAllPlugins():
         self.logger.debug( 'Found formatter "{}".'.format( plugin.name ) )
         if plugin.plugin_object.sniff_page( page.get( 'body' ) ):
            self.logger.info( 'Formatter "{}" can read "{}".'.format(
               plugin.name, page_title
            ) )
            return plugin.plugin_object.get_html( page.get( 'body' ), self )

