import pygame
from pygame.locals import *
from sys import exit

pygame.init()
fps = pygame.time.Clock()
SCREEN_SIZE =(800,600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)
jefSprite = pygame.image.load('amylee.jpg').convert()

class Jef():
    def __init__(self,x,y):
        self.image = jefSprite
        self.width = 70
        self.width = 100
        self.rect = self.image.get_rect()
        self.vel_y = 0
        self.rect.center = (x,y)
        self.pulando = False
    
    def move(self):

        jefx = 0
        jefy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            jefx = -10
        if key[pygame.K_d]:
            jefx = 10
        if key[pygame.K_w]:
            self.pulando = True

        gravidade = 1
        altura_pulo = 20
        y_velocidade = altura_pulo

        if self.pulando == True:
            jefy -= y_velocidade
            y_velocidade -= gravidade
            if y_velocidade < -altura_pulo:
                self.pulando = False
                y_velocidade = altura_pulo
            self.rect.y
            
        if self.rect.left + jefx < 0:
            jefx = -self.rect.left
        if self.rect.right + jefx > 800:
            jefx = 800 - self.rect.right
        
        self.rect.x += jefx
        self.rect.y += jefy

    def draw(self):
        screen.blit(self.image,self.rect)

jef = Jef(800/2, 600-150)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        jef.move()
        screen.fill((255,255,255))
        jef.draw()
    
        fps.tick(60)
        pygame.display.update()
