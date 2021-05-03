import pygame
import pickle
pygame.font.init()

class Wave:
    def __init__(self, default=0):
        self.directions = [False, False, False, False]
        self.incoming = 0
        self.outgoing = 0
        self.oldFacing = set()
        self.facing = set()
        self.default = default

    def AddUpdate(self):
        pass

    def getOutgoing(self):
        return self.outgoing+self.default

    def addIncoming(self, incoming):
        self.incoming += incoming

    def preUpdate(self):
        self.updateFacing()

    def postUpdate(self):
        self.outgoing = self.incoming

    def ToggleDirection(self, direction):
        self.directions[direction] = not self.directions[direction]

    def ChangeDefault(self, amount):
        self.default = max(self.default+amount, 0)

    def getDefault(self):
        return self.default

    def SetDefault(self, value):
        self.default = value

    def updateFacing(self):
        self.oldFacing = self.facing
        out = []
        if self.getOutgoing():
            for i in range(4):
                if self.IsDirectedTowards(i):
                    out.append(
                        vectorInt(directionToVector(i)*self.getOutgoing()))
        self.facing = set(out)

    # def getFacing(self):
    #     return self.facing

    # def getFacingOld(self):
    #     return self.oldFacing

    def getFacingAdded(self):
        return self.facing.difference(self.oldFacing)

    def getFacingRemoved(self):
        return self.oldFacing.difference(self.facing)

    # def turnUp(self):
    #     self.directions = [False, False, False, False]

    def IsDirected(self):
        return True in self.directions

    def IsDirectedTowards(self, direction):
        return self.directions[direction]

    def IsResettable(self):
        return not ((self.IsDirected()) or self.getOutgoing())

    def RotatedDirections(self, amount):
        a = amount % 4
        return self.directions[a:]+self.directions[:a]

    def SetDirections(self, directions):
        self.directions = directions

    def Save(self):
        return self.directions, self.default, self.incoming

    def Load(self, saveState):
        self.directions, self.default, self.incoming = saveState
        self.postUpdate()
        self.preUpdate()

    @staticmethod
    def Loaded(saveState):
        wave = Wave()
        wave.Load(saveState)
        return wave


