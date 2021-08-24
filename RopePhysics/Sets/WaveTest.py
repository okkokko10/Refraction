import sys
import pygame
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley

w=World()
import RopePhysics.Interactions.GlobalForces
#RopePhysics.Interactions.GlobalForces.AddGravity(w,15)
L=6*16
h=5
s=10
f1=[]
eqTriHeight=(3**0.5)/2
for x in range(L):
    f1.append([])
    for y in range(L):
        pos=pygame.Vector2(200+x*h*eqTriHeight,200+y*h-x*h/2)
        force=(0,0)
        mass=5
        f1[-1].append(w.AddParticle(pos,force,mass))
for x in range(L):
    for y in range(L):
        if y-1>=0:
            w.ConnectSpringRest(f1[x][y],f1[x][y-1],s)
        if x-1>=0:
            w.ConnectSpringRest(f1[x][y],f1[x-1][y],s)
        if x-1>=0 and y-1>=0:
            w.ConnectSpringRest(f1[x][y],f1[x-1][y-1],s)

'creating a wall'
owX=32+10
iwX=16+10
di=2
he=32
for y in range(L):
    if y==di+he+owX//2 or y==-di+he+owX//2:#24<y<32 or 40<y<46:
        pass
    else:
        w.GetParticle(f1[owX][y]).Anchor()
for y in range(L):
    if y==he+iwX//2:
        pass
    else:
        w.GetParticle(f1[iwX][y]).Anchor()
w.GetParticle(f1[0][he]).ApplyForce(pygame.Vector2(-1000,0))


def getTotal(self,events,screen):
    totalForce=pygame.Vector2(0,0)
    #totalPos=pygame.Vector2(0,0)
    for i in self.particles:
        totalForce+=self.particles[i].force
        #totalPos+=self.particles[i].pos
    #avgPos=totalPos*(1/len(self.particles))
    print(totalForce)
#w.AddScreenEventFunc(getTotal)

w.speed=10
w.midUpdates=1
def particleColor(particle):
    x=particle.appliedForceOld.length_squared()*10
    y=x/(x+1)
    c=(
        int(255*y),
        0,
        0
    )
    # if x>0:
    #     c=(255,0,0)
    # else:
    #     c=(0,0,0)
    return c
Draw.ParticleColor=particleColor
def noneFunc(*x):
    pass
Draw.DrawInteraction=noneFunc


Start(w)