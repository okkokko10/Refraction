import sys
sys.path.append('c:\\Users\\Okko Heiniö\\Desktop\\Python\\Refraction')
from RopeSets.RopePhysics import *
w=World()
# f1=[]
# for i in range(50):
#     f1.append(w.AddParticle(Particle((4*i+300,200),(0,0),10)))
#     if len(f1)>1:
#         w.ConnectSpring(f1[-1], f1[-2], 4, 30)
# w.GetParticle(f1[-1]).SetMass(50)
# w.GetParticle(f1[0]).Anchor()
# w.ConnectSpring(f1[0],w.AddParticle(Particle((500,200),(0,0),50)),200,30)
def grav(particle:Particle,deltaTime):
    particle.ApplyForce(pygame.Vector2(0,1)*particle.mass*deltaTime*15)
w.AddGlobalForce(grav)
l=64
f2=[]
for i in range(l):
    rot=pygame.Vector2(0,200).rotate(360/l*i)
    pos=rot+pygame.Vector2(300,300)
    force=(0,0)#pygame.Vector2(0,500).rotate(360/l*i-90)
    mass=2
    f2.append(w.AddParticle(Particle(pos,force,mass)))
p1=w.AddParticle(Particle((300,300),(0,0),10))
for i in range(l):
    w.ConnectSpringRest(f2[i],f2[i-1],100)
    w.ConnectSpringRest(f2[i],f2[i-8],100)
    w.ConnectSpringRest(f2[i],f2[i-16],100)
    w.ConnectSpringRest(f2[i],p1,100)
#w.GetParticle(f2[0]).ApplyForce((100,0))
w.GetParticle(p1).Anchor()
p2=w.AddParticle(Particle((100,300),(0,0),500))
w.ConnectSpring(p2,f2[16],0,50)
if False:
    f3=[]
    f4=[]
    s=300
    l=8
    for i in range(l):
        f3.append(w.AddParticle(Particle((300,535+i*30),(0,0),1)))
        f4.append(w.AddParticle(Particle((320,520+i*30),(0,0),1)))
    for i in range(l-1):
        w.ConnectSpringRest(f3[i],f3[i+1],s)
        w.ConnectSpringRest(f4[i],f4[i+1],s)
        w.ConnectSpringRest(f3[i],f4[i],s)
        w.ConnectSpringRest(f3[i],f4[i+1],s)
    w.ConnectSpringRest(f3[0],f2[0],s)
    w.ConnectSpringRest(f4[0],f2[-1],s)
    w.ConnectSpringRest(f4[0],f2[0],s)
    w.ConnectSpringRest(f4[-1],f3[-1],s)
    w.GetParticle(f3[-1]).SetMass(50)

w.speed=40
w.midUpdates=40

Start(w)