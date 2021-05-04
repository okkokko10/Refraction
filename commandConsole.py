
class CommandConsole:
    def __init__(self,commands=None):
        self.text = ['']
        self.selectedLine = 0
        self.selectedIndex = 0
        if commands:
            self.commands=commands
        else:
            self.commands={}

    def InsertLine(self, index, element):
        self.text.insert(index, element)

    def PopLine(self, index):
        self.text.pop(index)

    def InsertString(self, line, index, element):
        self.text[line] = self.text[line][:index] + \
            element+self.text[line][index:]

    def PopString(self, line, indexFrom, indexTo):
        self.text[line] = self.text[line][:indexFrom] + \
            self.text[line][indexTo+1:]

    def TypeText(self, element):
        self.InsertString(self.selectedLine, self.selectedIndex, element)
        self.MoveRight()
    
    def RemoveLineBreak(self,line):
        if line>0:
            self.text[line-1]+=self.text[line]
            self.text.pop(line)

    def InsertLineBreak(self, line, index):
        self.InsertLine(line+1, self.text[line][index:])
        self.text[line] = self.text[line][:index]
        

    def Backspace(self):
        if self.selectedIndex==0:
            if self.selectedLine==0:
                return
            self.MoveLeft()
            self.RemoveLineBreak(self.selectedLine+1)
            return
        self.MoveLeft()
        self.PopString(self.selectedLine, self.selectedIndex, self.selectedIndex)

    def Enter(self):
        self.InsertLineBreak(self.selectedLine, self.selectedIndex)
        self.MoveRight()

    def MoveTo(self, line, index):
        self.selectedIndex = index
        self.selectedLine = line
        self.WarpSelector()

    def MoveUp(self):
        self.selectedLine -= 1
        self.ClampSelector()

    def MoveDown(self):
        self.selectedLine += 1
        self.ClampSelector()

    def MoveLeft(self):
        self.selectedIndex -= 1
        self.WarpSelector()

    def MoveRight(self):
        self.selectedIndex += 1
        self.WarpSelector()

    def GetLine(self, line):
        if self.selectedLine == line:
            return self.text[line][:self.selectedIndex]+'|'+self.text[line][self.selectedIndex:]
        else:
            return self.text[line]

    def WarpSelector(self):
        self.selectedLine %= len(self.text)
        if self.selectedIndex > len(self.text[self.selectedLine]):
            self.selectedIndex = 0
            self.selectedLine += 1
            self.selectedLine %= len(self.text)
        elif self.selectedIndex < 0:
            self.selectedLine -= 1
            self.selectedLine %= len(self.text)
            self.selectedIndex = len(self.text[self.selectedLine])
        self.selectedLine %= len(self.text)

    def ClampSelector(self):
        if self.selectedLine >= len(self.text):
            self.selectedLine = len(self.text)-1
        elif self.selectedLine <= 0:
            self.selectedLine = 0
        if self.selectedIndex > len(self.text[self.selectedLine]):
            self.selectedIndex = len(self.text[self.selectedLine])
        elif self.selectedIndex < 0:
            self.selectedIndex = 0

    def Parse(self):
        return self.ParseLine(self.selectedLine)
    def ParseLine(self,line):
        text = self.text[line]
        if len(text)==0:# or text[0]!='/':
            return False
        words = text.split()
        print(words)
        if words[0] in self.commands:
            if words[1].isnumeric():
                return words[0],int(words[1])

import pygame
class CommandConsoleVisual:
    def __init__(self):
        self.console = CommandConsole()
        self.height = 50
        self.font = pygame.font.Font(None, self.height)
        self.opened = True
        self.commandBuffer=[]
        self.RefreshSurface()

    def RefreshSurface(self):
        self.surface = pygame.Surface(
            (600, self.height*(len(self.console.text))))
        out = []
        color = (0, 0, 200)
        for i in range(len(self.console.text)):
            out.append((self.font.render(self.console.GetLine(
                i), False, color), (0, i*self.height)))
        self.surface.blits(out)

    def BlitTo(self, destination):
        self.surface.set_alpha(50+100*self.opened)
        destination.blit(self.surface, (0, 0))

    def KeydownEvent(self, event):
        key = event.__dict__['key']
        if key == 303:  #pause
            if self.opened:
                self.Close()
            else:
                self.Open()
        elif self.opened:
            self.Write(event)
        self.RefreshSurface()

    def Open(self):
        self.opened = True
        #self.console.Enter()
        return

    def Close(self):
        self.opened = False
        #self.console.Parse()
        return

    def IsLocking(self):
        return self.opened

    def Write(self, event):
        #print(event)
        letter = event.__dict__['unicode']
        key = event.__dict__['key']
        mod = event.__dict__['mod']
        if key == 8:
            self.console.Backspace()
            return
        if key == 13:
            if mod&1:
                a=self.console.Parse()
                if a:
                    self.commandBuffer.append(a)
            else:
                self.console.Enter()
            return
        a = {273: self.console.MoveUp, 275: self.console.MoveRight,
             274: self.console.MoveDown, 276: self.console.MoveLeft}
        if key in a:
            a[key]()
        if letter:
            self.console.TypeText(letter)
            # self.text[-1]+=letter
    def TakeCommandBuffer(self):
        a = self.commandBuffer.copy()
        self.commandBuffer.clear()
        return a
