import numpy as np
import pygame

class Wave:
    def __init__(self,direction=0,default=0):
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
    def __init__(self,size,wrapAround=False):
        self.size=size
        self.array=np.ndarray((size,size),Wave)
        #self.array.fill(Wave())
        self.Reset()
        self.wrapAround=wrapAround
        self.selected=pygame.Vector2(size//2,size//2)
        self.updateList=set()
        self.newUpdateList=set()
    def Reset(self,defaultDirection=4):
        for x in range(self.size):
            for y in range(self.size):
                self.array[x,y]=Wave(defaultDirection)
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
                    self.selected = pygame.Vector2(self.selected[0]%self.size,self.selected[1]%self.size)
                d = {100:0,115:1,97:2,119:3}
                if key in d:
                    selWave.ToggleDirection(d[key])
                    self.AddUpdate(self.selected[0],self.selected[1])
                u = {114:1,102:-1}
                if key in u:
                    selWave.ChangeDefault(u[key])
                    self.AddUpdate(self.selected[0],self.selected[1])
        self.updateList=self.newUpdateList.copy()
        self.newUpdateList.clear()
        # for y in range(self.size):
        #     for x in range(self.size):
        #print(self.updateList)
        for x,y in self.updateList:
                wave = self.getWave((x,y))
                s = int(self.getWave((x,y)).getOutgoing())
                if s>0 and False:
                    for i in range(4):
                        if self.array[x,y].directions[i]:
                            v = Wave.Vector(i)
                            x1=x+v[0]*s
                            y1=y+v[1]*s
                            if self.wrapAround:
                                x1%=self.size
                                y1%=self.size
                            if 0<=x1<self.size and 0<=y1<self.size:
                                self.array[int(x1),int(y1)].addIncoming(1)
                
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

        # for y in self.array:
        #     for x in y:
        #         x.postUpdate()
        for p in self.newUpdateList.union(self.updateList):
            self.array[p[0],p[1]].postUpdate()
    def getWave(self,pos):
        return self.array[int(pos[0]%self.size),int(pos[1])%self.size]


    
class Screen:
    def __init__(self,scale,size):
        self.canvas=pygame.display.set_mode((size,size))
        self.scale = scale
        pygame.font.init()
        self.font=pygame.font.Font(None,self.scale)
        self.textDrawBuffer=[]
        self.textMemory={}
        self.textColor=(0,100,200)
    def DrawText(self,pos,text,color):
        self.textDrawBuffer.append((pos,text,color))
    def getText(self,text,color):
        return self.textMemory.setdefault((text,color),self.font.render(text, False, color))
    def actualDrawText(self,i):
        pos,text,color = i
        t=self.getText(text,color)
        posS=(pos+pygame.Vector2(1,1)/4)*self.scale
        self.canvas.blit(t,posS)
        return
    def clearTextBuffer(self):
        self.textDrawBuffer.clear()
    def DrawWaveArray(self,waveArray):
        self.canvas.lock()
        self.DrawSelector(waveArray.selected)
        for y in range(waveArray.size):
            for x in range(waveArray.size):
                self.DrawWave(waveArray.array[x,y],pygame.Vector2(x,y))
        self.canvas.unlock()
        for d in self.textDrawBuffer:
            self.actualDrawText(d)
        self.clearTextBuffer()
    def DrawWave(self,wave,pos):
        posS=(pos+pygame.Vector2(1/2,1/2))*self.scale
        color=(100*min(wave.getValue(),2),50,50)
        color2=(0,100*min(wave.getDefault(),2),50*min(wave.getDefault(),5))
        for i in range(4):
            if wave.directions[i]:
                diff=Wave.Vector(i)*self.scale//2
                pygame.draw.line(self.canvas,color,posS,posS+diff//1,self.scale//6)
        pygame.draw.circle(self.canvas,color2,(int(posS.x),int(posS.y)),self.scale//8)
        if wave.getOutgoing():
            self.DrawText(pos, str(wave.getOutgoing()), color)
    def DrawSelector(self,pos):
        posS=(pos+pygame.Vector2(1/2,1/2))*self.scale
        color=(200,200,200)
        pygame.draw.circle(self.canvas,color,(int(posS[0]),int(posS[1])),self.scale//4)
    def Clear(self):
        self.canvas.fill((100,100,100))
    

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



scale = 60
height = 15
timer = 40
a = WaveArray(height,True)
Screen(scale,scale*height).Loop(a,timer)