class WaveArray:
    def __init__(self):
        # self.array.fill(Wave())
        self.selected = pygame.Vector2(0, 0)
        self.updateList = set()
        self.newUpdateList = set()
        self.followSelected = False
        self.updating = True
        self.updatingOnce = False
        self.arrayLimitless = {}
        self.rectSelectA = (0, 0)
        self.rectSelectB = (0, 0)
        self.rectSelectRotation = 0
        self.console = CommandConsole()

    def ResetUnused(self):
        removable = []
        for p in self.arrayLimitless:
            # there might be a bug here if you reset and remove a direction at the same time. Hopefully the second conditional prevents this
            if self.arrayLimitless[p].IsResettable() and not (p in self.newUpdateList):
                removable.append(p)
        for p in removable:
            del self.arrayLimitless[p]

    def AddUpdate(self, p):
        self.newUpdateList.add(vectorInt(p))

    def Update(self, events, screen):
        self.UpdateInputs(events, screen)
        self.UpdateState()

    def UpdateInputs(self, events, screen):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                pos = e.__dict__['pos']
                posS = screen.InverseTransformPos(pos)
                self.SetSelected(vectorInt(posS))

            if e.type == pygame.KEYDOWN:
                self.console.KeydownEvent(e)
                if self.console.IsLocking():
                    return
                # print(e)
                key = e.__dict__['key']
                #   273^    275>    274v    276<
                v = {273: (0, -1), 274: (0, 1), 275: (1, 0), 276: (-1, 0)}
                if key in v:
                    self.MoveSelected(pygame.Vector2(v[key]))
                    #self.selected = pygame.Vector2(self.selected[0]%self.size,self.selected[1]%self.size)
                    if self.followSelected:
                        screen.MoveCamera(pygame.Vector2(v[key]))
                d = {100: 0, 115: 1, 97: 2, 119: 3}  # wasd
                if key in d:
                    self.getWave(self.selected).ToggleDirection(d[key])
                    self.AddUpdate(self.selected)
                u = {114: 1, 102: -1}  # r,f
                if key in u:
                    self.getWave(self.selected).ChangeDefault(u[key])
                    self.AddUpdate(self.selected)
                if key == 99:  # c
                    self.followSelected = not self.followSelected
                if key == 116:  # t
                    screen.ZoomCameraAt(0.5, self.selected)
                if key == 103:  # g
                    screen.ZoomCameraAt(2, self.selected)
                if key == 121:  # y
                    self.updating = not self.updating
                if key == 101:  # e
                    self.updatingOnce = True
                if key == 98:  # b
                    self.CloneSelected()
                if key == 110:  # n
                    self.SetRectSelectA(self.selected)
                if key == 109:  # m
                    self.SetRectSelectB(self.selected)
                if key == 117:  # u
                    self.RotateClone(1)
                if key == 106:  # j
                    self.RotateClone(-1)

                self.ResetUnused()

    def UpdateState(self):
        if self.updating or self.updatingOnce:
            self.updatingOnce = False
            self.updateList = self.newUpdateList.copy()
            self.newUpdateList.clear()
            for p in self.updateList:
                wave = self.getWave(p)
                wave.preUpdate()
                for f in wave.getFacingAdded():
                    p1 = f[0]+p[0], f[1]+p[1]
                    self.getWave(p1).addIncoming(1)
                    self.AddUpdate(p1)
                for f in wave.getFacingRemoved():
                    p1 = f[0]+p[0], f[1]+p[1]
                    self.getWave(p1).addIncoming(-1)
                    self.AddUpdate(p1)

            for p in self.newUpdateList.union(self.updateList):
                self.getWave(p).postUpdate()

    def getWave(self, pos, update=True):
        if update:
            return self.arrayLimitless.setdefault((vectorInt(pos)), Wave())
        else:
            if vectorInt(pos) in self.arrayLimitless:
                return self.arrayLimitless[vectorInt(pos)]

    def SetRectSelectA(self, pos):
        self.rectSelectA = vectorInt(pos)

    def SetRectSelectB(self, pos):
        self.rectSelectB = vectorInt(pos)

    def getRectSelectA(self):
        return self.rectSelectA

    def getRectSelectB(self):
        return self.rectSelectB

    def CloneGroup(self, positions, rotation):
        # positions: list of tuples that have from in index 0 and to in index 1
        out = {}
        for m in positions:
            a = self.getWave(m[0])
            out[m[1]] = a.RotatedDirections(rotation), a.getDefault()
        for v in out:
            a = self.getWave(v)
            a.SetDirections(out[v][0])
            a.SetDefault(out[v][1])
            self.AddUpdate(v)

    def CloneRect(self, pos1, pos2, posTo, rotation):
        changes = []
        if pos1[0] > pos2[0]:
            sx = -1
        else:
            sx = 1
        if pos1[1] > pos2[1]:
            sy = -1
        else:
            sy = 1

        for y in range(abs(pos2[1]-pos1[1])+1):
            for x in range(abs(pos2[0]-pos1[0])+1):
                f = (pos1[0]+sx*x, pos1[1]+sy*y)
                t = vectorInt(pygame.Vector2(
                    posTo)+rotateVector(pygame.Vector2(sx*x, sy*y), rotation))
                #t = (posTo[0]+sx*x, posTo[1]+sy*y)
                changes.append((f, t))
        self.CloneGroup(changes, rotation)

    def CloneSelected(self):
        self.CloneRect(self.getRectSelectA(),
                       self.getRectSelectB(), self.selected, self.rectSelectRotation)

    def RotateClone(self, amount):
        self.rectSelectRotation += amount
        self.rectSelectRotation %= 4

    def SetSelected(self, value):
        self.selected = value

    def GetSelected(self):
        return self.selected

    def MoveSelected(self, value):
        self.selected += pygame.Vector2(value)

    def Save(self):
        out = {}
        for p in self.arrayLimitless:
            out[p] = self.arrayLimitless[p].Save()
        return out  # ,self.newUpdateList.union(self.updateList)

    def Load(self, saveState):
        for p in saveState:
            self.arrayLimitless[p] = Wave.Loaded(saveState[p])
        self.ReloadAll()

    def ReloadAll(self):
        self.newUpdateList = set(self.arrayLimitless.keys())

    @staticmethod
    def Loaded(saveState):
        waveArray = WaveArray()
        waveArray.Load(saveState)
        return waveArray

    def OnQuit(self):
        pass

    def SaveTo(self, filename):
        ToFile(filename, self.Save())

    @staticmethod
    def LoadedFrom(filename):
        return WaveArray.Loaded(FromFile(filename))

    def GetRotatedRectSelectEnd(self):

        return pygame.Vector2(self.selected)
        +rotateVector(
            pygame.Vector2(self.getRectSelectB()) -
            pygame.Vector2(self.getRectSelectA()),
            self.rectSelectRotation)


