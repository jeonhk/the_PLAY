from .View import *
from ..Model.Dot import Dot

import random

threshold = 0.3


class KeyView(View):
    def onInit(self):
        self.pressTime = 0
        self.score = None
        self.prevTime = None
        self.act = False

        height = self.scene.dotEndY - self.scene.dotStartY
        self.barSurface = gameapi.Surface((self.width, height), apiVar.SRCALPHA)

        self.minusScoreColor = (random.randint(192,255),random.randint(64,127),random.randint(64,127),255)
        self.plusScoreColor = (random.randint(64,127),random.randint(192,255),random.randint(64,127),255)
        
        self.downColor = (random.randint(64,127),random.randint(64,127),random.randint(196,255),255)
        
        
    
    def drawBar(self):
        self.drawRect((128,0,0), (0, self.scene.lineY, self.width, 5))

    def onUpdateTime(self, time):
        if self.prevTime == None:
            self.prevTime = time
        self.updateDots()
        if self.keyMiddle.check(self.pitch):
            self.pressTime = time
            if self.score == None:
                self.downColor = (random.randint(64,127),random.randint(64,127),random.randint(196,255),255)
                self.score = 0
                
            if self.act == True:
                self.score += 500*(time - self.prevTime)
            else :
                self.score -= 200*(time - self.prevTime)
        elif self.act == True:
            if self.score == None:
                self.score = 0
            self.score -= 100*(time - self.prevTime)
        else:
            if self.score != None:
                self.scene.score += self.score
                self.score = None
        if self.score != None:
            self.scene.updatingScore += self.score

        timediff = time - self.pressTime
        if timediff > threshold:
            ratio = 1
        else:
            ratio = timediff/threshold
        self.keyColor = [self.downColor[i] + (self.upColor[i] - self.downColor[i]) * ratio for i in [0,1,2,3]]

        self.prevTime = time

    def setMiddle(self, middle):
        self.middle = middle

        
    def drawDots(self):
        lineY = self.scene.lineY
        self.act = False
        for dot in self.dotList:
            if dot.info != None :
                
                color = (0,0,128)
                if dot.info[0] > lineY and dot.info[1] < lineY :
                    self.act = True
                    if self.keyMiddle.check(self.pitch):
                        if random.randint(0,1) == 0:
                            image = self.dotImage
                        else:
                            image = self.lineDotImage
                    else:
                        image = self.lineDotImage
                else:
                    image = self.dotImage

                left, right = self.getDotLeftRight()
                    
                rect = (left, dot.info[1], right, dot.info[0] - dot.info[1])
                self.drawResizeImage(image, rect)
                
                ''' draw rectangle
                self.drawRect(color, rect)
                '''

    


        

    def updateDots(self):
        self.dotList = self.middle.getData(self.pitch)


    def drawScore(self):
        if self.score != None:
            if self.score < 0:
                color = self.minusScoreColor
                score = -self.score
            else:
                color = self.plusScoreColor
                score = self.score
            self.drawRect(color, (0, 0, self.width, self.height/200 * (score % 200)))
        #        self.drawChar(str(int(self.score)), (0,-50), self.scene.scoreFont, (128, 50, 50))


        
        
            
                


        
