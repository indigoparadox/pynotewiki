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

WIKI_CONFIG_PATH = os.path.join( os.path.expanduser( '~' ), '.pynotewiki.yaml' )

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

   def get_value( self, key ):

      ''' Return the requested config item from the store if present, or None
      if not. '''

      try:
         return self.config[key]
      except:
         return None

   def set_value( self, key, value ):

      ''' Set the given item in the config store and save it to disk. '''

      # Don't do anything if it's already set.
      try:
         if config[key] == value:
            pass
      except:
         pass

      self.config[key] = value
      
      # Save the altered config to disk immediately.
      with open( WIKI_CONFIG_PATH, 'w' ) as config_file:
         config_file.write( yaml.dump(
            self.config, default_flow_style=False, indent=3
         ) )

