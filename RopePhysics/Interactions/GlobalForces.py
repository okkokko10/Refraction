import sys
sys.path.append(sys.path[0][:sys.path[0].rfind('Refraction')]+'Refraction')
from RopePhysics.MainRope import *


def AddGravity(world:World,amount):
    def gravity(particle:Particle,deltaTime):
        particle.ApplyForce(pygame.Vector2(0,particle.mass*amount))
    world.AddGlobalForce(gravity)