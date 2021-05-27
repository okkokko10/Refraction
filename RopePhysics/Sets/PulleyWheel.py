import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley

w=World()

# f1=[]
# l=16
# for i in range(l):
#     pos=(300+i*5,300)
#     force=(0,0)
#     mass=5
#     w.AddParticle(pos,force,mass)

a=w.AddParticle((300,300),(0,0),100)
b=w.AddParticle((350,350),(0,0),10)
c=w.AddParticle((250,350),(0,0),50)
w.ConnectPulley(a,b,c,100,20)

Start(w)