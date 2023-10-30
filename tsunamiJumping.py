import pygame  # Biblioteca Pygame para criar o jogo
import random  # Biblioteca Random para geração de números aleatórios
import sys

pygame.init()  # Inicializa o Pygame

CLOCK = pygame.time.Clock()  # Cria um objeto para controlar o tempo
FPS = 60  # Taxa de quadros por segundo

# Define as dimensões da janela do jogo
SCREEN_WIDTH = 400  # Largura da janela
SCREEN_HEIGHT = 600  # Altura da janela

# Cria a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a janela com as dimensões especificadas
pygame.display.set_caption('Tsunami Jumping')  # Define o título da janela

SCROLL_SPEED = 0.5 # Velocidade da rolagem da tela
screen_movement = False # Rolagem da tela
SCROLL_THRESH = 200  # Limitador de rolagem da tela
GRAVITY = 1  # Gravidade aplicada ao personagem
MAX_PLATFORMS = 10  # Número máximo de plataformas na tela
scroll = 0  # Deslocamento vertical da tela
bg_scroll = 0  # Deslocamento do plano de fundo
game_over = False  # Indica se o jogo acabou
score = 0  # Pontuação do jogador
fade_counter = 0  # Contador para efeito de tela de game over
high_score = 0 # Pontuação maxima


# Define cores
WHITE = (255, 255, 255)  # Cor branca
BLACK = (0, 0, 0)  # Cor preta
PANEL = (153, 217, 234)  # Cor de um painel

font_small = pygame.font.SysFont('Lucida Sans', 20)  # Fonte pequena
font_big = pygame.font.SysFont('Lucida Sans', 24)  # Fonte grande

# Carrega imagens
sprite_parado = pygame.image.load("mario_standing.png")  # Carrega a imagem do personagem parado
sprite_pulando = pygame.image.load("mario_jumping.png") #  Carrega a imagem do personagem pulando
bg_image1 = pygame.image.load('bg1.png').convert_alpha()  # Carrega a imagem de fundo 1
bg_image = pygame.image.load('bg.png').convert_alpha()  # Carrega a imagem de fundo 
platform_image = pygame.image.load('plataforma.png').convert_alpha()  # Carrega a imagem das plataformas
wave_image = pygame.image.load("onda.png").convert_alpha() 

# Função para desenhar texto na tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # Renderiza o texto com a fonte e cor especificadas
    screen.blit(img, (x, y))  # Desenha o texto na tela nas coordenadas (x, y)

# Função para desenhar o painel de informações
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))  # Desenha um retângulo colorido como painel na parte superior da tela
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)  # Desenha uma linha branca abaixo do painel
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)  # Desenha a pontuação atual no painel
    draw_text('HIGH SCORE: ' + str(high_score), font_small, WHITE, 200, 0)
    
