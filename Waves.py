import numpy as np
import pygame

class Wave:
    def __init__(self,default=0):
        self.directions=[False,False,False,False]
        self.incoming=0
        self.value=0
        self.outgoing=0
        self.oldFacing=set()
        self.facing=set()
        self.default=default
        self.updated=True
        self.resettable=False
    def AddUpdate(self):
        self.updated=True
    def getOutgoing(self):
        return self.outgoing+self.default
    def addIncoming(self,incoming):
        self.incoming += incoming
    def preUpdate(self):
        self.updateFacing()
        pass
    def postUpdate(self):
        self.outgoing=self.incoming
        #self.incoming=self.default
        self.value=self.getOutgoing()
        self.updated=False
        pass
    def getValue(self):
        return max(0,self.value)
    def ToggleDirection(self,direction):
        self.directions[direction]= not self.directions[direction]
    def ChangeDefault(self,amount):
        self.AddUpdate()
        #self.incoming+=amount
        self.default=max(self.default+amount,0)
    def getDefault(self):
        return self.default
    def setDefault(self,value):
        self.default=value
    def getOld(self):
        return self.old
    def updateFacing(self):
        self.oldFacing=self.facing
        out=[]
        if self.getOutgoing():
            for i in range(4):
                if self.IsDirectedTowards(i):
                    out.append(vectorInt(directionToVector(i)*self.getOutgoing()))
        self.facing=set(out)
    def getFacing(self):
        return self.facing
    def getFacingOld(self):
        return self.oldFacing
    def getFacingAdded(self):
        return self.facing.difference(self.oldFacing)
    def getFacingRemoved(self):
        return self.oldFacing.difference(self.facing)
    def turnUp(self):
        self.directions=[False,False,False,False]
    def IsDirected(self):
        return True in self.directions
    def IsDirectedTowards(self,direction):
        return self.directions[direction]
    def IsResettable(self):
        return not ((self.IsDirected()) or self.getOutgoing())
    def RotatedDirections(self,amount):
        a=amount%4
        return self.directions[a:]+self.directions[:a]
    def SetDirections(self,directions):
        self.directions=directions
        self.AddUpdate()
    
