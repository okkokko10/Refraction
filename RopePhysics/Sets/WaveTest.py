import sys
import pygame
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *
import RopePhysics.Interactions.Spring
import RopePhysics.Interactions.Pulley
w=World()
import RopePhysics.Interactions.GlobalForces
#RopePhysics.Interactions.GlobalForces.AddGravity(w,15)
def noneFunc(*x):
    pass
    
def fakeWaveInteraction(world:World,particleID,interactionID):
    p1=world.GetParticle(particleID)
    p2=world.GetParticle(interactionID)
    if p1.anchored or p2.anchored:
        return
    I=p1.GetInteraction(interactionID)
    d=p1.waveZ-p2.waveZ
    d*=0.02
    p1.waveZchange-=d
    p2.waveZchange+=d
FAKEWAVE=Interaction.AddType(fakeWaveInteraction,noneFunc,noneFunc)

def ConnectSpringWave(self,A,B,strength):
    self.GetParticle(A).waveZ=0
    self.GetParticle(B).waveZ=0
    self.GetParticle(A).waveZchange=0
    self.GetParticle(B).waveZchange=0
    self.GetParticle(A).waveZvel=0
    self.GetParticle(B).waveZvel=0
    self.GetParticle(A).AddInteraction(B,FAKEWAVE,strength)
World.ConnectSpringRest=ConnectSpringWave
L=6*16
h=7
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
owX=50
iwX=26
impactX=16
di=2
wi=3
wi0=1
he=26
slit1=di+he+owX//2
slit2=-di+he+owX//2
slit0=he+iwX//2
if True:
    for y in range(L):
        if y-wi<=slit1<=y or y<=slit2<=y+wi:#24<y<32 or 40<y<46:
            pass
        else:
            w.GetParticle(f1[owX][y]).Anchor()
    if True:
        for y in range(L):
            if y-wi0<=slit0<=y+wi0:
                pass
            else:
                w.GetParticle(f1[iwX][y]).Anchor()

impactParticle=w.GetParticle(f1[impactX][he+impactX//2])
impactParticle.waveZvel=10
# impactParticle.ApplyForce(pygame.Vector2(-1,0))
# for i in range(1):
#     for p in f1[i]:
#         impactParticle=w.GetParticle(p)
#         impactParticle.waveZvel=1


def updateWave(p,deltaTime):
    p.waveZvel+=p.waveZchange
    p.waveZ+=p.waveZvel
    p.waveZchange=0
w.AddGlobalForce(updateWave)

from RopePhysics.Show import NearestParticle as NearPar
def pluckIt(self:World,events,screen):
    for e in events:
        if e.type==pygame.MOUSEBUTTONDOWN:
            button=e.__dict__['button']
            pos=e.__dict__['pos']
            if button==1:
                minDistanceSq=-1
                for i in range(30):
                    pI=NearPar(self,pos,minDistanceSq)
                    minDistanceSq=pI[1]
                    if pI[0]:
                        p=self.GetParticle(pI[0])
                        d=p.GetPos()-pos
                        # p.ApplyForce(10*d/(pI[1]))
                        p.ApplyForce(pygame.Vector2(10,0))
# w.AddScreenEventFunc(pluckIt)

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
    if particle.anchored:
        return (250,250,250)
    fo=particle.appliedForceOld
    #x=fo.length_squared()*10
    # y=x/(x+1)
    Y=lambda x: x/(x+1)
    # Y2=lambda x: (1+x/(abs(x)+1))/2
    # x=fo.x*10
    # a=(x>0)#*Y(x)
    b=0
    # c=(x<0)#*Y(-x)
    if particle.waveZ:
        a=Y(max(particle.waveZ,0))
        c=Y(max(-particle.waveZ,0))
    else:
        return None
    if particle.waveZ<0.1:
        return None
    color=(
        int(255*a),
        int(255*b),
        int(255*c)
    )
    return color
Draw.ParticleColor=particleColor
Draw.DrawInteraction=noneFunc


Start(w)