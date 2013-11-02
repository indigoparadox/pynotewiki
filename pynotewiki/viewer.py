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

import gtk
import webkit

class PyNoteWikiViewer:
   
   window = None
   viewer = None
   
   def __init__( self ):
      self.window = gtk.Window()
      self.window.set_title( 'PyNoteWiki Viewer' )
      self.window.connect( 'destroy', gtk.main_quit )

      self.viewer = webkit.WebView()
      self.viewer.load_html_string( 'Welcome to PyNoteWiki!', 'file:///' )
      self.window.add( self.viewer )
      self.window.show_all()

      gtk.main()

