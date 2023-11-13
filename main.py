import pygame, random, sys
from plataforma import Plataforma
from player import Player
from onda import Onda
import botao
from inimigo import Inimigo
from spritesheet import SpriteSheet


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
cena = "comeco"
som = True
nome_usuario = ""
ultima_pontuacao = 0
nivel = 1

# Define cores
WHITE, BLACK, PANEL = (255, 255, 255), (0,0,0), (45,206,244)

font_small = pygame.font.Font('assets/agency_fb.ttf', 20) 
font_big = pygame.font.Font('assets/agency_fb.ttf', 35) 
font_wave = pygame.font.Font('assets/agency_fb.ttf', 50)

# Carrega imagens
bg_image1 = pygame.image.load('assets/bg1.png')
bg_image = pygame.image.load('assets/bg.png')
bglv2 = pygame.image.load('assets/bg2.png')
bglv2 = pygame.transform.scale(bglv2, (400, 600))
bglv3 = pygame.image.load('assets/bg3.png')
bglv3 = pygame.transform.scale(bglv3, (400, 600))
bglv4 = pygame.image.load('assets/bg4.png')
bglv4 = pygame.transform.scale(bglv4, (400, 600))
img_comecar = pygame.transform.scale(pygame.image.load('assets/telaDeInicio.png'), (400,600))
platform_image = pygame.image.load('assets/plataforma.png')
btJogar = pygame.image.load('assets/btJogar.png')
btInstrucoes = pygame.image.load('assets/btInstrucoes.png')
btSom = pygame.image.load('assets/btSom.png')
btSomDes = pygame.image.load('assets/btSomDesligado.png')
btRanking = pygame.image.load('assets/btRanking.png')
btVoltar = pygame.image.load('assets/voltar.png')
wave_image = pygame.image.load("assets/ondaBT.png")

botao_voltar = botao.Button(10, 17, btVoltar, 1)
botao_start = botao.Button(50, 150, btJogar, 1)
botao_instrucao = botao.Button(50, 250, btInstrucoes, 1)
botao_som = botao.Button(50, 350, btSom, 1)
botao_somDes = botao.Button(50, 350, btSomDes, 1)
botao_ranking = botao.Button(50, 450, btRanking, 1)

#input rect
input_rect = pygame.Rect(200, 200, 50, 550)

jef_spritesheet_img = pygame.image.load("assets/spriteCorrendo.png").convert_alpha()
sprite_onda_img = pygame.image.load("assets/ondaSprite.png").convert_alpha()

fej_spritesheet_img = pygame.image.load('assets/inimigo.png').convert_alpha()
fej_image = SpriteSheet(fej_spritesheet_img)

sound_death = pygame.mixer.Sound("assets/sfx-death.mp3")
sound_death.set_volume(0.9)


pygame.mixer.music.load('assets/sfx-music.mp3')  # Carrega a música de fundo do jogo
pygame.mixer.music.set_volume(0.6)  # Define o volume da música
pygame.mixer.music.play(-1, 0.0)  # Reproduz a música em loop



# Função para desenhar texto na tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # Renderiza o texto com a fonte e cor especificadas
    screen.blit(img, (x, y))  # Desenha o texto na tela nas coordenadas (x, y)

# Função para desenhar o painel de informações
def draw_panel():
    global nivel
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))  # Desenha um retângulo colorido como painel na parte superior da tela
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)  # Desenha uma linha branca abaixo do painel
    draw_text('SCORE: ' + str(score), font_small, WHITE, 5, 3)  # Desenha a pontuação atual no painel
    draw_text('HIGH SCORE: ' + str(high_score), font_small, WHITE, 200, 3)
    draw_text('NIVEL: ' + str(nivel), font_small, WHITE, 100, 3)
    
