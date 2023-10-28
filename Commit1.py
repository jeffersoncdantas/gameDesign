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

maxPlat = 4

class Jef():

	def __init__(self,x,y):
		self.image = sprite_parado
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.jumping = False
		self.velocidade_y = 0
		self.direcao = "direita"
	
	def move(self):

		dx = 0
		dy = 0

		keys_pressed = pygame.key.get_pressed()

		if keys_pressed[pygame.K_SPACE] and self.jumping == False:
			self.velocidade_y = -20
			self.jumping = True
		
		if keys_pressed[pygame.K_SPACE] == False:
			if self.velocidade_y == 10:
				self.jumping = False
	
		if keys_pressed[pygame.K_d]:
			dx += 5
			self.direcao = "direita"
			self.image = sprite_parado
		
		if keys_pressed[pygame.K_a]:
			dx -= 5
			self.direcao = "esquerda"
			sprite_parado_virado = pygame.transform.flip(sprite_parado, True, False)
			self.image = sprite_parado_virado

		if self.rect.left + self.rect.x < 0:
			self.rect.x = -self.rect.left
		if self.rect.right + self.rect.x > 1600:
			self.rect.x = 1600 - self.rect.right
		
		self.velocidade_y += 1
		if self.velocidade_y > 10:
			self.velocidade_y = 10
		dy += self.velocidade_y

		if self.rect.y > 620:
			self.rect.y = 620

		for i in plataformas:
			if i.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if self.rect.bottom < i.rect.centery:
					if self.velocidade_y > 0:
						self.rect.bottom = i.rect.top
						dy = 0
		
		self.rect.x += dx
		self.rect.y += dy
			
	def draw(self):
		SCREEN.blit(self.image,self.rect)		
class Plataforma(pygame.sprite.Sprite):
	def __init__(self,x,y,width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(plataforma,(width,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		pygame.draw.rect(self.image, (255,0,0), [0, 0, width, 50], 1)	

jef = Jef(400, 630)

plataformas = pygame.sprite.Group()

for i in range (maxPlat):
	tamanho = random.randint (100,300)
	x = random.randint(0,800-tamanho)
	y = i*random.randint(80,250)
	while y >= 620:
		y = i*random.randint(80,250)
	plataforma_gerada = Plataforma(x,y,tamanho)
	plataformas.add(plataforma_gerada)

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	print(jef.velocidade_y)
	jef.move()
	SCREEN.blit(BACKGROUND, (0, 0))
	plataformas.draw(SCREEN)
	jef.draw()

	pygame.display.update()
	CLOCK.tick(60)