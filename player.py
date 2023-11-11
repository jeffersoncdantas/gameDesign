import pygame

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet):
        pygame.sprite.Sprite.__init__(self)

        self.imagens_jef = []
        for i in range (4):
            img = sprite_sheet.subsurface((i * 126, 0, 126, 126))
            img = pygame.transform.scale(img, (126 / 2, 126/ 2))
            self.imagens_jef.append(img)

        self.index_lista = 0
        self.image = self.imagens_jef[self.index_lista]
        self.rect = self.image.get_rect()
        self.width = 56  # Largura do retângulo do jogador
        self.height = 60  # Altura do retângulo do jogador
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Cria um retângulo para o jogador
        self.rect.center = (x, y)  # Define a posição inicial do jogador no centro da tela
        self.vel_y = 0  # Velocidade vertical
        self.jumping = False #Add 28/10
        self.flip = False  # Indica se o jogador está virado para a esquerda
        self.doubleJumping = 2
        self.sound_jump = pygame.mixer.Sound("assets/sfx-pop.mp3")
        self.sound_jump.set_volume(0.5)

    # def flip_spritesheet(self):
    #     for i in range(len(self.imagens_jef)):
    #         self.imagens_jef[i] = pygame.transform.flip(self.imagens_jef[i], True, False)

    def update(self):
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.1
        self.image = self.imagens_jef[int(self.index_lista)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        
    def move(self, SCREEN_WIDTH, GRAVITY, platform_group, SCROLL_THRESH):
        scroll = 0  # Deslocamento vertical da tela
        dx = 0  # Deslocamento horizontal
        dy = 0  # Deslocamento vertical

        key = pygame.key.get_pressed()  # Obtém o estado das teclas pressionadas
        
        if key[pygame.K_SPACE] and not self.jumping and self.doubleJumping > 0:
            self.vel_y = -20
            self.doubleJumping -= 1
            self.jumping = True
            self.sound_jump.play()
              
        if not key[pygame.K_SPACE]:
            if self.vel_y == 10:
              self.jumping = False
                  
        # if key[pygame.K_d]:  # Tecla "D" pressionada
        #     dx = 5  # Movimento para a direita
        #     self.flipped = False

        # if key[pygame.K_a]:  # Tecla "A" pressionada
        #     dx = -5  # Movimento para a esquerda
        #     self.image = pygame.transform.flip(self.image, True, False)  # Inverte a imagem horizontalmente
        #     self.flipped = True
        
        key = pygame.key.get_pressed()  # Obtém o estado das teclas pressionadas
        if key[pygame.K_a]:  # Tecla "A" pressionada
            dx = -5  # Movimento para a esquerda
            self.flip = True  # Define que o jogador está virado para a esquerda
            
        if key[pygame.K_d]:  # Tecla "D" pressionada
            dx = 5  # Movimento para a direita
            self.flip = False  # Define que o jogador não está virado para a esquerda
   
        if self.rect.left + dx < 0:  # Verifica se o jogador não está fora da tela à esquerda
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:  # Verifica se o jogador não está fora da tela à direita
            dx = SCREEN_WIDTH - self.rect.right
        
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for platform in platform_group:  # Verifica colisões com as plataformas
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # Verifica colisões na direção vertical
                if self.rect.bottom < platform.rect.centery:  # Verifica se o jogador está acima da plataforma
                    if self.vel_y > 0:  # Verifica se o jogador está descendo
                        self.rect.bottom = platform.rect.top  # Coloca o jogador no topo da plataforma
                        dy = 0  # Zera o deslocamento vertical
                        
                        self.doubleJumping = 2
                        

        if self.rect.top <= SCROLL_THRESH:  # Verifica se o jogador atingiu o limite superior da tela
            if self.vel_y < 0:  # Verifica se o jogador está subindo
                scroll = -dy  # Aplica um deslocamento negativo na tela

        self.rect.x += dx  # Atualiza a posição horizontal
        self.rect.y += dy + scroll # Atualiza a posição vertical com o deslocamento da tela

        self.mask = pygame.mask.from_surface(self.image)  # Atualiza a máscara de colisão

        return scroll  # Retorna o deslocamento vertical da tela

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, True), (self.rect.x - 10, self.rect.y - 10))  # Desenha o jogador na tela