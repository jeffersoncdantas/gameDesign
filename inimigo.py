import pygame
import random

class Inimigo(pygame.sprite.Sprite):
	def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
		pygame.sprite.Sprite.__init__(self)
		
		self.imagens_fej = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
		self.direction = random.choice([-1, 1])
		if self.direction == 1: #Define a direção da animação
			self.flip = False
		else:
			self.flip = True

		#Carregar as imagens do spritesheet
		numero_frames = 4
		for animation in range(numero_frames):
			image = sprite_sheet.get_image(animation, 120, 100, scale, (0, 0, 0))
			image = pygame.transform.scale(image, (120 / 1.1, 100/ 1.1))
			image = pygame.transform.flip(image, self.flip, False)
			image.set_colorkey((0, 0, 0))
			self.imagens_fej.append(image)
		
		#Setando imagem inicial e o retangulo do inimigo
		self.image = self.imagens_fej[self.frame_index]
		self.rect = self.image.get_rect()

		if self.direction == 1:
			self.rect.x = 0
		else:
			self.rect.x = SCREEN_WIDTH
		self.rect.y = y

	def update(self, scroll, SCREEN_WIDTH):
		#Atualiza animação
		animation_cooldown = 30000
		self.image = self.imagens_fej[self.frame_index]
		#Verifica quanto tempo passou desde a ultima atualização
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#Reinicia a animação, caso tenha acabado
		if self.frame_index >= len(self.imagens_fej):
			self.frame_index = 0

		#Movimento do inimigo
		self.rect.x += self.direction * 2
		self.rect.y += scroll

		#Verifica se o jogador saiu da tela
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()