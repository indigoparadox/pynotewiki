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
import wikiconfig
import os
import logging
from parser import PyNoteWikiParser
from wikiconfig import PyNoteWikiConfig

class PyNoteWikiViewer:
   
   window = None
   viewer = None
   wiki = None
   logger = None
   pageuri = None
   
   def __init__( self ):

      self.logger = logging.getLogger( 'pynotewiki.viewer' )

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
      openm.connect( 'activate', self.on_open )
      filemenu.append( openm )
      
      exitm = gtk.MenuItem( 'Exit' )
      exitm.connect( 'activate', gtk.main_quit )
      filemenu.append( exitm )

      mb.append( filem )

      # Add the HTML viewer.
      self.viewer = webkit.WebView()
      self.viewer.connect(
         'navigation-policy-decision-requested', self.on_navigate_decision
      )
      self.display_html( 'Welcome to PyNoteWiki!' )

      # Pack the widgets and show the window.
      vbox = gtk.VBox( False, 2 )
      vbox.pack_start( mb, False, False, 0 )
      vbox.pack_start( self.viewer, True, True, 0 )
      self.window.add( vbox )
      # TODO: Try to find pynotewiki.png on the system.
      self.window.set_icon_from_file( 'pynotewiki.png' )
      self.window.show_all()

      gtk.main()

   def display_html( self, string_in, return_html=False ):
      
      # TODO: Wrap the string in HTML headers with user-definable CSS from the
      #       config.

      if return_html:
         return string_in
      else:
         self.viewer.load_html_string( string_in, 'wiki:///' )

   def on_open( self, widget ):

      config = PyNoteWikiConfig()

      # Display a file open dialog.
      dialog =  gtk.FileChooserDialog(
         'Open Notebook...',
         None,
         gtk.FILE_CHOOSER_ACTION_OPEN,
         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK)
      )
      dialog.set_default_response( gtk.RESPONSE_OK )
      if None != config.get_value( 'LastDir' ):
         dialog.set_current_folder( config.get_value( 'LastDir' ) )

      nbkfilter = gtk.FileFilter()
      nbkfilter.set_name( 'Notebook Files' )
      nbkfilter.add_pattern( '*.nbk' )
      dialog.add_filter( nbkfilter )

      response = dialog.run()
      if gtk.RESPONSE_OK == response:
         # Store the last used path for later.
         config.set_value( 'LastDir', os.path.dirname( dialog.get_filename() ) )

         # TODO: Rule out bugs before silencing them.
         # Open the notebook file.
         #try:
         with open( dialog.get_filename(), 'r' ) as wiki_file:
            self.wiki = PyNoteWikiParser( wiki_file )
            self.display_html( self.wiki.get_page_html( 'Home' ) )
         #except:
         #   self.logger.error(
         #      'Unable to open notebook {}.'.format( dialog.get_filename() )
         #   )

      dialog.destroy()

   def on_navigate_decision( self, view, frame, req, act, poldec ):
      uri = req.get_uri()

      # Don't infinitely loop.
      if uri == self.pageuri:
         poldec.use()
         return True

      # Allow only wiki pages.
      # TODO: Determine valid wiki pages present in the wiki from invalid ones.
      if not uri.startswith( 'wiki:' ):
         return False

      self.pageuri = uri
      frame.load_string(
         self.display_html(
            self.wiki.get_page_html( uri.split( '/' )[3] ), True
         ),
         'text/html',
         'iso-8859-15',
         uri
      )
      poldec.ignore()
      return True

