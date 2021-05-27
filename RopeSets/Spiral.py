import sys
sys.path.append('c:\\Users\\Okko Heiniö\\Desktop\\Python\\Refraction')
from RopeSets.RopePhysics import *

w=World()
def grav(particle:Particle,deltaTime):
    particle.ApplyForce(pygame.Vector2(0,1)*particle.mass*deltaTime*15)
w.AddGlobalForce(grav)
center=pygame.Vector2(400,400)
l=360
r=40
s=40
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
for i in range(1):
    w.ConnectSpringRest(f1[i],p,s)

w.speed=5
w.midUpdates=5

Start(w)