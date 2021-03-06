import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring

World.AddParticle=World.OldAddParticle
w=World()
import RopePhysics.Interactions.GlobalForces
RopePhysics.Interactions.GlobalForces.AddGravity(w,15)
center=pygame.Vector2(400,400)
l=360
r=40
s=200
p=w.AddParticle(Particle(center,(0,0),10))
f1=[]
for i in range(l):
    pos=pygame.Vector2(2+i/2,0).rotate(360/r*i)+center
    force=(0,0)
    mass=1
    f1.append(w.AddParticle(Particle(pos,force,mass)))
for i in range(l):
    w.ConnectSpringRest(f1[max(i-1,0)],f1[i],s)
    if i-r>0:
        w.ConnectSpringRest(f1[max(i-r,0)],f1[i],s)
    # if i-r-1>0:
    #     w.ConnectSpringRest(f1[max(i-r-1,0)],f1[i],s)
    # if i-2*r-1>0:
    #     w.ConnectSpringRest(f1[max(i-2*r-1,0)],f1[i],s)
w.GetParticle(p).Anchor()
for i in range(r):
    w.ConnectSpringRest(f1[i],p,s)

w.speed=5
w.midUpdates=5

Start(w)