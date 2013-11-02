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
from parser import PyNoteWikiParser

class PyNoteWikiViewer:
   
   window = None
   viewer = None
   
   def __init__( self ):

      # Create the main window.
      self.window = gtk.Window()
      self.window.set_title( 'PyNoteWiki Viewer' )
      self.window.connect( 'destroy', gtk.main_quit )

      # Add a file menu.
      mb = gtk.MenuBar()

      filemenu = gtk.Menu()
      filem = gtk.MenuItem( 'File' )
      filem.set_submenu( filemenu )
      
      openm = gtk.MenuItem( 'Open Notebook' )
      openm.connect( 'activate', self.dialog_open )
      filemenu.append( openm )
      
      exitm = gtk.MenuItem( 'Exit' )
      exitm.connect( 'activate', gtk.main_quit )
      filemenu.append( exitm )

      mb.append( filem )

      # Add the HTML viewer.
      self.viewer = webkit.WebView()
      self.viewer.load_html_string( 'Welcome to PyNoteWiki!', 'file:///' )

      # Pack the widgets and show the window.
      vbox = gtk.VBox( False, 2 )
      vbox.pack_start( mb, False, False, 0 )
      vbox.pack_start( self.viewer, True, True, 0 )
      self.window.add( vbox )
      self.window.show_all()

      gtk.main()

   def dialog_open( self, widget ):
      print 'Not implemented.'

