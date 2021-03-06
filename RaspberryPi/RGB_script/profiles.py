import wheels
import time
from pixelclass import *
class Profile(object):
    def __init__(self,pixels,name="BASIC"):
        self.pixels = pixels
        self.name = name
        self.rgb = wheels.COLORS["BLUE"]

    def setRGB(self,rgb):
        self.rgb = rgb

    def colorController(self):
        pass

    def brightnessController(self):
        pass
    
    
    def display(self):
        self.colorController()
        self.brightnessController()
        self.pixels.fill(self.rgb)
        self.pixels.show()

    def __str__(self):
        return f"This is a {self.name} profile\nRGB current values : ({self.rgb}) "

class IndexProfile(Profile):
    def __init__(self,pixels,name="INDEX"):
        super().__init__(pixels,name)
        self.index = [0] 
    
    def addToIndex(self,values):
        self.index.extend(values)
        print(self.index)

    def cleanArray(self,arr):
        indextopop = None
        for y in range(len(arr)):
            if arr[y]>150 or arr[y]<0:
                indextopop=y
        if indextopop != None:
            arr.pop(indextopop)
        return arr
    
    def display(self):

        for i in range(150):
            for y in range(len(self.index)):
                if i == self.index[y]:
                    self.pixels[self.index[y]] = (self.rgb)
    
            if i not in self.index:
                self.pixels[i] = (0,0,0)

        print(self.index)
        self.pixels.show()
        self.index = self.cleanArray(self.index)

    
class ColorFadeProfile(Profile):
    def __init__(self,pixels):
        super().__init__(pixels,"COLORFADE")
        super().setRGB(wheels.COLORS["RED"])
    def colorController(self):
        self.rgb = wheels.colorwheel(self.rgb)

class BreathingProfile(Profile):
    def __init__(self,pixels, refresh=0.02, brightness=0.2):
        super().__init__(pixels,"BREATH")
        super().setRGB(wheels.COLORS["WHITE"])
        self.refresh = refresh
        self.brightness = brightness
        self.x = 0.01

    def display(self):
        super().display()
        time.sleep(self.refresh)
        
    def brightnessController(self):
        if self.pixels.brightness >= self.brightness:
            self.x = -self.x
        elif self.pixels.brightness <= 0:
            self.x = -self.x
            self.pixels.brightness = 0 
        self.pixels.brightness += self.x
        print(self.pixels.brightness)

class FlashProfile(Profile):
    def __init__(self,pixels, refresh=0.001, brightness=1):
        super().__init__(pixels,"FLASH")
        super().setRGB(wheels.COLORS["WHITE"])
        self.refresh = refresh
        self.brightness = brightness
        self.x = -0.06

    def display(self):
        super().display()
        time.sleep(self.refresh)
        
    def brightnessController(self):
        

        if self.pixels.brightness <= 0:
            self.pixels.brightness = self.brightness
            time.sleep(0.5)
        if self.pixels.brightness - self.x < 0:
            self.pixels.brightness = 0
        else:
            self.pixels.brightness += self.x
        
        print(self.pixels.brightness)

class ColorBreathingProfile(BreathingProfile):
    def __init__(self,pixels):
        super().__init__(pixels)
        super().setRGB(wheels.COLORS["GREEN"])
        self.name = "COLORBREATH"
    def colorController(self):
        self.rgb = wheels.colorwheel(self.rgb,3)


class LoadingProfile(Profile):
    def __init__(self,pixels,cursor=0,refresh=0.3):
        self.cursor = cursor
        self.cursor2 = cursor
        self.refresh = refresh
        super().__init__(pixels,"LOADING")
        pixels.fill((0,0,0))
        super().setRGB(wheels.COLORS["RED"])

    def display(self):
        self.pixels[self.cursor] = (self.rgb)
        self.pixels[self.cursor2] = (self.rgb)
        self.pixels.show()
        
        if self.cursor<149:
            self.cursor+=1
        if self.cursor2>0:
            self.cursor2-=1
        if self.cursor>149:
            self.cursor=149
        time.sleep(self.refresh)
    
    def resetCursor(self, cursor):
        self.cursor = cursor
        self.cursor2 = cursor

class SnakeProfile(IndexProfile):
    def __init__(self,pixels, refresh=0.05):
        super().__init__(pixels,"SNAKE")
        super().setRGB(wheels.COLORS["WHITE"])
        self.refresh = refresh
        self.index=[]
        self.front=[]
        self.back=[]

    def addToIndex(self,values):
        self.front.extend(values)
        self.back.extend(values)
    
    
    
    def display(self):
        self.index = self.front + self.back
        super().display()
    
        for y in range(len(self.front)):
            self.front[y] += 1
        for y in range(len(self.back)):
            self.back[y] -= 1
        self.front=super().cleanArray(self.front)
        self.back=super().cleanArray(self.back)
        time.sleep(self.refresh)