class WaveArray:
    def __init__(self):
        #self.array.fill(Wave())
        self.selected=pygame.Vector2(0,0)
        self.updateList=set()
        self.newUpdateList=set()
        self.followSelected=False
        self.updating=True
        self.updatingOnce=False
        self.arrayLimitless={}
        self.rectSelectA=(0,0)
        self.rectSelectB=(0,0)

    def ResetUnused(self):
        removable=[]
        for p in self.arrayLimitless:
            if self.arrayLimitless[p].IsResettable() and not (p in self.newUpdateList):#there might be a bug here if you reset and remove a direction at the same time. Hopefully the second conditional prevents this
                removable.append(p)
        for p in removable:
            del self.arrayLimitless[p]
    def AddUpdate(self,p):
        
        self.newUpdateList.add(vectorInt(p))
        self.getWave(vectorInt(p)).AddUpdate()
    def Update(self,events,screen):
        for e in events:
            # if e.type == pygame.MOUSEBUTTONDOWN:
                #     print(e)
                #     pos=e.__dict__['pos']
                #     pos= pos[0]//screen.scale,pos[1]//screen.scale
                #     button=e.__dict__['button']
                #     wave=self.array[pos[0],pos[1]]
                #     if button==1:
                #         wave.Rotate(1)
                #     elif button==3:
                #         wave.Rotate(-1)
                #     elif button==4:#up
                #         wave.ChangeDefault(1)
                #     elif button==5:#down
                #         wave.ChangeDefault(-1)
                #     elif button==6:#disable
                #         wave.turnUp()
            if e.type == pygame.KEYDOWN:
                #print(e)
                key = e.__dict__['key']
                #   273^    275>    274v    276<
                v={273:(0,-1),274:(0,1),275:(1,0),276:(-1,0)}
                if key in v:
                    self.selected+=pygame.Vector2(v[key])
                    #self.selected = pygame.Vector2(self.selected[0]%self.size,self.selected[1]%self.size)
                    if self.followSelected:
                        screen.MoveCamera(pygame.Vector2(v[key]))
                d = {100:0,115:1,97:2,119:3}#wasd
                if key in d:
                    self.getWave(self.selected).ToggleDirection(d[key])
                    self.AddUpdate(self.selected)
                u = {114:1,102:-1}#r,f
                if key in u:
                    self.getWave(self.selected).ChangeDefault(u[key])
                    self.AddUpdate(self.selected)
                if key==99:#c
                    self.followSelected = not self.followSelected
                if key==116:#t
                    screen.ZoomCameraAt(0.5,self.selected)
                if key==103:#g
                    screen.ZoomCameraAt(2,self.selected)
                if key==121:#y
                    self.updating=not self.updating
                if key==101:#e
                    self.updatingOnce=True
                if key==98:#b
                    self.CloneSelected()
                if key==110:#n
                    self.SetRectSelectA(self.selected)
                if key==109:#m
                    self.SetRectSelectB(self.selected)
                self.ResetUnused()
        if self.updating or self.updatingOnce:
            self.updatingOnce=False
            self.updateList=self.newUpdateList.copy()
            self.newUpdateList.clear()
            for p in self.updateList:
                    wave = self.getWave(p)
                    s = int(self.getWave(p).getOutgoing())

                    wave.preUpdate()
                    for f in wave.getFacingAdded():
                        p1=f[0]+p[0],f[1]+p[1]
                        self.getWave(p1).addIncoming(1)
                        self.AddUpdate(p1)
                    for f in wave.getFacingRemoved():
                        p1=f[0]+p[0],f[1]+p[1]
                        self.getWave(p1).addIncoming(-1)
                        self.AddUpdate(p1)

            for p in self.newUpdateList.union(self.updateList):
                self.getWave(p).postUpdate()
    def getWave(self,pos,update=True):
        if update:
            return self.arrayLimitless.setdefault((vectorInt(pos)),Wave())
        else:
            if vectorInt(pos) in self.arrayLimitless:
                return self.arrayLimitless[vectorInt(pos)]
    def SetRectSelectA(self,pos):
        self.rectSelectA=vectorInt(pos)
    def SetRectSelectB(self,pos):
        self.rectSelectB=vectorInt(pos)
    def getRectSelectA(self):
        return self.rectSelectA
    def getRectSelectB(self):
        return self.rectSelectB
    def CloneGroup(self,positions,rotation):
        #positions: list of tuples that have from in index 0 and to in index 1
        out={}
        for m in positions:
            a=self.getWave(m[0])
            out[m[1]]=a.RotatedDirections(rotation),a.getDefault()
        for v in out:
            a=self.getWave(v)
            a.SetDirections(out[v][0])
            a.setDefault(out[v][1])
            self.AddUpdate(v)

    def CloneRect(self,pos1,pos2,posTo):
        changes=[]
        if pos1[0]>pos2[0]:
            sx=-1
        else:
            sx=1
        if pos1[1]>pos2[1]:
            sy=-1
        else:
            sy=1

        for y in range(abs(pos2[1]-pos1[1])+1):
            for x in range(abs(pos2[0]-pos1[0])+1):
                f=(pos1[0]+sx*x,pos1[1]+sy*y)
                t=(posTo[0]+sx*x,posTo[1]+sy*y)
                changes.append((f,t))
        self.CloneGroup(changes, 0)
        pass
    def CloneSelected(self):
        self.CloneRect(self.getRectSelectA(), self.getRectSelectB(), self.selected)

    
