import pygame
import Screen


class World:
    def __init__(self):
        self.particles={}
        self.idIter=0
        self.speed=1
    def AddParticle(self,particle):
        self.idIter+=1
        self.particles[self.idIter]=particle
        return self.idIter
    def Connect(self,A,B,length,strength):
        self.particles[A].AddConnection(B,length,strength)
        #self.particles[B].AddConnection(A,length,strength)
    def Update(self):
        deltaTime=self.speed
        for i in self.particles:
            self.particles[i].Update1(deltaTime,self)
        for i in self.particles:
            self.particles[i].Update2(deltaTime,self)
    def ScreenUpdate(self,events,screen:Screen.Screen):
        self.Update()
        screen.Clear()
        for i in self.particles:
            p=self.particles[i]
            color=(0,0,0)
            screen.DrawCircle(p.pos, p.massSqrt, color)
            for i in p.GetConnections():
                screen.DrawLine(p.pos, self.particles[i].pos, color,p.GetConnections()[i][1])
    def GetParticle(self,i):
        return self.particles[i]
class Particle:
    def __init__(self,pos,force,mass):
        self.pos=pygame.Vector2(pos)
        self.force=pygame.Vector2(force)
        self.SetMass(mass)
        self.connections={}
    def SetMass(self,value):
        self.mass=value
        self.massSqrt=value**0.5
    def ApplyForce(self,force):
        self.force+=force
    def pullCoeff(self,distanceSq,length):
        return (distanceSq-length**2)/(distanceSq+length**2)
    def AttractionTo(self,other,length):
        d=other.GetPos()-self.GetPos()
        return d*self.pullCoeff(d.length_squared(),length)
    def AddConnection(self,otherID,length,strength):
        self.connections[otherID]=length,strength
    def GetConnections(self):
        return self.connections
    def ConnectionsAttraction(self,deltaTime,group):
        remove=[]
        for i in self.connections:
            if i in group:
                f=self.AttractionTo(group[i], self.connections[i][0])*self.connections[i][1]*deltaTime
                self.ApplyForce(f)
                group[i].ApplyForce(-f)
            else:
                remove.append(i)
        for i in remove:
            del self.connections[i]
    def Update1(self,deltaTime,world):
        self.ConnectionsAttraction(deltaTime, world.particles)
    def Update2(self,deltaTime,world):
        self.pos+=self.force/self.mass*deltaTime
        #self.force*=0.9
    def GetPos(self):
        return self.pos


w=World()
#a=w.AddParticle(Particle((100,100),(0,0),(100)))
# b=w.AddParticle(Particle((200,100),(0,0),(100)))
# c=w.AddParticle(Particle((200,110),(0,0),(100)))
# w.Connect(a, b, 50, 1)
# w.Connect(c, b, 30, 1)
# w.Connect(c, a, 20, 1)

f1=[]
for i in range(50):
    f1.append(w.AddParticle(Particle((10*i+200,200),(0,0),10+i)))
    if len(f1)>1:
        w.Connect(f1[-1], f1[-2], 10, 2+0*i/20)
w.GetParticle(f1[-1]).ApplyForce((1000,1000))
#w.GetParticle(f1[-1]).SetMass(100)
w.speed=2
Screen.Screen().Loop(w.ScreenUpdate)