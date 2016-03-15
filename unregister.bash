#!/usr/bin/bash

#
# Un-Register the pomodoro app in the Gnome Desktop
#

ICON=pomochrono.png
DESKTOP_FILE=pomochrono.desktop

rm /usr/share/pixmaps/$ICON 
rm /usr/share/applications/$DESKTOP_FILE 

update-desktop-database
