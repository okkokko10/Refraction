import pygame
import Screen


class Crossing:
    def __init__(self,nodeA,outA,nodeB,outB,pos,ID,isInput=False):
        self.ID = ID
        self.isInput = isInput
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeAOut = outA
        self.nodeBOut = outB
        self.pos = pos
        self.value =[0,0]
        self.newValue =[0,0]
    def update(self,getOthers):
        if not self.isInput:
            self.newValue[0]=getOthers(self.nodeA,self.nodeAOut)
            self.newValue[1]=getOthers(self.nodeB,self.nodeBOut)
            if self.newValue[0] and self.newValue[1]:
                self.newValue=[0,0]
    def inputUpdate(self,values):
        self.newValue[0]=values[self.ID]
        self.newValue[1]=values[self.ID]
    def postUpdate(self):
        self.value=self.newValue.copy()
    def Draw(self,screen,others):
        if not self.isInput:
            screen.DrawLine(self.pos+pygame.math.Vector2(-20,-20),others[self.nodeA].pos+pygame.math.Vector2(20,-20+40*self.nodeAOut),(others[self.nodeA].value[self.nodeAOut]*200,0,100),10)
            screen.DrawLine(self.pos+pygame.math.Vector2(-20,20),others[self.nodeB].pos+pygame.math.Vector2(20,-20+40*self.nodeBOut),(others[self.nodeB].value[self.nodeBOut]*200,0,100),10)
        screen.DrawLine(self.pos+pygame.math.Vector2(0,10),self.pos-pygame.math.Vector2(0,10),(100+self.isInput*100,self.value[0]*200,self.value[1]*200),20)
        
    


crossings={}
inputNodes={}
inputValues={}
IDiter=1
unfinishedCrossing=[]
def NearestNode(pos,others):
    nearest=0
    length=1000000
    for i in others:
        l=(others[i].pos[0]-pos[0])**2+(others[i].pos[1]-pos[1])**2
        if l<length:
            nearest=i
            length=l
    return nearest, others[nearest].pos[1]<pos[1]
def AddCrossing(events,others):
    IDiter=globals()['IDiter']
    for e in events:
        if e.type==pygame.MOUSEBUTTONDOWN:
            pos=e.__dict__['pos']
            if e.__dict__['button']==pygame.BUTTON_LEFT:
                stage=len(unfinishedCrossing)
                if stage<3:
                    unfinishedCrossing.append(pos)
                if stage==2:
                    a,aO=NearestNode(unfinishedCrossing[1],others)
                    b,bO=NearestNode(unfinishedCrossing[2],others)
                    newCrossing=Crossing(a,aO,b,bO,unfinishedCrossing[0],IDiter)
                    others[IDiter]=newCrossing
                    IDiter+=1
                    unfinishedCrossing.clear()
            elif e.__dict__['button']==pygame.BUTTON_RIGHT:
                newCrossing=Crossing(0,0,0,0,pos,IDiter,True)
                others[IDiter]=newCrossing
                inputNodes[IDiter]=newCrossing
                inputValues[IDiter]=1
                IDiter+=1
            elif e.__dict__['button']==pygame.BUTTON_WHEELUP:
                a=NearestNode(pos,inputNodes)[0]
                inputValues[a]=not inputValues[a]
    globals()['IDiter']=IDiter

def GetCrossings(a,b):
    return crossings[a].value[b]
def Main(events,screen):
    for i in crossings:
        crossings[i].update(GetCrossings)
    for i in inputNodes:
        inputNodes[i].inputUpdate(inputValues)
    screen.Clear()
    for i in crossings:
        crossings[i].postUpdate()
        crossings[i].Draw(screen,crossings)
    AddCrossing(events,crossings)
    

Screen.Screen().Loop(Main)