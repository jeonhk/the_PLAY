from .Scene import *

from ..View.GameScreenView import GameScreenView
from ..Middle.pianoKey import pianoKey

class GameScene(Scene):
    def initModel(self):
        self.dotStartY = -300
        self.lineY = 100
        self.dotEndY = 300
        self.setDotSpeed(150)

        self.playTime = 0
        self.play = True

        self.pianoKeyObserver = []

    def setSong(self, path):
        key = pianoKey(path)
        key.scene = self

        for e in self.pianoKeyObserver:
            e.setMiddle(key)
        

    def setDotSpeed(self, pixelPerSecond):
        self.dotSpeed = pixelPerSecond
        self.startTimeOffset = (self.lineY - self.dotStartY) / pixelPerSecond
        self.endTimeOffset = (self.lineY - self.dotEndY) / pixelPerSecond
    
    def initMainView(self):
        self.mainView = GameScreenView(self, None, (1000, 1000))

    def updateTime(self, time):
        try:
            if self.play:
                self.playTime += time - self.prevTime
        except:
            self.prevTime = time
        self.prevTime = time

        super().updateTime(time)
        