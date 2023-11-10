import pygame

# Classe da onda
class Onda(pygame.sprite.Sprite):
    def __init__(self, x, y, onda_spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_onda = []
        for i in range (14):
            img = onda_spritesheet.subsurface((i * 400, 0, 400, 600))
            img = pygame.transform.scale(img, (400 / 2, 600/ 2))
            self.sprite_onda.append(img)

        self.index_lista = 0
        self.image = self.sprite_onda[self.index_lista]
        self.rect = self.image.get_rect()

        self.width = 400  # Largura do retângulo do jogador
        self.height = 600  # Altura do retângulo do jogador
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Cria um retângulo para o jogador

        self.jumping = False #Add 28/10

    def update(self):
        self.index_lista += 0.1
        if self.index_lista >= len(self.sprite_onda):
            self.index_lista = 0
        self.image = self.sprite_onda[int(self.index_lista)]
    
    def draw(self, screen):
       screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
