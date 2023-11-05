import pygame
import random

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))  # Redimensiona a imagem da plataforma
        self.moving = moving  # Indica se a plataforma está se movendo
        self.move_counter = random.randint(0, 50)  # Contador de movimento
        self.direction = random.choice([-1, 1])  # Direção do movimento (esquerda ou direita)
        self.speed = random.randint(1, 2)  # Velocidade do movimento
        self.rect = self.image.get_rect()  # Obtém o retângulo da plataforma
        self.rect.x = x  # Define a posição horizontal
        self.rect.y = y  # Define a posição vertical

    def update(self, scroll, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.moving == True:  # Verifica se a plataforma está se movendo
            self.move_counter += 1  # Incrementa o contador de movimento
            self.rect.x += self.direction * self.speed  # Move a plataforma na direção especificada

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:  # Verifica se a plataforma deve mudar de direção
            self.direction *= -1  # Inverte a direção do movimento
            self.move_counter = 0  # Reinicia o contador de movimento

        self.rect.y += scroll  # Atualiza a posição vertical da plataforma com o deslocamento da tela

        if self.rect.top > SCREEN_HEIGHT:  # Verifica se a plataforma saiu da tela
            self.kill()  # Remove a plataforma do grupo