# Função para desenhar o plano de fundo
def draw_bg(bg_scroll):
    if score < 400:
        screen.blit(bg_image1, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
        screen.blit(bg_image, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
    else:
        screen.blit(bg_image, (0, 0 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
        screen.blit(bg_image, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento

# Classe do jogador
class Jef():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(sprite_parado, (30, 40))  # Redimensiona a imagem do personagem
        self.width = 25  # Largura do retângulo do jogador
        self.height = 34  # Altura do retângulo do jogador
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Cria um retângulo para o jogador
        self.rect.center = (x, y)  # Define a posição inicial do jogador no centro da tela
        self.vel_y = 0  # Velocidade vertical
        self.jumping = False #Add 28/10
        self.flip = False  # Indica se o jogador está virado para a esquerda

    def move(self):
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

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))  # Desenha o jogador na tela
        
# Classe das plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))  # Redimensiona a imagem da plataforma
        self.moving = moving  # Indica se a plataforma está se movendo
        self.move_counter = random.randint(0, 50)  # Contador de movimento
        self.direction = random.choice([-1, 1])  # Direção do movimento (esquerda ou direita)
        self.speed = random.randint(1, 2)  # Velocidade do movimento
        self.rect = self.image.get_rect()  # Obtém o retângulo da plataforma
        self.rect.x = x  # Define a posição horizontal
        self.rect.y = y  # Define a posição vertical

    def update(self, scroll):
        if self.moving == True:  # Verifica se a plataforma está se movendo
            self.move_counter += 1  # Incrementa o contador de movimento
            self.rect.x += self.direction * self.speed  # Move a plataforma na direção especificada

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:  # Verifica se a plataforma deve mudar de direção
            self.direction *= -1  # Inverte a direção do movimento
            self.move_counter = 0  # Reinicia o contador de movimento

        self.rect.y += scroll  # Atualiza a posição vertical da plataforma com o deslocamento da tela

        if self.rect.top > SCREEN_HEIGHT:  # Verifica se a plataforma saiu da tela
            self.kill()  # Remove a plataforma do grupo

# Instância do jogador
jef = Jef(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)  # Cria uma instância do jogador no centro da tela

# Cria grupos de sprites para plataformas e inimigos
platform_group = pygame.sprite.Group()  # Grupo de plataformas

# Cria a primeira plataforma
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False)  # Cria uma plataforma inicial
platform_group.add(platform)  # Adiciona a plataforma ao grupo de plataformas

# Loop principal do jogo
while True:

    CLOCK.tick(FPS)  # Limita a taxa de quadros por segundo.
    
    # Verifica se o jogo ainda não acabou.
    if game_over == False:
        # Chama a função para mover o personagem e obtém o valor de deslocamento vertical.
        scroll = jef.move()
        # Permite a rolagem da tela, primeiro pulo
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            screen_movement = True

        if screen_movement:
            for platform in platform_group:
                platform.rect.y += SCROLL_SPEED  # Move as plataformas para cima com a velocidade de rolagem
            bg_scroll += SCROLL_SPEED # Move o plano de fundo para cima

        # Desenha o fundo do jogo
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll) # Atualiza o deslocamento do fundo e desenha o fundo.
        
        #Desenha a onda 
        wave_rect = wave_image.get_rect()
        wave_rect.bottom = SCREEN_HEIGHT 
        screen.blit(wave_image, wave_rect)

        # Gera plataformas, verificando se o número de plataformas no grupo é menor que o máximo permitido.
        if len(platform_group) < MAX_PLATFORMS:
            
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 110)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            # Gera uma nova plataforma com propriedades aleatórias e adiciona ao grupo de plataformas.
            platform_group.add(platform) 

        # Atualiza as posições das plataformas de acordo com o deslocamento vertical.
        platform_group.update(scroll)
        
        # Incrementa a pontuação com base no deslocamento vertical.
        if scroll > 0:
            score += scroll
        
        # Desenha os sprites
        platform_group.draw(screen)
        jef.draw()

        # Desenha o painel de informações
        draw_panel()

        # Verifica se o personagem saiu da tela no topo e, nesse caso, encerra o jogo.
        if jef.rect.top > SCREEN_HEIGHT:
            game_over = True 
        # Verifica se o personagem encostou na onda e, nesse caso, encerra o jogo.    
        if jef.rect.colliderect(wave_rect):
            game_over = True
    else:
        
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
        else:
            draw_text('GAME OVER!', font_big, WHITE, 130, 200)
            draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
            # Se o jogo acabou, mostra a tela de "GAME OVER" e a pontuação.
            
            # Atualiza a pontuação mais alta
            if score > high_score:
                high_score = score
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # Se a tecla ESPAÇO for pressionada, reinicia o jogo.
                # Redefine as variáveis
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                jef.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150) # Reposiciona o personagem
                platform_group.empty() # Redefine as plataformas 
                bg_scroll = 0
                draw_bg(bg_scroll) # Desenha a tela novamente
                # Cria a plataforma inicial
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False)
                platform_group.add(platform)

    # Manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Atualiza a pontuação mais alta
            if score > high_score:
                high_score = score
            pygame.quit()
            sys.exit()
            
    # Atualiza a janela de exibição
    pygame.display.update()

# Finaliza o jogo e encerra o módulo Pygame
pygame.quit()