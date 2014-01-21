# pselc3

This is a simple gtk2-gui for browsing & watching recorded lectures of the [Chaos Communiction Congress(es)](http://events.ccc.de/congress/).

It simply lists all video-files & shows the description from the corresponding C3-wiki.
A video can then be played directly from the server (using mplayer, vlc or whatever mediaplayer you use)

It was intended as a lightweight, fast and easy interface to watch all the lectures on a mediacenter without using a browser.

Currently, there are two "configurations" available: for the 29C3 and 30C3. 
It's probably easy to include other conferences (recordings are available since 22C3) or even use this as a starting-point for completely different stuff.


## Installation

pselc3 needs Python 2, pygtk and pywebkitgtk. 

Be shure to check to start-/config files (`p29c3.py`, `p30c3.py`) for resolution, mediaplayer etc.

it is possible to load a custom GTK-RC-file (for larger font etc.) as well.
(`gtk_clear` is included as an example with large white font and gray background)