class Screen:
    def __init__(self, scale, size):
        self.canvas = pygame.display.set_mode(size)
        self.scale = scale
        self.font = pygame.font.Font(None, self.scale)
        self.textDrawBuffer = []
        self.textMemory = {}
        self.textColor = (0, 100, 200)
        self.cameraPos = -pygame.Vector2(1, 1)/2
        self.Resize()
        self.drawSettings = {'text': True,
                             'knobs': True, 'unpoweredKnobs': True}

    def DrawText(self, pos, text, color):
        self.textDrawBuffer.append((pos, text, color))

    def getText(self, text, color):
        return self.textMemory.setdefault((text, color), self.font.render(text, False, color))

    def Resize(self):
        self.size = pygame.Vector2(
            self.canvas.get_width(), self.canvas.get_height())/self.scale

    def getSize(self):
        return self.size

    def Visible(self):
        '''x1,y1,x2,y2'''
        x1, y1 = self.cameraPos
        x2, y2 = self.getSize()
        return int(x1), int(y1), int(x1+x2)+2, int(y1+y2)+2

    def CameraTransformPos(self, position):
        pos = position  # +pygame.Vector2(1,1)/2
        # v=self.getSize()/2
        a = (pos-self.cameraPos)
        c = a*self.scale
        return c

    def InverseTransformPos(self, pos):
        a = pygame.Vector2(pos)/self.scale
        b = self.cameraPos+a
        return b

    def CameraTransformScale(self, position, scale):
        # pos=position+pygame.Vector2(1,1)/2
        # v=self.getSize()/2
        # a=(pos-self.cameraPos)
        #l = (a-v).magnitude()
        return scale*self.scale  # *(5/(l+1))

    def MoveCamera(self, direction):
        self.cameraPos += direction

    def ZoomCameraAt(self, amount, position):
        pos = position  # +pygame.Vector2(1,1)/2
        self.scale *= amount
        self.cameraPos = pos + (self.cameraPos-pos)/amount
        self.Resize()

    def MoveCameraTo(self, pos):
        self.cameraPos = pos

    def actualDrawText(self, i):
        pos, text, color = i
        t = self.getText(text, color)
        posS = self.CameraTransformPos(pos)  # -pygame.Vector2(1,1)/4
        sc = self.CameraTransformScale(pos, 1/2)
        tS = pygame.transform.scale(
            t, (int(sc), int(sc*t.get_height()/t.get_width())))
        self.canvas.blit(tS, posS-sc*pygame.Vector2(1,
                                                    t.get_height()/t.get_width())/2)
        return

    def clearTextBuffer(self):
        self.textDrawBuffer.clear()

    def DrawWaveArray(self, waveArray):
        vx, vy, Vx, Vy = self.Visible()
        self.canvas.lock()
        self.DrawRectSelect(waveArray)
        # TODO: make it so it chooses which one to use based on which one is more efficient
        self.DrawSelector(waveArray.selected)
        # for y in range(vy,Vy):
        #     for x in range(vx,Vx):
        #         self.DrawWave(waveArray.getWave((x,y),False),pygame.Vector2(x,y))
        for p in waveArray.arrayLimitless:
            if vx <= p[0] <= Vx and vy <= p[1] <= Vy:
                self.DrawWave(waveArray.getWave(p, False), p)
        self.canvas.unlock()
        for d in self.textDrawBuffer:
            self.actualDrawText(d)
        self.clearTextBuffer()
        waveArray.console.BlitTo(self.canvas)

    def DrawWave(self, wave, pos):
        if not wave or wave.IsResettable():
            return
        pos = pygame.Vector2(pos)
        color = (100*min(wave.getOutgoing(), 2), 50, 50)
        color2 = (0, 100*min(wave.getDefault(), 2),
                  50*min(wave.getDefault(), 5))
        for i in range(4):
            if wave.IsDirectedTowards(i):
                posEnd = pos+directionToVector(i)/2
                self.tDrawLine(pos, posEnd, color, 1/6)
        if wave.IsDirected():
            self.tDrawCircle(pos, color2, 1/8)
        if wave.getOutgoing() and self.drawSettings['text']:
            color3 = color[1], color[2], color[0]
            self.DrawText(pos, str(wave.getOutgoing()), color3)

    def DrawSelector(self, pos):
        color = (200, 200, 200)
        self.tDrawCircle(pos, color, 1/4)

    def DrawRectSelect(self, waveArray):

        color = (150, 150, 150)
        self.tDrawRect(waveArray.getRectSelectA(),
                       waveArray.getRectSelectB(), color)
        color2 = (170, 170, 170)
        self.tDrawRect(waveArray.GetSelected(),
                       waveArray.GetRotatedRectSelectEnd(), color2)
        self.tDrawCircle(waveArray.getRectSelectA(), color, 1/4)

    def tDrawRect(self, vectorA, vectorB, color):
        vecA = self.CameraTransformPos(vectorA)
        vecB = self.CameraTransformPos(vectorB)
        rect = vectorToRect(vecA, vecB)
        pygame.draw.rect(self.canvas, color, rect)

    def Clear(self):
        self.canvas.fill((100, 100, 100))

    def ChangeSettings(self, setting, value):
        if setting in self.drawSettings:
            self.drawSettings[setting] = value

    def DrawLine(self, A, B, color, width):
        pygame.draw.line(self.canvas, color, vectorInt(A),
                         vectorInt(B), int(width))

    def DrawCircle(self, pos, color, radius):
        pygame.draw.circle(self.canvas, color, vectorInt(pos), int(radius))

    def tDrawLine(self, A, B, color, width):
        self.DrawLine(self.CameraTransformPos(A), self.CameraTransformPos(
            B), color, self.CameraTransformScale(A, width))

    def tDrawCircle(self, pos, color, radius):
        self.DrawCircle(self.CameraTransformPos(pos), color,
                        self.CameraTransformScale(pos, radius))

    def Loop(self, waveArray, timer=200):
        run = True
        while run:
            pygame.time.wait(timer)
            if pygame.event.get(pygame.QUIT):
                run = False
                waveArray.OnQuit()
                return
            e = pygame.event.get()
            waveArray.Update(e, self)
            self.Clear()
            self.DrawWaveArray(waveArray)
            pygame.display.update()