# Função para desenhar o plano de fundo
def draw_bg(bg_scroll):
    global nivel
    if score < 400:
        screen.blit(bg_image1, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
        screen.blit(bg_image, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
    else:
        screen.blit(bg_image, (0, 0 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
        screen.blit(bg_image, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
        if score > 2500:
            nivel = 2
            screen.blit(bglv2, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv2, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento

        if score > 5000:
            nivel = 3
            screen.blit(bglv3, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv3, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento
        if score > 7500:
            nivel = 4
            screen.blit(bglv4, (0, 0 + bg_scroll))  # Desenha o plano de fundo na tela com um deslocamento vertical
            screen.blit(bglv4, (0, -600 + bg_scroll))  # Desenha o plano de fundo acima do primeiro com deslocamento

# Instância do jogador
onda_alt = 200
jef = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, jef_spritesheet_img)

onda = Onda(0, 450 , sprite_onda_img)
onda2 = Onda(100, 450 , sprite_onda_img)
onda3 = Onda(200, 450 , sprite_onda_img)
onda4 = Onda(300, 450 , sprite_onda_img)

# Cria grupos de sprites para plataformas
platform_group = pygame.sprite.Group() 
jef_group =  pygame.sprite.Group(jef)
fej_group = pygame.sprite.Group()


onda_group = pygame.sprite.Group(onda)
onda_group2 = pygame.sprite.Group(onda2)
onda_group3 = pygame.sprite.Group(onda3)
onda_group4 = pygame.sprite.Group(onda4)

# Cria a primeira plataforma
platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)  # Cria uma plataforma inicial
platform_group.add(platform)  # Adiciona a plataforma ao grupo de plataformas

def jogar():
    
    global jef, jef_group, score, fej_group
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, screen_movement
    global GRAVITY, SCROLL_THRESH, SCROLL_SPEED, scroll
    global platform_group, platform, platform_image, MAX_PLATFORMS
    global p_w, p_x, p_y, p_type, p_moving
    global bg_scroll, draw_bg
    global wave_rect, wave_image, onda_group
    global draw_panel, game_over
    global som, sound_death

    global ultima_pontuacao
    
    
        
    # Chama a função para mover o personagem e obtém o valor de deslocamento vertical.
    scroll = jef.move(SCREEN_WIDTH, GRAVITY, platform_group, SCROLL_THRESH, som)

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

    #Desenha a onda base
    wave_rect = wave_image.get_rect() 
    wave_rect.bottom = SCREEN_HEIGHT 
    screen.blit(wave_image, wave_rect)

    #Sprite da onda
    onda_group.update()
    onda_group.draw(screen)
    
    onda_group2.update()
    onda_group2.draw(screen)
    
    onda_group3.update()
    onda_group3.draw(screen)
    
    onda_group4.update()
    onda_group4.draw(screen)

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
    platform_group.update(scroll, SCREEN_WIDTH, SCREEN_HEIGHT, wave_rect, onda_group, onda_group2, onda_group3, onda_group4)
    
    if len(fej_group) == 0 and score >2500:
        fej = Inimigo(SCREEN_WIDTH, 100, fej_image, 1.5)
        fej_group.add(fej)
	#Atualiza inimigos
    fej_group.update(scroll, SCREEN_WIDTH)

    if scroll > 0:
        score += scroll

    # Desenha os sprites
    platform_group.draw(screen)
    jef_group.draw(screen)
    jef_group.update()
    fej_group.draw(screen)

    # Desenha o painel de informações
    draw_panel()

    # Verifica se o personagem saiu da tela no topo e, nesse caso, encerra o jogo.
    if jef.rect.top > SCREEN_HEIGHT:
        if som:
            sound_death.play()
        game_over = True 
    # Verifica se o personagem encostou na onda e, nesse caso, encerra o jogo.    
    if jef.rect.colliderect(wave_rect):
        if som:
            sound_death.play()
        game_over = True
    # Verifica se o personagem encostou no inimigo e, nesse caso, encerra o jogo.   
    if pygame.sprite.spritecollide(jef, fej_group, False):
        if pygame.sprite.spritecollide(jef, fej_group, False, pygame.sprite.collide_mask):
            if som:
                sound_death.play()
            game_over = True
            

        
def reiniciar ():
    global game_over, score, scroll, fade_counter, jef, platform_group, bg_scroll, draw_bg, platform, screen_movement, nivel
    nivel = 1
    game_over = False
    score = 0
    scroll = 0
    fade_counter = 0
    jef.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200) # Reposiciona o personagem
    platform_group.empty() # Redefine as plataformas 
    fej_group.empty() #Redefine o inimigo
    bg_scroll = 0
    draw_bg(bg_scroll) # Desenha a tela novamente
    screen_movement = False


    # Cria a plataforma inicial
    platform = Plataforma(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 140, 100, False, platform_image)
    platform_group.add(platform)

def instrucoes():
    global screen, botao_voltar, cena, draw_text, font_big, font_small, font_wave, WHITE
    screen.fill((4, 89, 170))
    if botao_voltar.draw(screen):
        cena = "menu"
    draw_text('INSTRUÇÕES', font_wave, WHITE, 120, 10)
    draw_text('Para mover o Jef para a direita ', font_big, WHITE, 10, 100)
    draw_text('e esquerda utilize as teclas', font_big, WHITE, 10, 130)
    draw_text('A e D do teclado. ', font_big, WHITE, 10, 160)
    draw_text('Para fazer o Jef pular, utilize  ', font_big, WHITE, 10, 230) 
    draw_text('a tecla de Espaço no teclado. ', font_big, WHITE, 10, 260)
    draw_text('Caso o Jef colidir com a onda ', font_big, WHITE, 10, 330)
    draw_text('você perde o jogo. ', font_big, WHITE, 10, 360)
    draw_text('Caso o Jef colidir com o avião ', font_big, WHITE, 10, 430)
    draw_text('e o Fej, você perde o jogo. ', font_big, WHITE, 10, 460)
    
def mostrar_ranking():
    global screen, botao_voltar, cena, draw_text, font_big, font_small, font_wave, WHITE, ranking
    global lugar_1, lugar_2, lugar_3, lugar_4, lugar_5
    global nome_1, nome_2, nome_3, nome_4, nome_5
    
    screen.fill((4, 89, 170))
    if botao_voltar.draw(screen):
        cena = "menu"
        
    ranking_ordernado = sorted(ranking, key=lambda x: x[1], reverse=True)
    nomes_iguais = []
    cont = 1

    draw_text('RANKING', font_wave, WHITE, 120, 10)
    n = 100
    for i, (nome, score) in enumerate(ranking_ordernado, start=1):
        if nome in nomes_iguais:
            pass
        else:
            nomes_iguais.append(nome)
            draw_text(str(cont) + "º " + nome + " " + str(score), font_big, WHITE, 10, n)
            n += 50
            cont += 1
            if i == 8:
                break
        
def escreverArquivo(arquivo, nomeJogador, highScore):
        with open(arquivo, 'a') as file:
            file.write(nomeJogador + ", " + str(highScore) + '\n') 
            
def lerArquivo(arquivo):
    ranking = []
    
    with open (arquivo, "r") as file:
        dados = file.readlines()
    
    for linha in dados:
        partes = linha.split()
        if len(partes)>=2:
            nome_jogador = partes[0]
            score = int(partes[1])
            ranking.append((nome_jogador, score))
    new_ranking = list(set(ranking))
    return new_ranking
        
# Loop principal do jogo
while True:
    CLOCK.tick(FPS)
    
    
    
    ranking = lerArquivo("ranking.txt")
    
    if cena == 'comeco':
        screen.blit(img_comecar, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nome_usuario = nome_usuario[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    nome_usuario += event.unicode
                    
        draw_text('DIGITE SEU 1º NOME:', font_small, WHITE, 50, 140)        
        pygame.draw.rect(screen, WHITE, (50, 170, 310, 30), 1)
        
        # Renderiza o texto
        texto = font_small.render(nome_usuario, True, WHITE)
        screen.blit(texto, (60, 172))
        
        pygame.display.flip()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            cena = 'menu'     
            
              
    elif cena == 'menu':
        screen.fill((4, 89, 170)) 
        draw_text('BEM VINDO AO ', font_wave, WHITE, 90, 20)
        draw_text('TSUNAMI JUMPING', font_wave, WHITE, 59, 70)
        if botao_start.draw(screen):
            cena = "jogar"
        if botao_instrucao.draw(screen):
            cena = "instrucoes"
        if som and botao_som.draw(screen):
            pygame.mixer.music.pause()
            som = False
            botao_somDes.draw(screen)
        if not som and botao_somDes.draw(screen):
            pygame.mixer.music.play(-1, 0.0)
            som = True
        if botao_ranking.draw(screen):
            cena = "ranking"
        
                
    elif cena == 'instrucoes':
        instrucoes()
        
    elif cena == 'ranking':
        mostrar_ranking()
        
    elif cena == "jogar":           
    # Verifica se o jogo ainda não acabou.
        if game_over == False:
            jogar()
        else:
            if fade_counter < SCREEN_WIDTH:
                fade_counter += 5
                for y in range(0, 6, 2):
                    pygame.draw.rect(screen, (4,89,170), (0, y * 100, fade_counter, 100))
                    pygame.draw.rect(screen, (4,89,170), (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
            else:
                draw_text('GAME OVER!', font_big, WHITE, 130, 50)
                draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 90)
                draw_text('APERTE A TECLA ENTER', font_big, WHITE, 70, 200)
                draw_text('PARA JOGAR NOVAMENTE', font_big, WHITE, 60, 250)
                draw_text('OU APERTE V PARA VOLTAR', font_big, WHITE, 52, 370)
                draw_text('PARA A TELA INICIAL', font_big, WHITE, 85, 420)
                
                # Atualiza a pontuação mais alta
                if score > high_score:
                    high_score = score
            
                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    escreverArquivo("ranking.txt", nome_usuario, high_score) 
                    reiniciar()
                elif key[pygame.K_v]:
                    escreverArquivo("ranking.txt", nome_usuario, high_score) 
                    cena = "menu"
                    reiniciar()

    # Manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        
            pygame.quit()
            sys.exit()
            
    # Atualiza a janela de exibição
    pygame.display.update()