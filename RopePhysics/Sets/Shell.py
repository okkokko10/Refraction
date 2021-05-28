import sys
import pygame
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley

w=World()
def grav(particle:Particle,deltaTime):
    particle.ApplyForce(pygame.Vector2(0,1)*particle.mass*15)
w.AddGlobalForce(grav)
L=16
h=15
s=100
f1=[]
for x in range(L):
    f1.append([])
    for y in range(L):
        pos=pygame.Vector2(300+x*h,200+y*h-x*h/2)
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
w.GetParticle(f1[0][0]).Anchor()
w.GetParticle(f1[-1][0]).Anchor()

s1=5
c1=200
m2=20
a1=w.AddParticle((100,100),(0,0),5)
a2=w.AddParticle((100,200+c1),(0,0),m2)
b1=w.AddParticle((150,150),(0,0),5)
b2=w.AddParticle((150,200+c1),(0,0),m2)
w.ConnectSpringRest(a1,a2,s1)
w.ConnectSpringRest(b1,b2,s1)
w.GetParticle(a1).Anchor()
w.GetParticle(b1).Anchor()

w.speed=10
w.midUpdates=20

Start(w)