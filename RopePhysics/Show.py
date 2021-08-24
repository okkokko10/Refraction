import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import pygame

picked=[]
def ClickingScreen(self:World,events,screen:Screen.Screen):
    for e in events:
        if e.type==pygame.MOUSEBUTTONDOWN:
            button=e.__dict__['button']
            pos=e.__dict__['pos']
            if button==1:
                self.AddParticle(pos,(0,0),10)
            if button==3:
                i=NearestParticle(self,pos)[0]
                if i:
                    picked.append(i)
            if button==2:
                self.ConnectSpringRest(picked[-1],picked[-2],50)
    pass
def NearestParticle(self:World,pos,minDistanceSq=-1):
    'from Show.py \n\nreturns tuple, the particle nearest to the point, and the distance squared. setting minDistanceSq positive excludes nearer particles from the search'
    nearest=0
    lengthSq=10000
    for i in self.particles:
        p=self.GetParticle(i)
        d=(p.pos-pos)
        lSq=d.length_squared()
        if minDistanceSq<lSq<lengthSq:
            nearest=i
            lengthSq=lSq
    if lengthSq!=10000:
        return nearest,lengthSq
    else:
        return None,lengthSq
#World.NearestParticle=NearestParticle

#World.AddScreenEventFunc(ScreenEventHook)