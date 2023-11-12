import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_sheet):
        pygame.sprite.Sprite.__init__(self)

        self.imagens_fej = []
        for i in range(5):
            img = sprite_sheet.subsurface((i * 126, 0, 126, 126))
            img = pygame.transform.scale(img, (126 // 2, 126 // 2))
            self.imagens_fej.append(img)

        self.index_lista = 0
        self.image = self.imagens_fej[self.index_lista]
        self.width = 30  # Largura do retângulo do jogador
        self.height = 56  # Largura do retângulo do jogador
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.vel_y = 0
        inimigo_timer = 0
        INIMIGO_INTERVALO = 150
        self.plataforma_associada = None

        self.width = 56  # Largura do retângulo do jogador
        self.height = 56  # Altura do retângulo do jogador
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Cria um retângulo para o jogador
        self.rect.center = (x, y)  # Define a posição inicial do jogador no centro da tela
        self.vel_y = 0  # Velocidade vertical
        self.jumping = False #Add 28/10
        self.flipped = False  # Indica se o jogador está virado para a esquerda

    def flip_spritesheet(self):
        for i in range(len(self.imagens_fej)):
            self.imagens_fej[i] = pygame.transform.flip(self.imagens_fej[i], True, False)

    def update(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.1
        self.image = self.imagens_fej[int(self.index_lista)]

        if self.plataforma_associada:
            # Atualiza a posição vertical do inimigo com base na plataforma associada
            self.rect.y = self.plataforma_associada.rect.y - self.height
            
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        # Adicione a lógica para inverter a imagem se necessário
        screen.blit(self.image, (self.rect.x - 12, self.rect.y - 5))
