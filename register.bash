#!/usr/bin/bash

#
# Register the pomodoro app in the Gnome Desktop
#
ICON=pomochrono.png
DESKTOP_FILE=pomochrono.desktop

cp $ICON /usr/share/pixmaps
cp $DESKTOP_FILE /usr/share/applications

update-desktop-database
