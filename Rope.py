import pygame
import Screen

class World:
    def __init__(self):
        self.particles={}
        self.idIter=0
        self.speed=1
        self.globalForces=[]
        self.partialUpdate=False
        self.midUpdates=1
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
        deltaTime*=self.speed/1000
        for i in range(self.midUpdates):
            self.Update(deltaTime/self.midUpdates)
        Draw.World(self,screen)
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
        self.appliedForce=pygame.Vector2(0,0)
        self.appliedForceOld=pygame.Vector2(0,0)
        self.appliedForceFrame=pygame.Vector2(0,0)
    def SetMass(self,value):
        self.mass=value
        self.massSqrt=value**0.5
    def ApplyForce(self,force):
        self.appliedForce+=force
    def AddInteraction(self,otherID,length,strength,interactionType):
        self.interactions[otherID]=Interaction(interactionType,strength,length)
    def GetInteractions(self):
        return self.interactions
    def InteractionsAttraction(self,deltaTime,world):
        for i in self.interactions:
            Interaction.interact(self,world.particles[i],self.interactions[i],deltaTime)
            if self.interactions and world.partialUpdate:
                self.UpdateMid(deltaTime,world)

    def Update1(self,deltaTime,world):
        self.InteractionsAttraction(deltaTime, world)
    def Update2(self,deltaTime,world,disable=True):
        if world.partialUpdate:
            if disable and self.interactions:
                self.appliedForceOld=self.appliedForceFrame*deltaTime
                self.appliedForceFrame=pygame.Vector2(0,0)
                return
            self.appliedForceFrame+=self.appliedForce

        self.force+=self.appliedForce*deltaTime
        self.appliedForceOld=self.appliedForce
        self.appliedForce=pygame.Vector2(0,0)
        if not self.IsAnchored():
            a=self.force/self.mass*deltaTime
            self.MovePos(a)
        #self.force*=0.9
    def UpdateMid(self,deltaTime,world):
        self.Update2(deltaTime,world,False)
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
        return Interaction.GetInteractionFunction(interaction.inType)(A,B,interaction,deltaTime)
    @staticmethod
    def GetInteractionFunction(inType):
        if inType==Interaction.SPRING:
            return Interaction.InteractSpring
    @staticmethod
    def InteractSpring(A,B,interaction,deltaTime):
        strength,length=interaction.args
        d=B.GetPos()-A.GetPos()
        l=d.length()
        a=Interaction.Multiplier_Spring(l,length)*strength
        f=d*a
        A.ApplyForce(f)
        B.ApplyForce(-f)

        interaction.forceApplied = l*a
    @staticmethod
    def Multiplier_Spring(distance,length):
        if distance==0:
            return 0
        return 1-length/(distance)
    def __init__(self,interactionType,*args):
        self.inType=interactionType
        self.args=args
        self.forceApplied=0
        self.strength,self.length=args

class Draw:
    @staticmethod
    def World(world,screen:Screen.Screen):
        screen.Clear()
        for i in world.particles:
            p=world.particles[i]
            color=Draw.ColorAcceleration(p)
            screen.DrawCircle(p.pos, p.massSqrt, color)
            for i in p.GetInteractions():
                I=p.GetInteractions()[i]
                if I.inType==Interaction.SPRING:
                    width=1+0.2*I.strength**0.5
                    colorFA=Draw.ColorForceApplied(I)
                    screen.DrawLine(p.pos, world.particles[i].pos, colorFA,width)
    @staticmethod
    def ColorAcceleration(particle):
        x=particle.appliedForceOld.length_squared()/(particle.mass**2)
        y=x/(x+1)
        c=(
            int(255*y),
            0,
            0
        )
        return c
    @staticmethod
    def ColorForceApplied(interaction):
        x=interaction.forceApplied
        b=interaction.strength
        y=(1+x/(2*b+abs(x)))/2
        z=1-y
        c=(
            int(255*y),
            100,
            int(255*z)
        )
        return c
    pass
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

w.speed=80
w.midUpdates=40
Screen.Screen().Loop(w.ScreenUpdate,20)