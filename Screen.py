import pygame
class Screen:
    def __init__(self):
        self.canvas = pygame.display.set_mode((800,800))
    def Clear(self):
        self.canvas.fill((100,100,100))
    def DrawLine(self,A,B,color,width=1):
        a=int(A[0]),int(A[1])
        b=int(B[0]),int(B[1])
        pygame.draw.line(self.canvas,color,a,b,int(width))
    def DrawCircle(self,pos,radius,color):
        
        pygame.draw.circle(
            #self.canvas,0,(0,0),10)
            self.canvas,
            color,
            (int(pos[0]),int(pos[1])),
            int(radius))
        #pygame.draw.line(self.canvas,color,pos-pygame.Vector2(0,radius/2),pos+pygame.Vector2(0,radius/2),radius)
    def Loop(self,hook,time=40):
        run=True
        while run:
            deltaTime=pygame.time.wait(time)
            if pygame.event.get(pygame.QUIT):
                run=False
            e=pygame.event.get()
            hook(e,self,deltaTime)
            pygame.display.update()
            