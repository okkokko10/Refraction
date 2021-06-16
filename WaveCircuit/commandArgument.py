#   trying to make a console command parser, and maker.


'functionStart {str}',
'functionEnd',
'function {str}',
'if {bool} {command}',
'modifyword {int fromLine} {int fromWord} {int toLine} {int toWord}',
'setnode {int} {int} {int x if 0<=x<=3} {bool}',
'getnode {int} {int} {int x if 0<=x<=3} {result}',
'setdefault {int} {int} {int}',
'getdefault {int} {int} {result}'

[
    [
        'setnode','1','2','1','True'
    ],
    [
        ''
    ]
]

class AffectedConverterBase:
    def __init__(self,affected):
        self.affected=affected
    def getdefault(self,x,y):
        return str(0)
    def setdefault(self,x,y,value):
        pass
    def getvalue(self,x,y):
        return str(0)

class Command:
    def __init__(self,stringList,affected):
        self.commands={
            'if':Command.command_if,
            'modifyword':Command.command_modifyword
        }
        self.stringList=stringList
        self.affected=affected
    def Parse(self,line,word=0):
        s=self.stringList[line]
        if not s:
            return
        if s[word] in self.commands.keys():
            self.commands[s[word]](self,line,word)
    def AddCommands(self,commandDict):
        self.commands.update(commandDict)
    @staticmethod
    def command_if(self,line,word):
        l=self.stringList[line]
        if l[word+1]!='0':
            self.Parse(line,word+2)
    @staticmethod
    def command_modifyword(self,line,word):
        l=self.stringList[line]
        fl,fw,tl,tw=[int(l[word+1+i]) for i in range(4)]
        o = self.GetWord(fl,fw)
        self.SetWord(tl,tw,o)

    def GetWord(self,line,word):
        return self.stringList[line][word]
    def SetWord(self,line,word,value):
        self.stringList[line][word]=value
    def view(self):
        r = ''
        for line in self.stringList:
            for word in line:
                r+=word+' '
            r+='\n'
        return r
    def Execute(self):
        for i in range(len(self.stringList)):
            self.Parse(i)


def command_getdefault(self,line,word):
    l=self.stringList[line]
    l[word+3] = self.affected.getdefault(l[word+1],l[word+2])
def command_setdefault(self,line,word):
    l=self.stringList[line]
    self.affected.setdefault(l[word+1],l[word+2],l[word+3])
def command_getvalue(self,line,word):
    l=self.stringList[line]
    l[word+3] = self.affected.getvalue(l[word+1],l[word+2])
def command_getselected(self,line,word):
    l=self.stringList[line]
    l[word+1],l[word+2] = self.affected.getselected()

class WavesConverter(AffectedConverterBase):
    def getdefault(self, x, y):
        X,Y=int(x),int(y)
        return str(self.affected.getWave((X,Y)).getDefault())
    def setdefault(self, x, y, value):
        X,Y=int(x),int(y)
        self.affected.getWave((X,Y)).setDefault(int(value))
        self.affected.AddUpdate((X,Y))
    def getvalue(self, x, y):
        X,Y=int(x),int(y)
        return str(self.affected.getWave((X,Y)).getOutgoing())
    def getselected(self):
        x,y=self.affected.selected
        X,Y=int(x),int(y)
        return str(X),str(Y)
def commandConsoleExecute(self:Command,cc):
    self.stringList=[]
    for l in cc.text:
        self.stringList.append(l.split())
    self.Execute()
    cc.text=[]
    for l in self.stringList:
        cc.text.append('')
        for w in l:
            cc.text[-1]+=w+' '

def CreateWaves(waves):
    wc=WavesConverter(waves)
    c=Command([],wc)
    c.AddCommands({
    'getdefault':command_getdefault,
    'setdefault':command_setdefault,
    'getvalue':command_getvalue,
    'getselected':command_getselected})
    cons=waves.console.console
    def ex():
        if not waves.console.IsLocking():
            commandConsoleExecute(c,cons)
            waves.console.RefreshSurface()
    waves.UpdateHook=ex
