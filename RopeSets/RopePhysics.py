import pygame
import sys
sys.path.append(
'c:\\Users\\Okko Heiniö\\Desktop\\Python\\Refraction')
import Screen

class World:
    def __init__(self):
        self.particles={}
        self.idIter=0
        self.speed=1
        self.globalForces=[]
        self.midUpdates=1
    def AddParticle(self,particle):
        if isinstance(particle,tuple):
            particle = Particle(particle[0],particle[1],particle[2])
        self.idIter+=1
        self.particles[self.idIter]=particle
        return self.idIter
    def Update(self,deltaTime):
        for i in self.particles:
            self.particles[i].Update1(deltaTime,self)
        for f in self.globalForces:
            for i in self.particles:
                f(self.particles[i],deltaTime)
        for i in self.particles:
            self.particles[i].UpdateForce(deltaTime)
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
    def GetInteraction(self,i):
        return self.interactions[i]
    def InteractionsAttraction(self,deltaTime,world):
        for i in self.interactions:
            Interaction.interact(self,world.particles[i],self.interactions[i],deltaTime)


    def Update1(self,deltaTime,world):
        self.InteractionsAttraction(deltaTime, world)
    def UpdateForce(self,deltaTime):

        self.force+=self.appliedForce*deltaTime
        self.appliedForceOld=self.appliedForce
        self.appliedForce=pygame.Vector2(0,0)
        if not self.IsAnchored():
            a=self.force/self.mass*deltaTime
            self.MovePos(a)
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
    @staticmethod
    def interact(A,B,interaction,deltaTime):
        return Interaction.GetInteractionFunction(interaction.inType)(A,B,interaction,deltaTime)
    @staticmethod
    def GetInteractionFunction(inType):
        return Interaction.types[inType][0]
    def __init__(self,interactionType,*args):
        self.inType=interactionType
        self.args=args
        self.forceApplied=0
        Interaction.types[interactionType][1](self)
    types={}
    typeIter=0
    @staticmethod
    def AddType(function,init,draw):
        '''Adds a type of interaction.
        function'''
        Interaction.typeIter+=1
        Interaction.types[Interaction.typeIter]=function,init,draw
        return Interaction.typeIter

class Draw:
    @staticmethod
    def World(world,screen:Screen.Screen):
        screen.Clear()
        for i in world.particles:
            p=world.GetParticle(i)
            for k in p.GetInteractions():
                Draw.DrawInteraction(i,k,world,screen)
            color=Draw.ColorAcceleration(p)
            screen.DrawCircle(p.pos, p.massSqrt, color)
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
    @staticmethod
    def DrawInteraction(particle,interaction,world,screen:Screen.Screen):
        I=world.GetParticle(particle).GetInteractions()[interaction].inType
        Draw.GetInteractionDraw(I)(particle,interaction,world,screen)
    @staticmethod
    def GetInteractionDraw(inType):
        return Interaction.types[inType][2]


def Start(world):
    Screen.Screen().Loop(world.ScreenUpdate,20)