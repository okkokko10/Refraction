import pygame
import Screen

class World:
    def __init__(self):
        self.particles={}
        self.idIter=0
        self.speed=1
        self.globalForces=[]
    def AddParticle(self,particle):
        self.idIter+=1
        self.particles[self.idIter]=particle
        return self.idIter
    def ConnectSpring(self,A,B,length,strength):
        self.particles[A].AddInteraction(B,length,strength,Interaction.SPRING)
    def ConnectSpringRest(self,A,B,strength):
        d=self.particles[A].pos-self.particles[B].pos
        self.ConnectSpring(A,B,d.length(),strength)
    def Update(self,deltaTime):
        for i in self.particles:
            self.particles[i].Update1(deltaTime,self)
        for f in self.globalForces:
            for i in self.particles:
                f(self.particles[i],deltaTime)
        for i in self.particles:
            self.particles[i].Update2(deltaTime,self)
    def ScreenUpdate(self,events,screen:Screen.Screen,deltaTime):
        deltaTime/=1000
        self.Update(deltaTime)
        screen.Clear()
        for i in self.particles:
            p=self.particles[i]
            color=(0,0,0)
            screen.DrawCircle(p.pos, p.massSqrt, color)
            for i in p.GetInteractions():
                width=1+0.2*p.GetInteractions()[i][1]**0.5
                screen.DrawLine(p.pos, self.particles[i].pos, color,width)
    def GetParticle(self,i):
        return self.particles[i]
    def AddGlobalForce(self,func):
        """ func(particle,deltaTime) """
        self.globalForces.append(func)
class Particle:
    def __init__(self,pos,force,mass):
        self.pos=pygame.Vector2(pos)
        self.force=pygame.Vector2(force)
        self.SetMass(mass)
        self.interactions={}
        self.anchored=False
    def SetMass(self,value):
        self.mass=value
        self.massSqrt=value**0.5
    def ApplyForce(self,force):
        self.force+=force
    def AddInteraction(self,otherID,length,strength,interactionType):
        self.interactions[otherID]=interactionType,strength,length
    def GetInteractions(self):
        return self.interactions
    def InteractionsAttraction(self,deltaTime,group):
        remove=[]
        for i in self.interactions:
            if i in group:
                Interaction.interact(self,group[i],self.interactions[i],deltaTime)
            else:
                remove.append(i)
        for i in remove:
            del self.interactions[i]
    def Update1(self,deltaTime,world):
        self.InteractionsAttraction(deltaTime, world.particles)
    def Update2(self,deltaTime,world):
        if not self.IsAnchored():
            self.MovePos(self.force/self.mass*deltaTime)
        #self.force*=0.9
    def GetPos(self):
        return self.pos
    def MovePos(self,movement):
        self.pos+=movement
    def Anchor(self):
        self.anchored=True
    def Unanchor(self):
        self.anchored=False
    def IsAnchored(self):
        return self.anchored
class Interaction:
    SPRING=0
    @staticmethod
    def interact(A,B,interaction,deltaTime):
        Interaction.GetInteractionFunction(interaction[0])(A,B,interaction,deltaTime)
        pass
    @staticmethod
    def GetInteractionFunction(inType):
        if inType==Interaction.SPRING:
            return Interaction.InteractSpring
    @staticmethod
    def InteractSpring(A,B,interaction,deltaTime):
        strength,length=interaction[1:3]
        d=B.GetPos()-A.GetPos()
        
        f=d*Interaction.Multiplier_Spring(d.length_squared(),length)*strength*deltaTime#*A.mass*B.mass
        A.ApplyForce(f)
        B.ApplyForce(-f)

        return
    @staticmethod
    def Multiplier_Spring(distanceSq,length):
        if distanceSq==0:
            return 0
        return 1-length/(distanceSq**0.5)

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
    pos=pygame.Vector2(0,200).rotate(360/l*i)+pygame.Vector2(300,300)
    force=(0,0)
    mass=5
    f2.append(w.AddParticle(Particle(pos,force,mass)))
p1=w.AddParticle(Particle((300,300),(0,0),10))
for i in range(l):
    w.ConnectSpringRest(f2[i],f2[i-1],500)
    w.ConnectSpringRest(f2[i],f2[i-2],500)
    #w.ConnectSpringRest(f2[i],f2[i-3],5)
    w.ConnectSpring(f2[i],p1,200,100)
#w.GetParticle(f2[0]).ApplyForce((100,0))
w.GetParticle(p1).Anchor()
p2=w.AddParticle(Particle((100,300),(0,0),100))
w.ConnectSpring(p2,f2[16],0,400)
w.AddParticle(Particle((400,300),(0,0),200))

Screen.Screen().Loop(w.ScreenUpdate)