import pygame
class Screen:
    def __init__(self):
        self.canvas = pygame.display.set_mode((800,800))
    def Clear(self):
        self.canvas.fill((100,100,100))
    def DrawLine(self,A,B,color,width=1):
        pygame.draw.line(self.canvas,color,A,B,width)
    def DrawCircle(self,pos,radius,color):
        
        #pygame.draw.circle(self.canvas,color,pos,radius)
        pygame.draw.line(self.canvas,color,pos-pygame.Vector2(0,radius/2),pos+pygame.Vector2(0,radius/2),radius)
    def Loop(self,hook):
        run=True
        while run:
            pygame.time.wait(40)
            if pygame.event.get(pygame.QUIT):
                run=False
            e=pygame.event.get()
            hook(e,self)
            pygame.display.update()
            