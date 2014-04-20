from struct import unpack

from ..Middle import gameapi
from ..Middle import apiVar

from .MIDI.constants import *

from .MIDI.Song import Song
from ..Model.Dot import Dot

key = {
    'a':60,
    'w':61,
    's':62,
    'e':63,
    'd':64,
    'f':65,
    't':66,
    'g':67,
    }
status = [False] * 128

class pianoKey ():
    
    def __init__(self, file_name):
        song = Song(file_name)
        self.keyList = [[]]*128
        for i in range(128):
            onEvents = song.checkForEvent(i, 0x01)
            self.keyList[i] = self.createDots(onEvents)
            offEvents = song.checkForEvent(i, 0x00)
            self.addEndTimesToDots(offEvents, self.keyList[i])
        self.endTime = song.endTime

    def check(self, pitch):
        return status[pitch]

    def updateStatus(self, event):
        try:
            if event.type == apiVar.KEYDOWN:
                status[key[gameapi.key.name(event.key)]] = True
            elif event.type == apiVar.KEYUP:
                status[key[gameapi.key.name(event.key)]] = False
        except:
            print("not supported key")
        
    def createDots (self, onEvents):
        length = len(onEvents)
        dotList = []
        for i in range (0,length):
            dot = Dot(onEvents[i].startTime)
            dotList.append(dot)
        
        return dotList

    def addEndTimesToDots(self, offEvents, keyList):
        length = len(offEvents)
        if length == 0:
            return
        
        for i in range (length - 1):
            if (keyList[i+1].startTime > offEvents[i].startTime):
                keyList[i].endTime = offEvents[i].startTime
        keyList[-1].endTime = offEvents[-1].startTime

    def getData(self, pitch, playtime = None):
        if playtime == None:
            playtime = self.scene.playTime
            
        dotSpeed = self.scene.dotSpeed
        lineY = self.scene.lineY
        dotStartY = self.scene.dotStartY
        dotEndY = self.scene.dotEndY

        dotList = self.keyList[pitch]

        removeList = []        
        for dot in dotList:
            startY = (playtime - dot.startTime) * dotSpeed + lineY
            if startY > dotEndY:
                startY = dotEndY
            elif startY < dotStartY:
                dot.info = None
                continue

            if dot.endTime == None:
                endY = dotStartY
            else :
                endY = (playtime - dot.endTime) * dotSpeed + lineY
                if endY > dotEndY:
                    removeList.append(dot)
                    continue
                elif endY < dotStartY:
                    endY = dotStartY

            dot.info = (startY, endY)

        for e in removeList:
            dotList.remove(e)

        return dotList
        