class CommandConsole:
    def __init__(self):
        self.text=['']
        self.opened=False
        self.height = 50
        self.font = pygame.font.Font(None,self.height)
    def KeydownEvent(self,event):
        key = event.__dict__['key']
        if self.opened:
            self.Write(event)
        if key == 13:
            if self.opened:
                self.opened = False
                self.Close()
            else:
                self.opened = True
                self.Open()
    def IsLocking(self):
        return self.opened
    def Write(self,event):
        letter=event.__dict__['unicode']
        self.text[-1]+=letter
        pass
    def Open(self):
        return
    def Close(self):
        self.text.append('')
        return
    def Surface(self):
        surf = pygame.Surface((600,self.height*(len(self.text))))
        surf.set_alpha(100)
        out=[]
        color = (0,0,200)
        for i in range(len(self.text)):
            out.append((self.font.render(self.text[i], False, color),(0,i*self.height)))
        surf.blits(out)
        return surf
    def BlitTo(self,destination):
        destination.blit(self.Surface(),(0,0))
            

def vectorInt(v):
    return (round(v[0]), round(v[1]))


def directionToVector(direction=4):
    return pygame.Vector2([(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)][direction])


def rotateVector(vec, amount):
    return pygame.Vector2(vec).rotate(-amount*90)
    # x,y=vec
    # return pygame.Vector2([(x,y),(-y,x),(-x,-y),(y,-x)][amount%4])


def vectorToRect(vecA, vecB):
    return pygame.Rect(min(vecA[0], vecB[0]), min(vecA[1], vecB[1]), abs(vecA[0]-vecB[0]), abs(vecA[1]-vecB[1]))


def ToFile(filename, data):
    f = open(filename, 'wb')
    pickle.dump(data, f)
    f.close()


def FromFile(filename):
    f = open(filename, 'rb')
    out = pickle.load(f)
    f.close()
    return out


_scale = 60
_timer = 40
_scrSize = 1000, 700
a = WaveArray.LoadedFrom('Wavefile.obj')
S = Screen(_scale, _scrSize)
#S.ChangeSettings('text', False)
#S.ChangeSettings('unpoweredKnobs', False)
S.Loop(a, _timer)
a.SaveTo('Wavefile.obj')
