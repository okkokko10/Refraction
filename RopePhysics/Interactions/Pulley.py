import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *

def Interact(world:World,particleID,interactionID,deltaTime):

    C=world.GetParticle(particleID)#center
    I=C.GetInteraction(interactionID)#interaction
    i1,i2=interactionID
    P1=world.GetParticle(i1)#particle 1
    P2=world.GetParticle(i2)#particle 2
    length,strength=I.args
    d1=C.pos-P1.pos
    d2=C.pos-P2.pos
    L1=d1.length()
    L2=d2.length()
    stretch=(L1+L2-length)*strength
    
    f1=d1/L1*stretch
    f2=d2/L2*stretch

    P1.ApplyForce(f1)
    P2.ApplyForce(f2)
    C.ApplyForce(-f1-f2)

    pass
def Init(self):
    self.length,self.strength=self.args
    pass

def draw(world,particleID,interactionID,screen):
    pass
PULLEY=Interaction.AddType(Interact,Init,draw)

def ConnectPulley(self,center,A,B,length,strength):
    self.GetParticle(center).AddInteraction((A,B),PULLEY,length,strength)
def ConnectPulleyRest(self,center,A,B,strength):
    C=self.GetParticle(center)#center
    P1=self.GetParticle(A)#particle 1
    P2=self.GetParticle(B)#particle 2
    d1=C.pos-P1.pos
    d2=C.pos-P2.pos
    L1=d1.length()
    L2=d2.length()
    ConnectPulley(self,center,A,B,L1+L2,strength)
World.ConnectPulley=ConnectPulley
World.ConnectPulleyRest=ConnectPulleyRest