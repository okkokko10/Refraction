import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley

w=World()
def grav(particle:Particle,deltaTime):
    particle.ApplyForce(pygame.Vector2(0,1)*particle.mass*15)
w.AddGlobalForce(grav)
# f1=[]
# l=16
# for i in range(l):
#     pos=(300+i*5,300)
#     force=(0,0)
#     mass=5
#     w.AddParticle(pos,force,mass)

a=w.AddParticle((300,300),(0,0),100)
b=w.AddParticle((350,350),(0,0),10)
c=w.AddParticle((250,250),(0,0),10)
w.GetParticle(b).Anchor()
#w.GetParticle(c).Anchor()
w.ConnectPulley(a,b,c,150,20)

w.speed=20
w.midUpdates=40
Start(w)