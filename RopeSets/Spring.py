import sys
a=sys.path[0].rfind('Refraction')
sys.path.append(sys.path[0][:a]+'Refraction')
from RopeSets.RopePhysics import *
    
def InteractSpring(A,B,interaction,deltaTime):
    strength,length=interaction.args
    d=B.GetPos()-A.GetPos()
    l=d.length()
    a=Multiplier_Spring(l,length)*strength
    f=d*a
    A.ApplyForce(f)
    B.ApplyForce(-f)

    interaction.forceApplied = l*a
def Multiplier_Spring(distance,length):
    if distance==0:
        return 0
    return 1-length/(distance)
def SpringInit(self):
    self.strength,self.length=self.args

def SpringDraw(particle,interaction,world,screen):
    p=world.GetParticle(particle)
    I=p.GetInteraction(interaction)
    width=1+0.2*I.strength**0.5
    colorFA=Draw.ColorForceApplied(I)
    screen.DrawLine(p.pos, world.GetParticle(interaction).pos, colorFA,width)
SPRING=Interaction.AddType(InteractSpring,SpringInit,SpringDraw)

def ConnectSpring(self,A,B,length,strength):
    self.particles[A].AddInteraction(B,length,strength,SPRING)
def ConnectSpringRest(self,A,B,strength):
    d=self.particles[A].pos-self.particles[B].pos
    self.ConnectSpring(A,B,d.length(),strength)
World.ConnectSpring=ConnectSpring
World.ConnectSpringRest=ConnectSpringRest