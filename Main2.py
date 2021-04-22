import pygame
import Screen


class Node:
    """
    ID: id of the node

    pos: visual position of the node

    A,B: ID's of nodes connected to the input, 0 for none

    As,Bs: which outputs of the nodes are connected to inputs

    inputNode: what external input channel the node follows. 0 for none

    Ao,Bo: IDs of nodes connected to the outputs

    updated: has its value changed

    Av,Bv: values that are output 

    Ai,Bi: values that are input
    """
    ID: int
    pos: pygame.Vector2
    A = 0
    As = False
    B = 0
    Bs = False
    inputNode = 0
    Ao: list
    Bo: list
    updated = False
    Av = 0
    Bv = 0
    Ai = 0
    Bi = 0

    def __init__(self, ID, pos):
        self.ID = ID
        self.Ao = []
        self.Bo = []
        self.pos = pos


class NodeBoard:
    nodes: dict
    _idIter = 0
    def __init__(self):
        self.nodes={}

    def IDiter(self):
        self._idIter += 1
        return self._idIter

    def nodeGUI_Pos(self, nodeID):
        return self.nodes[nodeID].pos

    def nodeGUI_DistanceSq(self, nodeID, pos):
        return (self.nodeGUI_Pos(nodeID)-pos).magnitude_squared()

    def nodeGUI_NearestQuadrant(self, nodeID, pos):
        difference = self.nodeGUI_Pos(nodeID)-pos
        return (difference.x > 0)+2*(difference.y > 0)
        #   0,1
        #  2,3
        #  n&2=y,n&1=x

    def nodeGUI_QuadrantPos(self, nodeID, quadrant):
        diff = -pygame.Vector2((quadrant & 1)*2-1, (quadrant & 2)-1)
        return self.nodeGUI_Pos(nodeID)+diff*20

    def nodeGUI_NearestNode(self, pos):
        if len(self.nodes)==0:
            return 0
        else:
            return sorted(self.nodes.keys(), key=lambda x: self.nodeGUI_DistanceSq(x, pos))[0]


    def link_DetachLink(self, emitterID, emitterQuadrant, receiverID, receiverQuadrant):
        """ detaches the link between specified emitter and receiver nodes """
        # emitter side
        if emitterQuadrant & 2 == 0:
            self.nodes[emitterID].Ao.remove(receiverID)
        else:
            self.nodes[emitterID].Bo.remove(receiverID)
        # receiver side
        if receiverQuadrant & 2 == 0:
            self.nodes[receiverID].A = 0
        else:
            self.nodes[receiverID].B = 0
        return

    def link_DetachReceiver(self, receiverID, receiverQuadrant):
        """ detaches the link received by the node \n
        determines the emitter of the link and calls link_DetachLink with it and the receiver """
        emitterID = self.nodes[receiverID].A
        emitterQuadrant = self.nodes[receiverID].As * 2
        if emitterID == 0:
            return False
        else:
            self.link_DetachLink(emitterID, emitterQuadrant,
                                 receiverID, receiverQuadrant)
            return True

    def link_GetLinks(self, emitterID, emitterQuadrant, receiverID):
        """gets the quadrants of the receiver connected to the emitter's quadrant"""
        out = []
        rec = self.nodes[receiverID]
        side = bool(emitterQuadrant & 2)
        if rec.A == emitterID and rec.As == side:
            out.append(0)
        if rec.B == emitterID and rec.Bs == side:
            out.append(2)
        return out
    
    def link_DetachEmitter(self, emitterID, emitterQuadrant):
        """detaches all links connected to the emitter's quadrant \n
        calls link_DetachLink with all receivers connected to the quadrant"""
        o = []
        if emitterQuadrant & 2 == 0:
            o = self.nodes[emitterID].Ao
        else:
            o = self.nodes[emitterID].Bo
        for receiverID in o:
            for receiverQuadrant in self.link_GetLinks(emitterID, emitterQuadrant, receiverID):
                self.link_DetachLink(
                    emitterID, emitterQuadrant, receiverID, receiverQuadrant)
        return

    def link_AttachLink(self, emitterID, emitterQuadrant, receiverID, receiverQuadrant):
        """ creates a link between specified emitter and receiver nodes"""
        # receiver can only have one emitter
        self.link_DetachReceiver(receiverID, receiverQuadrant)

        # emitter side
        if emitterQuadrant & 2 == 0:
            self.nodes[emitterID].Ao.append(receiverID)
        else:
            self.nodes[emitterID].Bo.append(receiverID)
        # receiver side
        if receiverQuadrant & 2 == 0:
            self.nodes[receiverID].A = emitterID
            self.nodes[receiverID].As = bool(emitterQuadrant & 2)
        else:
            self.nodes[receiverID].B = emitterID
            self.nodes[receiverID].Bs = bool(emitterQuadrant & 2)

    def link_CreateLink(self, nodeA, quadrantA, nodeB, quadrantB):
        """creates a link between two nodes \n
        determines which one is the emitter and which one is the receiver, and calls link_AttachLink with them \n
        returns True if a link is successfully created, False otherwise"""
        if quadrantA & 1 == 0 and quadrantB & 1 == 1:
            #B is emitter, A is receiver
            self.link_AttachLink(nodeB, quadrantB, nodeA, quadrantA)
        elif quadrantA & 1 == 1 and quadrantB & 1 == 0:
            #A is emitter, B is receiver
            self.link_AttachLink(nodeA, quadrantA, nodeB, quadrantB)
        else:
            return False
        return True
    
    def link_DetachQuadrant(self,nodeID,nodeQuadrant):
        if nodeQuadrant & 1:
            self.link_DetachEmitter(nodeID,nodeQuadrant)
        else:
            self.link_DetachReceiver(nodeID,nodeQuadrant)
    def link_DetachCompletely(self,nodeID):
        """removes all links connected to the node"""
        for i in 0,2:
            self.link_DetachReceiver(nodeID,i)
        for i in 1,3:
            self.link_DetachEmitter(nodeID,i)
        return
    def link_GetReceiverLink(self,receiverID,receiverQuadrant):
        if receiverQuadrant&2==0:
            return self.nodes[receiverID].A,self.nodes[receiverID].As*2+1
        else:
            return self.nodes[receiverID].B,self.nodes[receiverID].Bs*2+1

    def node_CreateEmpty(self, pos):
        n = Node(self.IDiter(), pos)
        return n

    def node_RemoveNode(self,nodeID):
        self.link_DetachCompletely(nodeID)
        del self.nodes[nodeID]
    def node_QuadrantValue(self,nodeID,nodeQuadrant):
        n = self.nodes[nodeID]
        return [n.Ai,n.Av,n.Bi,n.Bv][nodeQuadrant]

    GUIinteraction_previousSelection=0,0
    GUIinteraction_hovered = 0,0
    GUIinteraction_mouse:pygame.Vector2

    def GUIinteraction_Hover(self,pos):
        """ sets GUIinteraction_hovered to the node and its quadrant nearest to pos"""
        posV= pygame.Vector2(pos)
        self.GUIinteraction_mouse =posV
        if len(self.nodes)==0:
            return
        n = self.nodeGUI_NearestNode(posV)
        q = self.nodeGUI_NearestQuadrant(n,posV)
        self.GUIinteraction_hovered =n,q
    def GUIinteraction_Click(self,button):
        if self.GUIinteraction_hovered[0]!=0:
            if button == 0:
                self.GUIinteraction_Connect(self.GUIinteraction_hovered)
            elif button == 1:
                self.GUIinteraction_HaltConnect()
            elif button == 2:
                self.GUIinteraction_DeleteLink(self.GUIinteraction_hovered)
            elif button == 3:
                self.GUIinteraction_DeleteNode(self.GUIinteraction_hovered)
        if button == 4:
            self.GUIinteraction_CreateNode(self.GUIinteraction_mouse)
    def GUIinteraction_Connect(self,IDaQ):
        if self.GUIinteraction_previousSelection[0] == 0:
            self.GUIinteraction_previousSelection = IDaQ
        else:
            prSl = self.GUIinteraction_previousSelection
            self.link_CreateLink(IDaQ[0],IDaQ[1],prSl[0],prSl[1])
            self.GUIinteraction_previousSelection = 0,0
    def GUIinteraction_HaltConnect(self):
        self.GUIinteraction_previousSelection = 0,0
    def GUIinteraction_DeleteLink(self,IDaQ):
        self.link_DetachQuadrant(IDaQ[0],IDaQ[1])
    def GUIinteraction_DeleteNode(self,IDaQ):
        self.node_RemoveNode(IDaQ[0])
    def GUIinteraction_CreateNode(self,pos):
        n=self.node_CreateEmpty(pos)
        self.nodes[n.ID]=n

    def draw_DrawNode(self,nodeID,screen:Screen.Screen):
        col=(100,200,0)
        screen.DrawCircle(self.nodeGUI_Pos(nodeID),50,col)
    def draw_DrawConnections(self,receiverID,screen:Screen.Screen):
        for q in 0,2:
            emitter=self.link_GetReceiverLink(receiverID,q)
            if emitter[0]!=0:
                recPos=self.nodeGUI_QuadrantPos(receiverID,q)
                emiPos=self.nodeGUI_QuadrantPos(emitter[0],emitter[1])
                value=self.node_QuadrantValue(receiverID,q)
                col=(100+100*value,50+50*value,150*value)
                screen.DrawLine(recPos,emiPos,col)
    def draw_All(self,screen:Screen.Screen):
        for nodeID in self.nodes.keys():
            self.draw_DrawNode(nodeID,screen)
            self.draw_DrawConnections(nodeID,screen)
    def interface_Update(self,events,screen:Screen.Screen):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                self.GUIinteraction_Hover(e.__dict__['pos'])
            elif e.type == pygame.KEYDOWN:
                print(e.__dict__)
                print(self.nodes)
                k = e.__dict__['unicode']
                l = {'a':0,'s':1,'d':2,'f':3,'g':4}
                if k in l.keys():
                    print(l[k])
                    self.GUIinteraction_Click(l[k])
        screen.Clear()
        self.draw_All(screen)

a = NodeBoard()

Screen.Screen().Loop(a.interface_Update)

"""possible bugs:
    possibly undefined behaviour when removing a connection between a receiver and an emitter that have two connections
    """

