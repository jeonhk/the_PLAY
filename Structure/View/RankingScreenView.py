from .View import *
from ..Model.Score import HighScore

import pygame.midi as midi
import os

class RankingScreenView(View):
    def onInit(self):
        self.blue = gameapi.Color(0,0,255)
        self.fileSelected = False
        self.keyHelp = self.resizeImage(gameapi.image.load(os.path.join("Image","keyHelp.png")), (800, 200))
        
        
        
    def onDraw(self):            
        self.fill((0,0,0))

        song = self.scene.getSong()
        self.drawChar(song.name, (200,40), self.scene.font, (255,0,0))
        rank = self.scene.rank
        for i in range(5):
            if i == rank:
                color = (255,0,0)
            else:
                color = (0,255,0)

            score = "%20s"%str(song.slotList[i].score)
            self.drawChar(score, (0, 100 + 50*i), self.scene.font, color)
            self.drawChar(str(song.slotList[i].name), (400, 100 + 50*i), self.scene.font, color)
        
        self.drawImage (self.keyHelp, (0,350))

    def onEvent(self, event):
        if event.type == apiVar.KEYDOWN or event.type == midi.MIDIIN:
            pitch = self.keyMiddle.getPressedPitch(event)
            if pitch != None:
                if pitch >= 48 and pitch < 48+26:
                    c = chr(ord('a') + pitch - 48)
                    self.scene.addLetter(c)
                elif pitch == 83:
                    self.scene.backspace()
                elif pitch == 81:
                    self.scene.done()
                else:
                    self.scene.addLetter(" ")
