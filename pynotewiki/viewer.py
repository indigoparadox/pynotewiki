#!/usr/bin/env python

'''
This file is part of PyNoteWiki.

PyNoteWiki is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

PyNoteWiki is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more 
details.

You should have received a copy of the GNU General Public License along
with PyNoteWiki.  If not, see <http://www.gnu.org/licenses/>.
'''

import gtk
import webkit
import wikiconfig
import os
import logging
import urlparse
import urllib
from parser import PyNoteWikiParser
from wikiconfig import PyNoteWikiConfig

DEFAULT_CSS = '.missing { color: red }'
DEFAULT_PAGE_URI = 'wiki:///Home'

STATUSBAR_CONTEXT_UPDATED = 1

class PyNoteWikiViewer:
   
   window = None
   viewer = None
   wiki = None
   wiki_path = None
   logger = None
   page_uri = None
   history = []
   goingback = False
   config = None
   statusbar = None
   visitingsame = False

   def __init__( self, wiki_path=None, page_uri=None ):

      self.logger = logging.getLogger( 'pynotewiki.viewer' )

      self.config = PyNoteWikiConfig()

      # Create the main window.
      self.window = gtk.Window()
      self.window.set_title( 'PyNoteWiki Viewer' )
      self.window.connect( 'destroy', gtk.main_quit )

      mb = gtk.MenuBar()

      # Add a file menu.
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

      # Add a navigation menu.
      navmenu = gtk.Menu()
      navm = gtk.MenuItem( 'Navigation' )
      navm.set_submenu( navmenu )

      homem = gtk.MenuItem( 'Home' )
      homem.connect( 'activate', self.on_home )
      navmenu.append( homem )

      backm = gtk.MenuItem( 'Back' )
      backm.connect( 'activate', self.on_back )
      navmenu.append( backm )

      mb.append( navm )

      # Add a toolbar.
      toolbar = gtk.Toolbar()

      openb = gtk.ToolButton( gtk.STOCK_OPEN )
      openb.connect( 'clicked', self.on_open )
      homeb = gtk.ToolButton( gtk.STOCK_HOME )
      homeb.connect( 'clicked', self.on_home )
      backb = gtk.ToolButton( gtk.STOCK_GO_BACK )
      backb.connect( 'clicked', self.on_back )
      editb = gtk.ToolButton( gtk.STOCK_EDIT )
      editb.connect( 'clicked', self.on_edit )
   
      toolbar.insert( openb, 0 )
      toolbar.insert( gtk.SeparatorToolItem(), 1 )
      toolbar.insert( homeb, 2 )
      toolbar.insert( backb, 3 )
      toolbar.insert( gtk.SeparatorToolItem(), 4 )
      toolbar.insert( editb, 5 )

      # Add the HTML viewer.
      self.viewer = webkit.WebView()
      self.viewer.connect(
         'navigation-policy-decision-requested', self.on_navigate_decision
      )
      self.display_html( 'Welcome to PyNoteWiki!' )

      viewer_scroller = gtk.ScrolledWindow()
      viewer_scroller.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
      viewer_scroller.add( self.viewer )

      # Add a status bar.
      self.statusbar = gtk.Statusbar()

      # Pack the widgets and show the window.
      vbox = gtk.VBox( False, 2 )
      vbox.pack_start( mb, False, False, 0 )
      vbox.pack_start( toolbar, False, False, 0 )
      vbox.pack_start( viewer_scroller, True, True, 0 )
      vbox.pack_start( self.statusbar, False, False, 0 )
      self.window.add( vbox )
      # TODO: Try to find pynotewiki.png on the system.
      self.window.set_icon_from_file( '/usr/share/pixmaps/pynotewiki.png' )
      self.window.show_all()

      if None != wiki_path:
         self.load_wiki( wiki_path, page_uri )

      gtk.main()

   def load_wiki( self, wiki_path, page_uri=None ):
      # Open the notebook file.
      try:
         self.wiki = PyNoteWikiParser( wiki_path )
         self.wiki_path = wiki_path
         self.goingback = False
         self.page_uri = None
         self.history = []
         if None != page_uri:
            self.viewer.open( page_uri )
         else:
            self.viewer.open( DEFAULT_PAGE_URI )
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

   def display_html( self, string_in, return_html=False ):
      
      # TODO: Wrap the string in HTML headers with user-definable CSS from the
      #       config.

      # TODO: Escape the saved CSS for safety.
      string_in = '<html><head><style type="text/css">' + DEFAULT_CSS + \
         '</style><style type="text/css">' + \
         self.config.get_value( 'PageCSS' ) + '</style></head><body>' + \
         string_in + '</body></html>'

      if return_html:
         return string_in
      else:
         self.viewer.load_html_string( string_in, 'wiki:///' )

   def on_open( self, widget ):

      # Display a file open dialog.
      dialog =  gtk.FileChooserDialog(
         'Open Notebook...',
         None,
         gtk.FILE_CHOOSER_ACTION_OPEN,
         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK)
      )
      dialog.set_default_response( gtk.RESPONSE_OK )
      if None != self.config.get_value( 'LastDir' ):
         dialog.set_current_folder( self.config.get_value( 'LastDir' ) )

      # TODO: Poll the parser plugins and get the list of valid extensions.
      nbkfilter = gtk.FileFilter()
      nbkfilter.set_name( 'MMD Wikis' )
      nbkfilter.add_pattern( 'Home.md' )
      dialog.add_filter( nbkfilter )

      nbkfilter = gtk.FileFilter()
      nbkfilter.set_name( 'Notebook Files' )
      nbkfilter.add_pattern( '*.nbk' )
      dialog.add_filter( nbkfilter )

      response = dialog.run()
      if gtk.RESPONSE_OK == response:
         # Store the last used path for later.
         self.config.set_value(
            'LastDir', os.path.dirname( dialog.get_filename() )
         )

         self.load_wiki( dialog.get_filename() )

      dialog.destroy()

   def on_navigate_decision( self, view, frame, req, act, poldec ):
      uri = req.get_uri()

      # Aggressively weed out non-local pages for now so that we can control
      # integration with CSS, etc. Maybe later we can open them in a proper
      # browser window.
      if not uri.startswith( 'wiki:' ):
         poldec.ignore()
         return True

      # Don't infinitely loop, but don't allow going to the same page more 
      # than once because webkit doesn't seem to like that.
      if uri == self.page_uri:
         if not self.visitingsame:
            poldec.use()
            self.visitingsame = True
            return True
         else:
            self.logger.debug( 'Attempted to visit same page.' )
            poldec.ignore()
            return True
      self.visitingsame = False

      # Store the URI for the coming page and parse it to be usable.
      uri_break = urlparse.urlparse( uri )
      page_name = urllib.unquote_plus( uri_break[2][1:] )

      # Allow only wiki pages.
      # TODO: Determine valid wiki pages present in the wiki from invalid ones.
      if '' == page_name:
         return False

      # Allow allow pages when a wiki is loaded.
      if None == self.wiki:
         poldec.ignore()
         return True

      # Set the new page name and add the old one to the history pile.
      # TODO: Figure out how to not append backtracked items to the history
      #       without using a pseudo-global.
      if not self.goingback and None != self.page_uri:
         self.logger.info( 'Adding "{}" to history...'.format( self.page_uri ) )
         self.history.append( self.page_uri )
      else:
         self.goingback = False
      self.page_uri = uri

      # Load and display the wiki page.
      self.logger.info( 'Loading wiki page "{}"...'.format( page_name ) )
      frame.load_string(
         self.display_html(
            self.wiki.get_page_html( page_name ), True
         ),
         'text/html',
         'iso-8859-15',
         uri
      )

      # Display the page status.
      # TODO: Format the updated time for display.
      page = self.wiki.get_page( page_name )
      self.statusbar.pop( STATUSBAR_CONTEXT_UPDATED )
      self.statusbar.push( STATUSBAR_CONTEXT_UPDATED, page.get( 'updated' ) )

      poldec.ignore()
      return True

   def on_back( self, widget ):
      try:
         self.goingback = True
         backstep = self.history.pop()
         self.viewer.open( backstep )
      except:
         # Guess we're not going back after all!
         self.goingback = False
         self.logger.error( 'Tried to go back too many times.' )

   def on_home( self, widget ):
      self.viewer.open( DEFAULT_PAGE_URI )

   def on_edit( self, widget ):
      from editor import PyNoteWikiEditor
      self.window.destroy()
      PyNoteWikiEditor( self.wiki_path, self.page_uri )