class CometProfile(IndexProfile):
    def __init__(self,pixels, refresh=0.05):
        super().__init__(pixels,"COMET")
        super().setRGB((255,0,255))
        self.refresh = refresh
        self.index=[1,2,3,4]
        self.x = 1

    def cleanArray(self, arr):
        return arr
    def display(self):
        super().display()
    
        for y in range(len(self.index)):
            if self.index[y] == 60 or self.index[y] == 0:
                self.x = -self.x
                break
        for y in range(len(self.index)):
            self.index[y] += self.x
        time.sleep(self.refresh)



class ColorWaveProfile(Profile):
    def __init__(self,pixels,refresh=0.001,c1 = wheels.COLORS["YELLOW"],c2=wheels.COLORS["WHITE"]):
        super().__init__(pixels,"COLORWAVE")
        self.pixelscolors = PixelColors(150)
        self.refresh = refresh
        self.startcolor = c1
        self.target = c2
        self.rgb = self.startcolor
        self.pixelscolors.fillAll(self.startcolor)
        self.start()
        
        
        
    def start(self):
        for i in range(150):

            self.rgb = wheels.colorGradient(self.rgb,self.target,20)
            self.pixelscolors.setColor(i,self.rgb)

            if self.rgb == self.target:
                self.target = self.startcolor
                self.startcolor = self.rgb
            elif self.rgb == self.startcolor:
                self.startcolor = self.target
                self.target = self.rgb

            self.pixels[i] = self.rgb
            self.pixels.show()
        

    def setColors(self,c1,c2):
        self.startcolor = c1
        self.target = c2
        self.start()
    
    def display(self):
        for i in range(150):
            if self.pixelscolors.getColor(i) == self.target:
                self.pixelscolors.setHighLow(i,False)
            elif self.pixelscolors.getColor(i) == self.startcolor:
                self.pixelscolors.setHighLow(i,True)
            
            if self.pixelscolors.getHighLow(i):
                self.pixelscolors.setColor(i,wheels.colorGradient(self.pixelscolors.getColor(i),self.target,))
            else:
                self.pixelscolors.setColor(i,wheels.colorGradient(self.pixelscolors.getColor(i),self.startcolor))

            self.pixels[i] = self.pixelscolors.getColor(i)
 
        self.pixels.show()
        time.sleep(self.refresh)


class StarsProfile(Profile):
    def __init__(self,pixels,refresh=0.001):
        super().__init__(pixels,"STARS")
        self.pixelscolors = PixelColors(150)
        self.refresh = refresh
        self.startcolor = wheels.COLORS["BLUE"]
        self.target = wheels.COLORS["WHITE"]
        self.rgb = self.startcolor
        self.pixelscolors.fillAll(self.startcolor)
        self.start()

    def start(self):
        for i in range(150):

            self.rgb = wheels.randomColorGradient(self.rgb,self.target,2)
            self.pixelscolors.setColor(i,self.rgb)

            if self.rgb == self.target:
                self.target = self.startcolor
                self.startcolor = self.rgb
            elif self.rgb == self.startcolor:
                self.startcolor = self.target
                self.target = self.rgb

            self.pixels[i] = self.rgb
            self.pixels.show()
    def display(self):
        for i in range(150):
            if self.pixelscolors.getColor(i) == self.target:
                self.pixelscolors.setHighLow(i,False)
            elif self.pixelscolors.getColor(i) == self.startcolor:
                self.pixelscolors.setHighLow(i,True)
            
            if self.pixelscolors.getHighLow(i):
                self.pixelscolors.setColor(i,wheels.colorGradient(self.pixelscolors.getColor(i),self.target,))
            else:
                self.pixelscolors.setColor(i,wheels.colorGradient(self.pixelscolors.getColor(i),self.startcolor))

            self.pixels[i] = self.pixelscolors.getColor(i)
 
        self.pixels.show()
        time.sleep(self.refresh)

class WebProfile(Profile):
    def __init__(self,pixels):
        super().__init__(pixels)
        super().setRGB(wheels.COLORS["CYAN"])
        self.name = "WEBSITE"
    def setRGB(self,rgb):
        super().setRGB(rgb)
        print(f"Changed RGB to : {rgb}")
    
