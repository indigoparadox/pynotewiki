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

class PyNoteWikiEditor:

   window = None
   editor = None
   wiki = None

   @classmethod
   def from_wiki_path( cls, wiki_path, page_uri='wiki:///Home' ):
      new_editor = cls()
      new_editor.load_wiki( wiki_path, page_uri )
      return new_editor

   def __init__( self ):

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

      # Create the editor.
      self.editor = gtk.TextView()

      editor_scroller = gtk.ScrolledWindow()
      editor_scroller.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
      editor_scroller.add( self.editor )

      # Pack the widgets and show the window.
      vbox = gtk.VBox( False, 2 )
      vbox.pack_start( mb, False, False, 0 )
      #vbox.pack_start( toolbar, False, False, 0 )
      vbox.pack_start( editor_scroller, True, True, 0 )
      #vbox.pack_start( self.statusbar, False, False, 0 )
      self.window.add( vbox )
      # TODO: Try to find pynotewiki.png on the system.
      self.window.set_icon_from_file( '/usr/share/pixmaps/pynotewiki.png' )
      self.window.show_all()

      gtk.main()

   def load_wiki( self, wiki_path ):
      pass

