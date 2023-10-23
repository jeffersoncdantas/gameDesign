import pygame
import sys
import random

pygame.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 800))

sprite_parado = pygame.transform.scale(pygame.image.load("mario_standing.png"), (48, 64))
sprite_pulando = pygame.transform.scale(pygame.image.load("mario_jumping.png"), (48, 64))
BACKGROUND = pygame.image.load("background.png")
plataforma = pygame.image.load("plataforma.png").convert_alpha()

maxPlat = 10

class Jef():

    def __init__(self,x,y):
        self.jefx = x
        self.jefy = y
        self.image = sprite_parado
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.jumping = False
        self.gravidade = 1
        self.altura_pulo = 20
        self.velocidade_y = self.altura_pulo
        self.direcao = "direita"
    
    def move(self):

        dx=0
        dy=0

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            self.jumping = True
        
        if keys_pressed[pygame.K_d]:
            self.jefx += 5
            self.rect.x += 5
            self.direcao = "direita"
        
        if keys_pressed[pygame.K_a]:
            self.jefx -= 5
            self.rect.x -=5
            self.direcao = "esquerda"


        if self.rect.left + self.jefx < 0:
            self.jefx = -self.rect.left
        if self.rect.right + self.jefx > 1600:
            self.jefx = 1600 - self.rect.right


        if self.jumping:
            self.jefy -= self.velocidade_y
            self.velocidade_y -= self.gravidade
            if self.velocidade_y < -self.altura_pulo:
                self.jumping = False
                self.velocidade_y = self.altura_pulo
            self.image = sprite_pulando
            self.rect.center = (self.jefx, self.jefy)
            SCREEN.blit(sprite_pulando, self.rect)
        else:
            self.image = sprite_parado
            self.rect.center = (self.jefx, self.jefy)
            SCREEN.blit(sprite_parado, self.rect)

        for i in plataformas:
            if i.rect.colliderect(self.rect.y + dy, self.rect.y, 48, 64):
                dy = 0
                if self.velocidade_y < 0:
                    dy = i.rect.bottom - self.rect.top
                    self.velocidade_y = 0
            
    def draw(self):
        if self.direcao == "direita":
            SCREEN.blit(self.image,self.rect)
        else:
            if self.jumping:
                sprite_pulando_virado = pygame.transform.flip(sprite_pulando, True, False)
                SCREEN.blit(sprite_pulando_virado,self.rect)
            else:    
                sprite_parado_virado = pygame.transform.flip(sprite_parado, True, False)
                SCREEN.blit(sprite_parado_virado,self.rect)
    
class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plataforma,(width,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.draw.rect(self.image, (255,0,0), [0, 0, width, 50], 1)


jef = Jef(400, 660)

plataformas = pygame.sprite.Group()

for i in range (maxPlat):
    tamanho = random.randint (100,300)
    x = random.randint(0,800-tamanho)
    y = i*random.randint(80,250)
    plataforma_gerada = Plataforma(x,y,tamanho)
    plataformas.add(plataforma_gerada)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jef.move()
    SCREEN.blit(BACKGROUND, (0, 0))
    plataformas.draw(SCREEN)
    jef.draw()

    pygame.display.update()
    CLOCK.tick(60)