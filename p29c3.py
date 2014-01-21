#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# include different GTK-file (e.g. with larger fonts)
#import sys, os
#os.environ["GTK2_RC_FILES"] = os.path.join(sys.path[0],"gtk_clear")

import pselc3_gtk

################################## 29C3-Config #################################

app = pselc3_gtk.Pselect({
    # window-title
    "Title" : "30C3",

    # initial window-size. Tuple of (X,Y) or "fullscreen"
    "Size"  : (1024,768),
    #"Size" : "fullscreen",
    
    # which mediaplayer do you use? I really like mplayer
    "playerCmd" : "mplayer -fs '%s'",

    # show infos for each event
    "showMovieInfos" : True,

    # URL to fetch movie infos from (by 4-digit-ID)
    # see http://events.ccc.de/congress/2012/Fahrplan/events.de.html
    "murl" : "http://events.ccc.de/congress/2012/Fahrplan/events/%s.de.html",
    "mrex" : r'<div class="section vevent" id="event">(.*)</div>',
    "head" : """
        <html><head>
        <link rel="Stylesheet" href="../style.css" type="text/css"></link>
        <style>
            body, table, h1 { font-size: 22px; font-family:Tahoma; line-height:32px; }
            table { font-size: 20px; line-height: 28px; }
            h1 { font-size: 30px; }
            #infobox { width: 350px; }
            #navigation { display: none; }
            .feedback { display: none; }
            th { display: none; }
        </style>
        </head><body>
    """,
    "foot" : """
        </body></html>
    """,

    # this is where we get the stream for playback
    "base" : "http://cdn.media.ccc.de/congress/2012/mp4-h264-HQ/",
    #"base" : "http://mirror.fem-net.de/CCC/29C3/mp4/",
    
    # match filenames, group for ID, Language and Name and complete filename within index-HTML
    "rex" : r'<a href="29c3-([0-9]{4})-(de-en|en|de)-(.+?)_h264.mp4">(29c3-.+?_h264.mp4)</a>'
})