class Screen:
    def __init__(self,scale,size):
        self.canvas=pygame.display.set_mode(size)
        self.scale = scale
        pygame.font.init()
        self.font=pygame.font.Font(None,self.scale)
        self.textDrawBuffer=[]
        self.textMemory={}
        self.textColor=(0,100,200)
        self.cameraPos=-pygame.Vector2(1,1)/2
        self.Resize()
        self.drawSettings={'text':True,'knobs':True,'unpoweredKnobs':True}
    def DrawText(self,pos,text,color):
        self.textDrawBuffer.append((pos,text,color))
    def getText(self,text,color):
        return self.textMemory.setdefault((text,color),self.font.render(text, False, color))
    def Resize(self):
        self.size = pygame.Vector2(self.canvas.get_width(),self.canvas.get_height())/self.scale
    def getSize(self):
        return self.size
    def Visible(self):
        '''x1,y1,x2,y2'''
        x1,y1=self.cameraPos
        x2,y2=self.getSize()
        return int(x1),int(y1),int(x1+x2)+2,int(y1+y2)+2
    def CameraTransformPos(self,position):
        pos=position#+pygame.Vector2(1,1)/2
        #v=self.getSize()/2
        a=(pos-self.cameraPos)
        c=a*self.scale
        return c
    def CameraTransformScale(self,position,scale):
        #pos=position+pygame.Vector2(1,1)/2
        #v=self.getSize()/2
        #a=(pos-self.cameraPos)
        #l = (a-v).magnitude()
        return scale*self.scale#*(5/(l+1))
    def MoveCamera(self,direction):
        self.cameraPos+=direction
    def ZoomCameraAt(self,amount,position):
        pos = position#+pygame.Vector2(1,1)/2
        self.scale*=amount
        self.cameraPos = pos + (self.cameraPos-pos)/amount
        self.Resize()
    def MoveCameraTo(self,pos):
        self.cameraPos=pos
    def actualDrawText(self,i):
        pos,text,color = i
        t=self.getText(text,color)
        posS=self.CameraTransformPos(pos)#-pygame.Vector2(1,1)/4
        sc=self.CameraTransformScale(pos, 1/2)
        tS=pygame.transform.scale(t,(int(sc),int(sc*t.get_height()/t.get_width())))
        self.canvas.blit(tS,posS-sc*pygame.Vector2(1,t.get_height()/t.get_width())/2)
        return
    def clearTextBuffer(self):
        self.textDrawBuffer.clear()
    def DrawWaveArray(self,waveArray):
        vx,vy,Vx,Vy=self.Visible()
        self.canvas.lock()
        self.DrawRectSelect(waveArray)
        self.DrawSelector(waveArray.selected)   #TODO: make it so it chooses which one to use based on which one is more efficient
        # for y in range(vy,Vy):
        #     for x in range(vx,Vx):
        #         self.DrawWave(waveArray.getWave((x,y),False),pygame.Vector2(x,y))
        for p in waveArray.arrayLimitless:
            if vx<=p[0]<=Vx and vy<=p[1]<=Vy:
                self.DrawWave(waveArray.getWave(p,False),p)
        self.canvas.unlock()
        for d in self.textDrawBuffer:
            self.actualDrawText(d)
        self.clearTextBuffer()
    def DrawWave(self,wave,pos):
        if not wave or wave.IsResettable():
            return
        pos=pygame.Vector2(pos)
        posS=self.CameraTransformPos(pos)
        color=(100*min(wave.getValue(),2),50,50)
        color2=(0,100*min(wave.getDefault(),2),50*min(wave.getDefault(),5))
        for i in range(4):
            if wave.IsDirectedTowards(i):
                posEnd=self.CameraTransformPos(pos+directionToVector(i)/2)
                self.DrawLine(posS, posEnd, color, self.CameraTransformScale(pos, 1/6))
        if wave.IsDirected():
            self.DrawCircle(posS, color2, self.CameraTransformScale(pos,1/8))
        if wave.getOutgoing() and self.drawSettings['text']:
            color3 =color[1],color[2],color[0]
            self.DrawText(pos, str(wave.getOutgoing()), color3)
    def DrawSelector(self,pos):
        posS=self.CameraTransformPos(pos)
        color=(200,200,200)
        self.DrawCircle(posS, color, self.CameraTransformScale(pos, 1/4))
    def DrawRectSelect(self,waveArray):
        color=(150,150,150)
        vecA=self.CameraTransformPos( waveArray.getRectSelectA() )
        vecB=self.CameraTransformPos( waveArray.getRectSelectB() )
        rect = vectorToRect(vecA, vecB)
        pygame.draw.rect(self.canvas,color,rect)
        pass
    def Clear(self):
        self.canvas.fill((100,100,100))
    def ChangeSettings(self,setting,value):
        if setting in self.drawSettings:
            self.drawSettings[setting]=value
    def DrawLine(self,A,B,color,width):
        pygame.draw.line(self.canvas,color,vectorInt(A),vectorInt(B),int(width))
    def DrawCircle(self,pos,color,radius):
        pygame.draw.circle(self.canvas,color,vectorInt(pos),int(radius))

    def Loop(self,waveArray,timer=200):
        run=True
        while run:
            pygame.time.wait(timer)
            if pygame.event.get(pygame.QUIT):
                run=False
                return
            e=pygame.event.get()
            waveArray.Update(e,self)
            self.Clear()
            self.DrawWaveArray(waveArray)
            pygame.display.update()


def vectorInt(v):
    return (int(v[0]),int(v[1]))
def directionToVector(direction=4):
    return pygame.Vector2([(1,0),(0,1),(-1,0),(0,-1),(0,0)][direction])
def rotateVector(vec,amount):
    return pygame.Vector2(vec).rotate(amount*90)
    # x,y=vec
    # return pygame.Vector2([(x,y),(-y,x),(-x,-y),(y,-x)][amount%4])
def vectorToRect(vecA,vecB):
    return pygame.Rect(min(vecA[0],vecB[0]),min(vecA[1],vecB[1]),abs(vecA[0]-vecB[0]),abs(vecA[1]-vecB[1]))
    

_scale = 60
_timer = 40
_scrSize =800,700
a = WaveArray()
S=Screen(_scale,_scrSize)
#S.ChangeSettings('text', False)
#S.ChangeSettings('unpoweredKnobs', False)
S.Loop(a,_timer)