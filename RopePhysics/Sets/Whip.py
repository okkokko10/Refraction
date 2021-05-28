import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley

w=World()
import RopePhysics.Interactions.GlobalForces
#RopePhysics.Interactions.GlobalForces.AddGravity(w,15)

# c1=w.AddParticle((300,300),(0,0),5)
# w.GetParticle(c1).Anchor()
# a2=w.AddParticle((200,300),(0,0),5)
# a3=w.AddParticle((300,350),(0,0),500)
# b1=w.AddParticle((200,300),(0,0),50)

# w.ConnectPulleyRest(c1,a2,a3,200)
# w.ConnectSpringRest(a2,b1,200)

c1=w.AddParticle((370,300),(-5000,0),20)
f1=[]
pl= (100,300),(300,200),(300,400)
for p in pl:
    f1.append(w.AddParticle(p,(0,0),10))
for i in range(3):
    w.ConnectSpringRest(f1[i],f1[i-1],50)
    w.ConnectSpringRest(f1[i],c1,50)
w.GetParticle(f1[0]).Anchor()

Start(w)