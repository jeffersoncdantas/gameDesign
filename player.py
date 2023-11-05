import pygame


# Classe do jogador
class Player():
    def __init__(self, x, y, sprite_parado):
        self.image = pygame.transform.scale(sprite_parado, (30, 40))  # Redimensiona a imagem do personagem
        self.width = 25  # Largura do retângulo do jogador
        self.height = 34  # Altura do retângulo do jogador
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Cria um retângulo para o jogador
        self.rect.center = (x, y)  # Define a posição inicial do jogador no centro da tela
        self.vel_y = 0  # Velocidade vertical
        self.jumping = False #Add 28/10
        self.flip = False  # Indica se o jogador está virado para a esquerda

    def move(self, SCREEN_WIDTH, GRAVITY, platform_group, SCROLL_THRESH):
        scroll = 0  # Deslocamento vertical da tela
        dx = 0  # Deslocamento horizontal
        dy = 0  # Deslocamento vertical

        key = pygame.key.get_pressed()  # Obtém o estado das teclas pressionadas
        
        if key[pygame.K_SPACE] and self.jumping == False:
            self.vel_y = -20
            self.jumping = True
            
        if key[pygame.K_SPACE] == False:
            if self.vel_y == 10:
              self.jumping = False
                
        if key[pygame.K_d]:  # Tecla "D" pressionada
            dx += 5  # Movimento para a direita
            self.flip = False  # Define que o jogador não está virado para a esquerda
        
        if key[pygame.K_a]:  # Tecla "A" pressionada
            dx = -5  # Movimento para a esquerda
            self.flip = True  # Define que o jogador está virado para a esquerda

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

        if self.rect.top <= SCROLL_THRESH:  # Verifica se o jogador atingiu o limite superior da tela
            if self.vel_y < 0:  # Verifica se o jogador está subindo
                scroll = -dy  # Aplica um deslocamento negativo na tela

        self.rect.x += dx  # Atualiza a posição horizontal
        self.rect.y += dy + scroll # Atualiza a posição vertical com o deslocamento da tela

        self.mask = pygame.mask.from_surface(self.image)  # Atualiza a máscara de colisão

        return scroll  # Retorna o deslocamento vertical da tela

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))  # Desenha o jogador na tela