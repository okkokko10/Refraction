import pygame
import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
import Screen
sys.path.pop()

class World:
    def __init__(self):
        self.particles={}
        self.idIter=0
        self.speed=1
        self.globalForces=[]
        self.midUpdates=1
    def OldAddParticle(self,particle):
        self.idIter+=1
        self.particles[self.idIter]=particle
        return self.idIter
    def AddParticle(self,pos,force,mass):
        return self.OldAddParticle(Particle(pos,force,mass))
    def Update(self,deltaTime):
        for i in self.particles:
            self.ParticleUpdate(i,deltaTime)
        for f in self.globalForces:
            for i in self.particles:
                f(self.particles[i],deltaTime)
        for i in self.particles:
            self.particles[i].UpdateForce(deltaTime)
    def ScreenUpdate(self,events,screen:Screen.Screen,deltaTime):
        dt=deltaTime*self.speed/1000/self.midUpdates
        for i in range(self.midUpdates):
            self.Update(dt)
        Draw.World(self,screen)
    def GetParticle(self,i):
        return self.particles[i]
    def AddGlobalForce(self,func):
        """ func(particle,deltaTime) """
        self.globalForces.append(func)
    def ParticleUpdate(self,particleID,deltaTime):
        p=self.GetParticle(particleID)
        for interactionID in p.interactions:
            Interaction.interact(self,particleID,interactionID,deltaTime)
        pass
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
    def AddInteraction(self,otherID,interactionType,*args):
        self.interactions[otherID]=Interaction(interactionType,args)
    def GetInteractions(self):
        return self.interactions
    def GetInteraction(self,i):
        return self.interactions[i]
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
    def interact(world,particleID,interactionID,deltaTime):
        I=world.GetParticle(particleID).GetInteraction(interactionID).inType
        return Interaction.GetInteractionFunction(I)(world,particleID,interactionID,deltaTime)
    @staticmethod
    def GetInteractionFunction(inType):
        return Interaction.types[inType][0]
    def __init__(self,interactionType,args):
        self.inType=interactionType
        self.args=args
        self.forceApplied=0
        Interaction.types[interactionType][1](self)
    types={}
    typeIter=0
    @staticmethod
    def AddType(function,init,draw):
        '''Adds a interaction type.

        returns the interaction type's ID

        function(world,particleID,interactionID,deltaTime)

        init(self)

        draw(world,particleID,interactionID,screen)'''
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
                Draw.DrawInteraction(world,i,k,screen)
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
        if x==0:
            y=1/2
        else:
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
    def DrawInteraction(world,particleID,interactionID,screen:Screen.Screen):
        I=world.GetParticle(particleID).GetInteractions()[interactionID].inType
        Draw.GetInteractionDraw(I)(world,particleID,interactionID,screen)
    @staticmethod
    def GetInteractionDraw(inType):
        return Interaction.types[inType][2]


def Start(world):
    Screen.Screen().Loop(world.ScreenUpdate,20)