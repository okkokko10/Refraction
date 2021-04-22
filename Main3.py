class Node:
    ID:int
    gates:dict
    def __init__(self,ID):
        self.ID=ID
class Signal:
    value:int
class Gate:
    ID:int
    node:Node
    link:Link
    signal:Signal
    def Connect(self,other):
        pass
        
class Link:
    ID:int
    gates:dict
    signal:Signal
    def __init__(self,ID,gate):
        self.ID
        self.gates={gate.ID:gate}
    def Merge(self,other):
        self.gates.update(other.gates)
        other.Secede(self)
    def Secede(self,other):
        for g in self.gates:
            self.gates[g].link=other
    # I was going to make this so when you connect node A to node B while 
    # node B is connected to node C, node A would also get connected to node C.
    # this would be a pain in the ass to use, so I won't do it

class Circuit:
    nodes:dict

