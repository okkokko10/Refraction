import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
    
def InteractSpring(world:World,particleID,interactionID,deltaTime):
    p1=world.GetParticle(particleID)
    p2=world.GetParticle(interactionID)
    I=p1.GetInteraction(interactionID)
    length,strength=I.args
    d=p1.GetPos()-p2.GetPos()
    l=d.length()
    if l==0:
        a=0
    else:
        # (l-length)/l
        a=(1-length/l)*strength
    f=d*a
    p2.ApplyForce(f)
    p1.ApplyForce(-f)

    I.forceApplied = 2*l*a
def Multiplier_Spring(distance,length):
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
    ConnectSpring(self,A,B,d.length(),strength)
World.ConnectSpring=ConnectSpring
World.ConnectSpringRest=ConnectSpringRest