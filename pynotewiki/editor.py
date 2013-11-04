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
import logging
import urllib
import urlparse
from parser import PyNoteWikiParser

class PyNoteWikiEditor:

   window = None
   editor = None
   wiki = None
   wiki_path = None
   logger = None
   page_uri = None

   def __init__( self, wiki_path, page_uri ):

      self.logger = logging.getLogger( 'pynotewiki.editor' )

      # Create the main window.
      self.window = gtk.Window()
      self.window.set_title( 'PyNoteWiki Editor' )
      self.window.connect( 'destroy', gtk.main_quit )

      mb = gtk.MenuBar()

      # Create the file menu.
      filemenu = gtk.Menu()
      filem = gtk.MenuItem( 'File' )
      filem.set_submenu( filemenu )
      
      exitm = gtk.MenuItem( 'Exit' )
      exitm.connect( 'activate', gtk.main_quit )
      filemenu.append( exitm )

      mb.append( filem )

      # Create the toolbar.
      toolbar = gtk.Toolbar()

      saveb = gtk.ToolButton( gtk.STOCK_SAVE )
      saveb.connect( 'clicked', self.on_save )
      cancelb = gtk.ToolButton( gtk.STOCK_NO )
      cancelb.connect( 'clicked', self.on_view )

      toolbar.insert( saveb, 0 )
      toolbar.insert( cancelb, 1 )

      # Create the editor.
      self.editor = gtk.TextView()
      self.editor.set_editable( True )
      editor_scroller = gtk.ScrolledWindow()
      editor_scroller.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
      editor_scroller.add( self.editor )

      # Pack the widgets and show the window.
      vbox = gtk.VBox( False, 2 )
      vbox.pack_start( mb, False, False, 0 )
      vbox.pack_start( toolbar, False, False, 0 )
      vbox.pack_start( editor_scroller, True, True, 0 )
      #vbox.pack_start( self.statusbar, False, False, 0 )
      self.window.add( vbox )
      # TODO: Try to find pynotewiki.png on the system.
      self.window.set_icon_from_file( '/usr/share/pixmaps/pynotewiki.png' )
      self.window.show_all()

      self.load_wiki( wiki_path, page_uri )

      gtk.main()

   def load_wiki( self, wiki_path, page_uri ):
      # Open the notebook file.
      try:
         self.wiki = PyNoteWikiParser( wiki_path )
         self.wiki_path = wiki_path
         self.page_uri = page_uri

         # TODO: Make this a common function somewhere (maybe in the parser?).
         uri_break = urlparse.urlparse( page_uri )
         page_name = urllib.unquote_plus( uri_break[2][1:] )

         # Load the page source into the editor.
         buf = self.editor.get_buffer()
         buf.set_text( self.wiki.get_page( page_name ).get( 'body' ) )

      except Exception, e:
         md = gtk.MessageDialog(
            self.window,
            gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_CLOSE,
            'Unable to open wiki {}: {}'.format( wiki_path, e.message )
         )
         md.run()
         md.destroy()

         self.logger.error(
            'Unable to open wiki {}: {}'.format( wiki_path, e.message )
         )

   def on_save( self, widget ):
      pass

   def on_view( self, widget ):
      from viewer import PyNoteWikiViewer
      self.window.destroy()
      PyNoteWikiViewer( self.wiki_path, self.page_uri )

