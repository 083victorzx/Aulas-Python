import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA_JOGO = 600
ALTURA = 400
LARGURA_TOTAL = 800  # espaço extra para o placar
TAMANHO_QUADRADO = 20
TAMANHO_OBSTACULO = 40  # obstáculos maiores

tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA))
pygame.display.set_caption("🐍 Snake Game com Obstáculos Grandes")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 150, 255)
CINZA = (40, 40, 40)
AMARELO = (255, 255, 0)

# Fonte
fonte = pygame.font.SysFont("Arial", 25, True)

# Função para desenhar a cobra com cantos arredondados
def desenhar_cobra(tamanho, lista_corpo):
    for x, y in lista_corpo:
        pygame.draw.rect(tela, VERDE, (x, y, tamanho, tamanho), border_radius=6)

# Função para mostrar o placar na lateral
def mostrar_pontuacao(pontos):
    pygame.draw.rect(tela, CINZA, (LARGURA_JOGO, 0, 200, ALTURA))  # painel lateral
    texto_titulo = fonte.render("PLACAR", True, BRANCO)
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_titulo, (LARGURA_JOGO + 50, 30))
    tela.blit(texto_pontos, (LARGURA_JOGO + 40, 70))

# Função para gerar obstáculo aleatório
def gerar_obstaculo():
    x = round(random.randrange(0, LARGURA_JOGO - TAMANHO_OBSTACULO) / 20.0) * 20
    y = round(random.randrange(0, ALTURA - TAMANHO_OBSTACULO) / 20.0) * 20
    return [x, y]

# Função principal do jogo
def jogo():
    sair = False
    fim_de_jogo = False

    x = LARGURA_JOGO // 2
    y = ALTURA // 2
    x_vel = TAMANHO_QUADRADO
    y_vel = 0
    velocidade = 10

    corpo_cobra = []
    tamanho_cobra = 1
    pontos = 0

    comida_x = round(random.randrange(0, LARGURA_JOGO - TAMANHO_QUADRADO) / 20.0) * 20
    comida_y = round(random.randrange(0, ALTURA - TAMANHO_QUADRADO) / 20.0) * 20

    obstaculos = []  # lista de obstáculos

    clock = pygame.time.Clock()

    while not sair:
        while fim_de_jogo:
            tela.fill(PRETO)
            msg = fonte.render("💀 Game Over! Pressione R para reiniciar ou Q para sair", True, VERMELHO)
            tela.blit(msg, (LARGURA_TOTAL / 2 - 300, ALTURA / 2 - 30))
            mostrar_pontuacao(pontos)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair = True
                    fim_de_jogo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        sair = True
                        fim_de_jogo = False
                    if evento.key == pygame.K_r:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_vel == 0:
                    x_vel = -TAMANHO_QUADRADO
                    y_vel = 0
                elif evento.key == pygame.K_RIGHT and x_vel == 0:
                    x_vel = TAMANHO_QUADRADO
                    y_vel = 0
                elif evento.key == pygame.K_UP and y_vel == 0:
                    y_vel = -TAMANHO_QUADRADO
                    x_vel = 0
                elif evento.key == pygame.K_DOWN and y_vel == 0:
                    y_vel = TAMANHO_QUADRADO
                    x_vel = 0

        x += x_vel
        y += y_vel

        # Quando bate na parede, dá meia-volta
        if x >= LARGURA_JOGO:
            x = LARGURA_JOGO - TAMANHO_QUADRADO
            x_vel = -x_vel
        elif x < 0:
            x = 0
            x_vel = -x_vel
        elif y >= ALTURA:
            y = ALTURA - TAMANHO_QUADRADO
            y_vel = -y_vel
        elif y < 0:
            y = 0
            y_vel = -y_vel

        tela.fill(PRETO)
        pygame.draw.rect(tela, (20, 20, 20), (0, 0, LARGURA_JOGO, ALTURA))

        # Desenha comida arredondada
        pygame.draw.rect(tela, AZUL, (comida_x, comida_y, TAMANHO_QUADRADO, TAMANHO_QUADRADO), border_radius=8)

        # Atualiza corpo da cobra
        cabeca_cobra = [x, y]
        corpo_cobra.append(cabeca_cobra)
        if len(corpo_cobra) > tamanho_cobra:
            del corpo_cobra[0]

        # Verifica colisão com próprio corpo
        for parte in corpo_cobra[:-1]:
            if parte == cabeca_cobra:
                fim_de_jogo = True

        # Desenha a cobra
        desenhar_cobra(TAMANHO_QUADRADO, corpo_cobra)

        # Desenha obstáculos grandes
        for ox, oy in obstaculos:
            pygame.draw.rect(tela, AMARELO, (ox, oy, TAMANHO_OBSTACULO, TAMANHO_OBSTACULO), border_radius=6)

        # Verifica colisão com obstáculos
        for ox, oy in obstaculos:
            if (x + TAMANHO_QUADRADO > ox and x < ox + TAMANHO_OBSTACULO and
                y + TAMANHO_QUADRADO > oy and y < oy + TAMANHO_OBSTACULO):
                fim_de_jogo = True

        # Mostra placar lateral
        mostrar_pontuacao(pontos)

        pygame.display.update()

        # Quando come a comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, LARGURA_JOGO - TAMANHO_QUADRADO) / 20.0) * 20
            comida_y = round(random.randrange(0, ALTURA - TAMANHO_QUADRADO) / 20.0) * 20
            tamanho_cobra += 1
            pontos += 1
            velocidade += 0.2

            # A cada 20 pontos, adiciona um obstáculo grande
            if pontos % 20 == 0:
                obstaculos.append(gerar_obstaculo())

        clock.tick(velocidade)

# Inicia o jogo
jogo()
pygame.quit()
