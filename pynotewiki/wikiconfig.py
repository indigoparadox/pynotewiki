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

import os
import yaml

WIKI_CONFIG_PATH = os.path.join( os.path.expanduser( '~' ), '.pynotewiki' )

class PyNoteWikiConfig:

   _instance = None

   config = None

   def __new__( cls, *args, **kwargs ):

      # Preserve a singleton for inter-modular config cache.
      if not cls._instance:
         cls._instance = super( PyNoteWikiConfig, cls ).__new__(
            cls, *args, **kwargs
         )
      return cls._instance

   def __init__( self ):

      # Try to open existing user config store.
      try:
         with open( WIKI_CONFIG_PATH, 'r' ) as config_file:
            self.config = yaml.load( config_file )
      except:
         pass

      # Create a new config store if none exists.
      if None == self.config:
         self.config = {}

   def set_value( self, key, value ):
      self.config[key] = value
      
      # Save the altered config to disk immediately.
      with open( WIKI_CONFIG_PATH, 'w' ) as config_file:
         config_file.write( yaml.dump( self.config ) )


