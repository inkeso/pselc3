#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
import urllib, re
import gobject, gtk, webkit
import threading

gtk.gdk.threads_init()

class GeneratorTask(object):
    """
    Helper-Class for Multithreading. It is used to retrieve an show MovieInfos
    without losing the ability to navigate through the list
    """
    def __init__(self, generator, loop_callback, complete_callback=None):
        self.generator = generator
        self.loop_callback = loop_callback
        self.complete_callback = complete_callback

    def _start(self, *args, **kwargs):
        self._stopped = False
        for ret in self.generator(*args, **kwargs):
            if self._stopped:
                thread.exit()
            gobject.idle_add(self._loop, ret)
        if self.complete_callback is not None:
            gobject.idle_add(self.complete_callback)

    def _loop(self, ret):
        if ret is None:
            ret = ()
        if not isinstance(ret, tuple):
            ret = (ret,)
        self.loop_callback(*ret)

    def start(self, *args, **kwargs):
        threading.Thread(target=self._start, args=args, kwargs=kwargs).start()

    def stop(self):
        self._stopped = True


class Pselect():
    columns = ("Name","Language","ID","URL")
    cTypes  = (str,str,str,str)
    
    def __init__(self, cfg):
        self.cfg = cfg
        
        # GUI
        # - GtkHBox
        #   +- GtkScrolledWindow
        #   |  +- GtkTreeView (movielist)
        #   +- GtkScrolledWindow
        #      +- WebView (mozi)
        
        # Movie list
        self.treestore = gtk.TreeStore(*self.cTypes) 
        self.movielist = gtk.TreeView()
        self.movielist.set_model(self.treestore)
        # create the TreeViewColumnw to display the data
        cell = gtk.CellRendererText()                   # create a CellRenderer
        for cn in range(len(self.columns)):
            one = gtk.TreeViewColumn(self.columns[cn])  # create column-object
            one.pack_start(cell, cn==0)                 # add cell & allow expansion, if first
            one.add_attribute(cell, 'text', cn)         # retrieve text from corresponding column in treestore
            self.movielist.append_column(one)           # add column to TreeView
        
        self.movielist.set_headers_visible(False)       # hide headers
        self.movielist.get_column(2).set_visible(False) # hide ID-column
        self.movielist.get_column(3).set_visible(False) # hide url-column
        self.movielist.set_search_column(0)             # make it searchable
        # Create a ScrolledWindow with movielist and add it to a HBox
        self.scrollml = gtk.ScrolledWindow()
        self.scrollml.add(self.movielist)
        self.hbox = gtk.HBox(spacing=2)
        self.hbox.pack_start(self.scrollml)
        
        if self.cfg["showMovieInfos"]: # create the html-info-viewer
            self.mozi = webkit.WebView() 
            self.mozi.load_html_string(self.cfg["head"] + '''
                <div style="font-size:2em;text-align:center;"><br/>Loading...<br/><br/>
                <img src="file:///'''+sys.path[0]+'''/wait.gif" style="display:block;margin:auto;" /></div>
                ''' + self.cfg["foot"], "file:///"+sys.path[0])
            self.scrollmi = gtk.ScrolledWindow()
            self.scrollmi.add(self.mozi)
            self.hbox.pack_start(self.scrollmi)
        
        # Main Window
        self.wind = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.wind.set_title(self.cfg["Title"])
        if "Size" in self.cfg:
            if type(self.cfg["Size"]) == str and self.cfg["Size"].lower() == "fullscreen":
                self.wind.maximize();
            elif type(self.cfg["Size"]) in (tuple, list):
                self.wind.set_default_size(*self.cfg["Size"])
        else:
            self.wind.set_default_size(800, 600) # default
        self.wind.add(self.hbox)
        self.wind.show_all()
        
        # assign event-handlers
        self.wind.connect("destroy", gtk.main_quit) # or on ESC:
        self.movielist.connect("key-press-event", lambda x,y: (y.keyval == 65307 and gtk.main_quit()))
        self.movielist.connect("cursor-changed",  self.on_ml_cursor)
        self.movielist.connect("row-activated",   self.on_ml_activate)
        
        # get filelist & start GTK-mainloop
        self.filist = [] # list of files, see getFiles()
        GeneratorTask(self.getFiles, self.movielist.set_cursor).start()
        gtk.main()
    
    def getFiles(self):
        # get list of files from index-HTML
        http = urllib.urlopen(self.cfg["base"])
        page = http.read()
        http.close()
        self.filist = re.findall(self.cfg["rex"], page)
        self.filist.sort(cmp=lambda x,y: (x[2].lower()>y[2].lower())*2-1)
        for foo in self.filist:
            # since colums are [Name, Language, ID, URL] we have to reorder
            self.treestore.append(None, (foo[2], foo[1], foo[0], self.cfg["base"]+foo[3]))
        yield 0
    
    def getMovieInfo(self, movie):
        """
        Retrieve MovieInfos from the net
        """
        http = urllib.urlopen(self.cfg["murl"] % movie)
        page = http.read()
        http.close()
        mdet = re.search(self.cfg["mrex"], page, re.DOTALL)
        mdes = ""
        if mdet is not None:
            mdes = mdet.group(1).strip()
        else:
            mdes = "No description available"
        yield mdes
    
    def setMovieHtml(self, mdes):
        self.mozi.load_html_string(self.cfg["head"] + mdes + self.cfg["foot"], self.cfg["murl"][:self.cfg["murl"].index("%s")])
    
    def on_ml_cursor(self, tv):
        selected = self.movielist.get_cursor()[0]
        if self.cfg["showMovieInfos"]:
            film = self.treestore.get_value(self.treestore.get_iter(selected),2)
            GeneratorTask(self.getMovieInfo, self.setMovieHtml).start(film)
    
    def on_ml_activate(self, tv, selected, cColumn):
        sUrl = self.treestore.get_value(self.treestore.get_iter(selected),3)
        if self.cfg["showMovieInfos"]:
            self.mozi.load_html_string('''%s
                <div style="font-size:2em;text-align:center;"><br/>Playing</div><br/>
                <div style="text-align:center;">%s</div>%s
                ''' % (self.cfg["head"], sUrl, self.cfg["foot"]), "file:///"+sys.path[0])
            while gtk.events_pending(): gtk.main_iteration()
        
        os.system(self.cfg["playerCmd"] % sUrl)
        
        if self.cfg["showMovieInfos"]:
            for f in self.getMovieInfo(self.treestore.get_value(self.treestore.get_iter(selected),2)):
                self.setMovieHtml(f)

