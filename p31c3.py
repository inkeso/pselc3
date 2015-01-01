#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# include different GTK-file (e.g. with larger fonts)
#import sys, os
#os.environ["GTK2_RC_FILES"] = os.path.join(sys.path[0],"gtk_clear")

import pselc3_gtk

################################## 31C3-Config #################################

app = pselc3_gtk.Pselect({
    # window-title
    "Title" : "31C3",

    # initial window-size. Tuple of (X,Y) or "fullscreen"
    "Size"  : (1024,768),
    #"Size" : "fullscreen"

    # which mediaplayer do you use? I really like mplayer
    "playerCmd" : "mplayer -fs '%s'",

    # show infos for each event
    "showMovieInfos" : True,

    # URL to fetch movie infos from (by 4-digit-ID)
    # see https://events.ccc.de/congress/2014/Fahrplan/events.html
    "murl" : "https://events.ccc.de/congress/2014/Fahrplan/events/%s.html",
    "mrex" : r'<div id="main-content">(.*)</div>',
    "head" : """
        <html><head>
        <link rel="Stylesheet" href="../style.css" type="text/css"></link>
        <style>
            body, h1     { font-size: 22px; font-family:Tahoma; line-height:32px; background: #444; color: white; }
            table        { font-size: 20px; line-height: 28px; }
            h1           { font-size: 30px; }
            a            { text-decoration: none; color: white; }
            div.image    { float: left; margin:0.5em; }
            #details     { float: left; background: #555; padding-left:0.5em; float: left; margin:0; }
            #sidebar     { float: right; padding: 0.5em; padding-top:0;  background: #555; margin:0; }
            #details h3  { display: none; }
            #details p a { display: none; }
            #details ul  { display: none; }
            #details p a[href^="/congress/2013/Fahrplan/schedule"] { display: inline; }
            #concurrent_events, .release { display: none; }
        </style>
        </head><body>
    """,
    "foot" : """
        </body></html>
    """,

    # this is where we get the stream for playback
    "base" : "http://cdn.media.ccc.de/congress/2014/h264-hd/",
    #"base" : "http://mirror.fem-net.de/CCC/31C3/mp4/",

    # match filenames, group for ID, Language and Name and complete filename within index-HTML
    "rex" : r'<a href="31c3-([0-9]{4})-([end-]+?)-(.+?)_hd.mp4">(31c3-.+?_hd.mp4)</a>'
})

