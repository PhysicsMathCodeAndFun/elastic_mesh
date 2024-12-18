import pygame
import sys
import random
import math



pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()

size = 20
t = 0
delta_time = 0.0
dt = 0.01

class Particles:
    def __init__(self, x, y):
        self.rect =  pygame.Rect(x, y, size, size)
        self.visible = True
        self.color = [50,200,50]
        self.F = [0,0]
        
        self.x = [x,y]
        self.x0 = [x,y]
        self.m = 1.0

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)

            

particles = []
x_c, y_c = w//2, h//2
c_radius = 500
angle = 0

size2 = 100 

for x in range(2*size, w - 2*size, 2 * size):
    aux = []
    for y in range(2*size, h - 2*size, 2 * size):
        aux.append(Particles(x, y))
    particles.append(aux)
    
player = pygame.Rect(w//2, 400, 100, 100)
mousePress = False
idClicks_i = []
idClicks_j = []

k_elastic = 1.0 # elastic constant


def Update(screen):
    global t
    global delta_time
    global k_elastic
    
    screen.fill((0,0,0))

    
    last_p = particles
    
    for i in range(1, len(particles) - 1):
        for j in range(1, len(particles[0]) - 1):       
            
            c = [[0,0], [1,0], [0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]
            x_sum = 0
            y_sum = 0
            
            for k in range(1,9):
                cx = c[k][0]
                cy = c[k][1]
                x_sum += (last_p[i + cx][j + cy].x[0] - last_p[i + cx][j + cy].x0[0])
                y_sum += (last_p[i + cx][j + cy].x[1] - last_p[i + cx][j + cy].x0[1])
            
            particles[i][j].x[0] = 0.125 * ((last_p[i][j].F[0] / k_elastic) + x_sum) + last_p[i][j].x0[0]
            particles[i][j].x[1] = 0.125 * ((last_p[i][j].F[1] / k_elastic) + x_sum) + last_p[i][j].x0[1]
            
            particles[i][j].rect.centerx = particles[i][j].x[0]
            particles[i][j].rect.centery = particles[i][j].x[1]
            
            particles[i][j].draw(screen)
            
            
            
    
    text = font.render(f'github.com/PhysicsMathCodeAndFun  (elastic constant = {k_elastic:.2f})', True, (255,255,255))
    screen.blit(text, pygame.Rect(30, 0, 400,300))
    
    pygame.draw.rect(screen, (255, 0, 255), player, width=2)
    
    if mousePress:
        for l in idClicks_i:
            for p in idClicks_j:
                particles[l][p].F[0] = 1.0 * (player.centerx - particles[l][p].x0[0])
                particles[l][p].F[1] = 1.0 * (player.centery - particles[l][p].x0[1])
                particles[l][p].color = [255,255,255]
    else:           
        if len(idClicks_i) != 0 and len(idClicks_j) != 0:
            for l in idClicks_i:
                for p in idClicks_j:
                    particles[l][p].F[0] = 0
                    particles[l][p].F[1] = 0
                    particles[l][p].color = [50,200,50]
                    
            idClicks_i.clear()
            idClicks_j.clear()
            beep.play()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        player.width += 1
        player.height += 1
    if keys[pygame.K_s]:
        player.width -= 1
        player.height -= 1
    if keys[pygame.K_a]:
        if k_elastic > 0:
            if k_elastic >= 1:
                k_elastic -= 0.1
            else:
                k_elastic -= 0.01

            
    if keys[pygame.K_d]:
        if k_elastic >= 1:
            k_elastic += 0.1
        else:
            k_elastic += 0.01
        
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    
    

isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, len(particles)):
                for j in range(0, len(particles[0])):
                    if player.colliderect(particles[i][j].rect):
                        mousePress = True
                        idClicks_i.append(i)
                        idClicks_j.append(j)
                    
            
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            player.centerx = mouse_pos[0]
            player.centery = mouse_pos[1]

        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePress = False    
        
            
    Update(screen)
    
pygame.quit()
sys.exit()
