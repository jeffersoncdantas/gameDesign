import os
import pygame, random, sys
from plataforma import Plataforma
from player import Player
from onda import Onda
import botao

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
menu = "start"
game_paused = False
seilabicho = True
som = True

# Define cores
WHITE, BLACK, PANEL = (255, 255, 255), (0,0,0), (153, 217, 234)

font_small = pygame.font.SysFont('Consolas', 20) 
font_big = pygame.font.SysFont('Consolas', 24) 
font_bigbig = pygame.font.SysFont('Consolas', 42) 

# Carrega imagens
bg_image1 = pygame.image.load('assets/bg1.png')
bg_image = pygame.image.load('assets/bg.png')
bglv2 = pygame.image.load('assets/bg2.png')
bglv2 = pygame.transform.scale(bglv2, (400, 600))
bglv3 = pygame.image.load('assets/bg3.png')
bglv3 = pygame.transform.scale(bglv3, (400, 600))
bglv4 = pygame.image.load('assets/bg4.png')
bglv4 = pygame.transform.scale(bglv4, (400, 600))
platform_image = pygame.image.load('assets/plataforma.png')
botaoimg = pygame.image.load('assets/botao.png')
wave_image = pygame.image.load("assets/ondaBG.png")

botao_start = botao.Button(50, 150, botaoimg, 1)
botao_instrucao = botao.Button(50, 250, botaoimg, 1)
botao_som = botao.Button(50, 350, botaoimg, 1)
botao_ranking = botao.Button(50, 450, botaoimg, 1)

jef_spritesheet_img = pygame.image.load("assets/spriteCorrendo.png").convert_alpha()
sprite_onda_img = pygame.image.load("assets/ondaSprite.png").convert_alpha()

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
        if score > 2500:

            screen.blit(bglv2, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv2, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento

        if score > 5000:
            screen.blit(bglv3, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv3, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
        if score > 7500:
            screen.blit(bglv4, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv4, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento

# Instância do jogador
onda_alt = 200
jef = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, jef_spritesheet_img)
onda = Onda(0, 200 , sprite_onda_img)

# Cria grupos de sprites para plataformas
platform_group = pygame.sprite.Group() 
jef_group =  pygame.sprite.Group(jef)
onda_group = pygame.sprite.Group(onda)

# Cria a primeira plataforma
platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)  # Cria uma plataforma inicial
platform_group.add(platform)  # Adiciona a plataforma ao grupo de plataformas

def jogar():
    
    global jef, jef_group, score
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, screen_movement
    global GRAVITY, SCROLL_THRESH, SCROLL_SPEED, scroll
    global platform_group, platform, platform_image, MAX_PLATFORMS
    global p_w, p_x, p_y, p_type, p_moving
    global bg_scroll, draw_bg
    global wave_rect, wave_image, onda_group
    global draw_panel, game_over
    
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

    #Sprite da onda
    onda_group.update()
    onda_group.draw(screen)

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
    jef_group.draw(screen)
    jef_group.update()

    # Desenha o painel de informações
    draw_panel()

    # Verifica se o personagem saiu da tela no topo e, nesse caso, encerra o jogo.
    if jef.rect.top > SCREEN_HEIGHT:
        game_over = True 
    # Verifica se o personagem encostou na onda e, nesse caso, encerra o jogo.    
    if jef.rect.colliderect(wave_rect):
        game_over = True
        
def reiniciar ():
    global game_over, score, scroll, fade_counter, jef, platform_group, bg_scroll, draw_bg, platform
    game_over = False
    score = 0
    scroll = 0
    fade_counter = 0
    jef.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200) # Reposiciona o personagem
    platform_group.empty() # Redefine as plataformas 
    bg_scroll = 0
    draw_bg(bg_scroll) # Desenha a tela novamente
    # Cria a plataforma inicial
    platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)
    platform_group.add(platform)
    
# Loop principal do jogo
while True:
    CLOCK.tick(FPS)
    if seilabicho == True:
        screen.fill((135,206,250)) 
        seilabicho = False
    else:
        if menu == 'start':
            draw_text('TSUNAMI JUMPING', font_bigbig, WHITE, 25, 55)
            if botao_start.draw(screen):
                menu = "comecou"
            if botao_instrucao.draw(screen):
                menu = "instrucoes"
            if botao_som.draw(screen):
                if som:
                    som = False
                if not som:
                    som = True
            if botao_ranking.draw(screen):
                pygame.quit()
                sys.exit()

        elif menu == 'instrucoes':
            retangulo = pygame.draw.rect(screen, (255,255,0), pygame.Rect(30, 30, 60, 60))
            screen.blit(screen,retangulo)
        else:           
        # Verifica se o jogo ainda não acabou.
            if game_over == False:
                jogar()
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
                    
                    # Atualiza a pontuação mais alta
                    if score > high_score:
                        high_score = score
                        
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        reiniciar()

        # Manipulador de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Atualiza a janela de exibição
        pygame.display.update()