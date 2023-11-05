import pygame, random, sys
from plataforma import Plataforma
from player import Player

pygame.init()

CLOCK = pygame.time.Clock()
FPS = 60 

# Define as dimensões da janela do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600  

# Cria a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption('Tsunami Jumping')

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
WHITE, BLACK, PANEL = (255, 255, 255), (0,0,0), (153, 217, 234)

font_small = pygame.font.SysFont('Consolas', 20) 
font_big = pygame.font.SysFont('Consolas', 24) 

# Carrega imagens
sprite_parado = pygame.image.load("assets/mario_standing.png") 
sprite_pulando = pygame.image.load("assets/mario_jumping.png") 
bg_image1 = pygame.image.load('assets/bg1.png')
bg_image = pygame.image.load('assets/bg.png')
platform_image = pygame.image.load('assets/plataforma.png')
wave_image = pygame.image.load("assets/onda.png")

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

# Instância do jogador
jef = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, sprite_parado) 

# Cria grupos de sprites para plataformas
platform_group = pygame.sprite.Group() 

# Cria a primeira plataforma
platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)  # Cria uma plataforma inicial
platform_group.add(platform)  # Adiciona a plataforma ao grupo de plataformas

# Loop principal do jogo
while True:
    CLOCK.tick(FPS)  
    
    # Verifica se o jogo ainda não acabou.
    if game_over == False:
        # Chama a função para mover o personagem e obtém o valor de deslocamento vertical.
        scroll = jef.move(SCREEN_WIDTH, GRAVITY, platform_group, SCROLL_THRESH)
        
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
            p_w = random.randint(40, 50)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(50, 60)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Plataforma(p_x, p_y, p_w, p_moving, platform_image)
            # Gera uma nova plataforma com propriedades aleatórias e adiciona ao grupo de plataformas.
            platform_group.add(platform) 

        # Atualiza as posições das plataformas de acordo com o deslocamento vertical.
        platform_group.update(scroll, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Incrementa a pontuação com base no deslocamento vertical.
        if scroll > 0:
            score += scroll
        
        # Desenha os sprites
        platform_group.draw(screen)
        jef.draw(screen)

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
                platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)
                platform_group.add(platform)

    # Manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # # Atualiza a pontuação mais alta
            # if score > high_score:
            #     high_score = score
            pygame.quit()
            sys.exit()
            
    # Atualiza a janela de exibição
    pygame.display.update()