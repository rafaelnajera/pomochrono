#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Pomodoro Chrono
#

import os
import sys
import pygtk
pygtk.require('2.0')
import pynotify
import gtk
import gobject
import pango
import time
import re

#
# Some labels and constants
#

# Timer defaults
defaultTimeRatio = 21 / 16.0
defaultTimerPeriod = 250  #in milliseconds
defaultFont = "CMU Sans Serif 64"

#appPath = os.path.dirname(sys.argv[0])
appPath = "/usr/share/pomochrono/"

iconPath = appPath + "pomochrono.png"
alertSound = appPath + "alert.oga"



#
# A couple of helper functions
#
def playSound(fileName):
    os.system("play -V1 -q %s &" % (fileName))

def notifyUser(msg):
    global iconPath
    
    n = pynotify.Notification("Pomochrono", msg, "file://" + iconPath )
    n.show()

def formatTime(seconds):
    secs = int(seconds)
    sign = ' '
    if secs < 0:
        sign = "-"
        secs = -1 * secs
    hours = secs/3600
    secs = secs % 3600
    return "%s%d:%02d:%02d" % (sign, hours, secs/60, secs%60)

def processArguments(argVector):
    tr = None

    for arg in argVector[1:]:
        if re.match('^\d+\:\d+$', arg) != None:
            tStr = time.strftime('%Y-%m-%d')
            rt = time.strptime(tStr + ' ' + arg, '%Y-%m-%d %H:%M')
            tr = time.mktime(rt)
        else:
            raise TypeError("Unrecognized argument " + arg)
    return tr
        
    
#
#  The App
# 
class PomoChronoApp:

    
    def startTimer (self) :
        self.timerId =  gobject.timeout_add(self.timerPeriod,self.timerFunction) 
        
    def stopTimer (self) :
        gobject.source_remove(self.timerId)
    
    def updateChronoLabel(self) :
        currentTime = time.time()
        elapsedSeconds = currentTime - self.startTime
        self.currentPauseSeconds = 0
        if self.state == 1:
            self.currentPauseSeconds = currentTime - self.pauseStart
        workSeconds = elapsedSeconds - self.accPause -self.currentPauseSeconds       
        pomoSeconds = (workSeconds * self.timeRatio)
        breakSeconds = pomoSeconds - elapsedSeconds
        if breakSeconds <= 0:
            if not self.negativeBreak and not self.notifiedOfEndOfBreak:
                notifyUser('Break is over!')
                self.notifiedOfEndOfBreak = True
                playSound(alertSound)
            self.negativeBreak = True
        else:
            self.negativeBreak = False
            self.notifiedOfEndOfBreak = False
        
        self.elapsedLabel.set_label(formatTime(elapsedSeconds))
        self.breakLabel.set_label(formatTime(breakSeconds))
        self.pomoLabel.set_label(formatTime(pomoSeconds))
        
    def timerFunction(self) :
        self.startTimer()
        self.updateChronoLabel()
            
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def window_focus_in(self, widget, event) :
        self.window.set_title("PomoChrono")
        return False

    def buttonFunction(self, widget, data=None):
        if self.state == 0:
            self.state = 1
            self.pauseStart = time.time()
            self.button.set_label("Continue")
        elif self.state == 1:
            self.state = 0
            currentTime = time.time()
            self.currentPauseSeconds = currentTime - self.pauseStart
            self.accPause = self.accPause + self.currentPauseSeconds
            self.currentPauseSeconds = 0
            self.notifiedOfEndOfBreak = False
            self.button.set_label("Pause")
        else:
            g_print("Undefined state reached!!")
            self.state = 0

  

    def __init__(self, st = 0, r = defaultTimeRatio):
        
        self.timeRatio = r
        self.timerPeriod = defaultTimerPeriod
        print "Starting Pomochrono with ratio %.2f" % (self.timeRatio)
        if st == 0:
            self.startTime = time.time()
        else:
            self.startTime = st
        self.currentPauseSeconds = 0
        self.accPause = 0
        self.state = 0  # i.e., running
        self.notifiedOfEndOfBreak = False
        self.negativeBreak = False
        self.startTimer()
        pynotify.init('pomochrono')

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.connect("focus_in_event", self.window_focus_in)
        self.window.set_border_width(10)
        self.window.set_icon_from_file(iconPath)

        labelSt = gtk.Label("Start: %s\nRatio: %.3f = 1 / %.3f" % (time.strftime("%H:%M:%S", time.localtime(self.startTime)), self.timeRatio, 1/self.timeRatio))
        labelSt.modify_font(pango.FontDescription("Times 16"))
        label1 = gtk.Label("\nElapsed Time")
        self.elapsedLabel = gtk.Label("")
        self.elapsedLabel.modify_font(pango.FontDescription(defaultFont))
        label2 = gtk.Label("\nAccrued Break")
        self.breakLabel = gtk.Label("")
        self.breakLabel.modify_font(pango.FontDescription(defaultFont))
        label3 = gtk.Label("\nEffective Work Time")
        self.pomoLabel = gtk.Label("")
        self.pomoLabel.modify_font(pango.FontDescription(defaultFont))
        self.updateChronoLabel()
        self.button = gtk.Button("Pause")
        self.button.connect("clicked", self.buttonFunction, None)
        
        box = gtk.VBox()
        box.add(labelSt)
        box.add(label1)
        box.add(self.elapsedLabel)
        box.add(label2)
        box.add(self.breakLabel)
        box.add(label3)
        box.add(self.pomoLabel)
        box.add(self.button)
        self.window.add(box)
        labelSt.show()
        label1.show()
        self.elapsedLabel.show()
        label2.show()
        self.breakLabel.show()
        label3.show()
        self.pomoLabel.show()
        self.button.show()
        box.show()
        self.window.show()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    try:
        t = processArguments(sys.argv)
    except TypeError as e:
        print "Error: " + str(e)
        exit()

    if t==None:
        t=0
    chrono = PomoChronoApp(t)
    chrono.main()

