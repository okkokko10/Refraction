import sys
a=sys.path[0].rfind('Refraction')
sys.path.append(sys.path[0][:a]+'Refraction')
from RopeSets.RopePhysics import *
    
def InteractSpring(world,particleID,interactionID,deltaTime):
    p1=world.GetParticle(particleID)
    p2=world.GetParticle(interactionID)
    I=p1.GetInteraction(interactionID)
    length,strength=I.args
    d=p1.GetPos()-p2.GetPos()
    l=d.length()
    a=Multiplier_Spring(l,length)*strength
    f=d*a
    p2.ApplyForce(f)
    p1.ApplyForce(-f)

    I.forceApplied = 2*l*a
def Multiplier_Spring(distance,length):
    if distance==0:
        return 0
    return 1-length/(distance)
def SpringInit(self):
    self.length,self.strength=self.args

def SpringDraw(world,particleID,interactionID,screen):
    p=world.GetParticle(particleID)
    I=p.GetInteraction(interactionID)
    width=1+0.2*I.strength**0.5
    colorFA=Draw.ColorForceApplied(I)
    screen.DrawLine(p.pos, world.GetParticle(interactionID).pos, colorFA,width)
SPRING=Interaction.AddType(InteractSpring,SpringInit,SpringDraw)

def ConnectSpring(self,A,B,length,strength):
    self.GetParticle(A).AddInteraction(B,SPRING,length,strength)
def ConnectSpringRest(self,A,B,strength):
    d=self.GetParticle(A).pos-self.GetParticle(B).pos
    self.ConnectSpring(A,B,d.length(),strength)
World.ConnectSpring=ConnectSpring
World.ConnectSpringRest=ConnectSpringRest