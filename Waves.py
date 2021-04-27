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
    def AddUpdate(self):
        self.updated=True
    def ResolveUpdate(self):
        if self.updated:
            self.updated=False
            return True
        else:
            return False
    @staticmethod
    def Vector(direction=4):
        return pygame.Vector2([(1,0),(0,1),(-1,0),(0,-1),(0,0)][direction])
    def getOutgoing(self):
        return self.outgoing+self.default
    def addIncoming(self,incoming):
        self.incoming += incoming
    def preUpdate(self):
        self.updateFacing()
        self.updated=False
        pass
    def postUpdate(self):
        self.outgoing=self.incoming
        #self.incoming=self.default
        self.value=self.getOutgoing()
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
    def getOld(self):
        return self.old
    def updateFacing(self):
        self.oldFacing=self.facing
        out=[]
        if self.getOutgoing():
            for i in range(4):
                if self.directions[i]:
                    out.append(tuple(Wave.Vector(i)*self.getOutgoing()))
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
class WaveArray:
    def __init__(self,size,wrapAround=False,limitless=False):
        self.size=size
        #self.array.fill(Wave())
        self.wrapAround=wrapAround
        self.selected=pygame.Vector2(0,0)
        self.updateList=set()
        self.newUpdateList=set()
        self.followSelected=False
        self.updating=True
        self.updatingOnce=False
        self.limitless=limitless
        if limitless:
            self.ResetLimitless()
        else:
            self.Reset()
    def Reset(self,defaultDirection=4):
        self.array=np.ndarray((self.size,self.size),Wave)
        for x in range(self.size):
            for y in range(self.size):
                self.array[x,y]=Wave()
    def ResetLimitless(self):
        self.arrayLimitless={}
    def __str__(self):
        out=''
        for y in self.array:
            for x in y:
                out+=str(x)+' '
            out+='\n'
        return out
    def AddUpdate(self,x,y):
        x=int(x)
        y=int(y)
        self.newUpdateList.add((x,y))
        self.getWave((x,y)).AddUpdate()
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
                selWave=self.getWave(self.selected)
                v={273:(0,-1),274:(0,1),275:(1,0),276:(-1,0)}
                if key in v:
                    self.selected+=pygame.Vector2(v[key])
                    #self.selected = pygame.Vector2(self.selected[0]%self.size,self.selected[1]%self.size)
                    if self.followSelected:
                        screen.MoveCamera(pygame.Vector2(v[key]))
                d = {100:0,115:1,97:2,119:3}
                if key in d:
                    selWave.ToggleDirection(d[key])
                    self.AddUpdate(self.selected[0],self.selected[1])
                u = {114:1,102:-1}
                if key in u:
                    selWave.ChangeDefault(u[key])
                    self.AddUpdate(self.selected[0],self.selected[1])
                if key==99:
                    self.followSelected = not self.followSelected
                if key==116:#t
                    screen.ZoomCameraAt(0.5,self.selected)
                if key==103:#g
                    screen.ZoomCameraAt(2,self.selected)
                if key==121:#y
                    self.updating=not self.updating
                if key==104:#h
                    self.updatingOnce=True
        if self.updating or self.updatingOnce:
            self.updatingOnce=False
            self.updateList=self.newUpdateList.copy()
            self.newUpdateList.clear()
            for x,y in self.updateList:
                    wave = self.getWave((x,y))
                    s = int(self.getWave((x,y)).getOutgoing())

                    wave.preUpdate()
                    for f in wave.getFacingAdded():
                        x1=int(f[0]+x)
                        y1=int(f[1]+y)
                        self.getWave((x1,y1)).addIncoming(1)
                        self.AddUpdate(x1,y1)
                    for f in wave.getFacingRemoved():
                        x1=int(f[0]+x)
                        y1=int(f[1]+y)
                        self.getWave((x1,y1)).addIncoming(-1)
                        self.AddUpdate(x1,y1)

            for p in self.newUpdateList.union(self.updateList):
                self.getWave(p).postUpdate()
    def getWave(self,pos,update=True):
        if self.limitless:
            if update:
                return self.arrayLimitless.setdefault((vectorInt(pos)),Wave())
            else:
                if vectorInt(pos) in self.arrayLimitless:
                    return self.arrayLimitless[vectorInt(pos)]
        # if (0<=pos[0]<self.size and 0<=pos[1]<self.size) or wrapAround:
        #     return self.array[int(pos[0]%self.size),int(pos[1])%self.size]
        # else:
        #     return False


    
class Screen:
    def __init__(self,scale,size):
        self.canvas=pygame.display.set_mode(size)
        self.scale = scale
        pygame.font.init()
        self.font=pygame.font.Font(None,self.scale)
        self.textDrawBuffer=[]
        self.textMemory={}
        self.textColor=(0,100,200)
        self.cameraPos=pygame.Vector2(0,0)
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
        return int(x1),int(y1),int(x2)+2,int(y2)+2
    def CameraTransformPos(self,position):
        pos=position+pygame.Vector2(1,1)/2
        #v=self.getSize()/2
        a=(pos-self.cameraPos)
        c=a*self.scale
        return c
    def CameraTransformScale(self,position,scale):
        pos=position+pygame.Vector2(1,1)/2
        #v=self.getSize()/2
        #a=(pos-self.cameraPos)
        #l = (a-v).magnitude()
        return scale*self.scale#*(5/(l+1))
    def MoveCamera(self,direction):
        self.cameraPos+=direction
    def ZoomCameraAt(self,amount,position):
        pos = position+pygame.Vector2(1,1)/2
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
        vis=self.Visible()
        self.canvas.lock()
        self.DrawSelector(waveArray.selected)
        for y in range(vis[1],vis[1]+vis[3]):
            for x in range(vis[0],vis[0]+vis[2]):
                self.DrawWave(waveArray.getWave((x,y),False),pygame.Vector2(x,y))
        self.canvas.unlock()
        for d in self.textDrawBuffer:
            self.actualDrawText(d)
        self.clearTextBuffer()
    def DrawWave(self,wave,pos):
        if not wave:
            return
        posS=self.CameraTransformPos(pos)
        color=(100*min(wave.getValue(),2),50,50)
        color2=(0,100*min(wave.getDefault(),2),50*min(wave.getDefault(),5))
        for i in range(4):
            if wave.directions[i]:
                posEnd=self.CameraTransformPos(pos+Wave.Vector(i)/2)
                self.DrawLine(posS, posEnd, color, self.CameraTransformScale(pos, 1/6))
        if self.drawSettings['unpoweredKnobs'] or wave.getOutgoing():
            self.DrawCircle(posS, color2, self.CameraTransformScale(pos, #wave.getOutgoing()*
            1/8))
        if wave.getOutgoing() and self.drawSettings['text']:
            color3 =color[1],color[2],color[0]
            self.DrawText(pos, str(wave.getOutgoing()), color3)
    def DrawSelector(self,pos):
        posS=self.CameraTransformPos(pos)
        color=(200,200,200)
        self.DrawCircle(posS, color, self.CameraTransformScale(pos, 1/4))
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
            e=pygame.event.get()
            waveArray.Update(e,self)
            self.Clear()
            self.DrawWaveArray(waveArray)
            pygame.display.update()


def vectorInt(v):
    return (int(v[0]),int(v[1]))

_scale = 60
_height = 30
_timer = 40
_scrSize =800,700
a = WaveArray(_height,True,True)
S=Screen(_scale,_scrSize)
#S.ChangeSettings('text', False)
#S.ChangeSettings('unpoweredKnobs', False)
S.Loop(a,_timer)