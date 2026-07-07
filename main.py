# main.py
import pygame
import sys
import math 
from personagem import Jogador
from inimigos import Inimigo
from efeitos import EfeitoRastro
import map  # Usaremos o seu map.py diretamente

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("core-sync: mask edition")
RELOGIO = pygame.time.Clock()

map.inicializar_iluminacao(LARGURA, ALTURA)

COR_FUNDO = (10, 10, 18)          
COR_TEXTO = (240, 240, 255)       
COR_ROXO_NEON = (180, 50, 255)    
COR_ROXO_ESCURO = (32, 24, 48)     
COR_ROXO_HOVER = (120, 40, 220)   
COR_MOLDURA_ARCADE = (45, 30, 70)

FONTE_TITULO = pygame.font.SysFont("Impact", 85) 
FONTE_MENU = pygame.font.SysFont("Lucida Console", 20, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Consolas", 16, bold=True)

botao_jogar = pygame.Rect(LARGURA // 2 - 150, 270, 300, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 150, 350, 300, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 150, 430, 300, 50)

# Inicialização dos objetos do jogo
jogador = Jogador(55.0, 55.0, 40)
inimigos = Inimigo(505.0, 455.0, 40)
gerenciador_efeitos = EfeitoRastro() 

fase_atual = 1
# Correção: Buscando a função diretamente do seu módulo 'map'
lista_paredes_do_seu_mapa = map.carregar_fase(fase_atual)
rect_portal = pygame.Rect(0, 0, 0, 0)

estado_jogo = "MENU"
rodando = True
tempo_animacao = 0 

def atualizar_posicao_portal():
    """Encontra o bloco do portal (tipo 6) na matriz atual e gera seu Rect de colisão."""
    global rect_portal
    for linha_idx, linha in enumerate(map.MAPA_ATUAL):
        for col_idx, tipo in enumerate(linha):
            if tipo == 6:
                x = col_idx * map.TAMANHO_BLOCO
                y = linha_idx * map.TAMANHO_BLOCO
                rect_portal = pygame.Rect(x, y, map.TAMANHO_BLOCO, map.TAMANHO_BLOCO)
                return
    # Caso não encontre portal na fase, joga para fora da tela
    rect_portal = pygame.Rect(-100, -100, 0, 0)

def desenhar_linhas_tecnologicas():
    """Desenha detalhes de fundo e linhas angulares de alta tecnologia no menu."""
    for x in range(0, LARGURA, 40):
        pygame.draw.line(TELA, (18, 15, 28), (x, 0), (x, ALTURA), 1)
    for y in range(0, ALTURA, 40):
        pygame.draw.line(TELA, (18, 15, 28), (0, y), (LARGURA, y), 1)
    
    pygame.draw.rect(TELA, COR_ROXO_NEON, (20, 20, 30, 4), border_radius=2)
    pygame.draw.rect(TELA, COR_ROXO_NEON, (20, 20, 4, 30), border_radius=2)
    pygame.draw.rect(TELA, COR_ROXO_NEON, (LARGURA - 50, 20, 30, 4), border_radius=2)
    pygame.draw.rect(TELA, COR_ROXO_NEON, (LARGURA - 24, 20, 4, 30), border_radius=2)

def desenhar_texto(texto: str, fonte: pygame.font.Font, cor: tuple, x: int, y: int):
    imagem_texto = fonte.render(texto, True, cor)
    TELA.blit(imagem_texto, imagem_texto.get_rect(center=(x, y)))

def desenhar_botao_profissional(retangulo: pygame.Rect, texto: str, posicao_mouse: tuple):
    """Desenha botões minimalistas profissionais com indicadores de seleção nas laterais."""
    colidindo = retangulo.collidepoint(posicao_mouse)
    
    cor_fundo = COR_ROXO_ESCURO if not colidindo else (45, 32, 68)
    cor_borda = COR_ROXO_HOVER if not colidindo else COR_ROXO_NEON
    
    pygame.draw.rect(TELA, cor_fundo, retangulo, border_radius=6)
    pygame.draw.rect(TELA, cor_borda, retangulo, width=2, border_radius=6)
    
    if colidindo:
        pygame.draw.rect(TELA, COR_ROXO_NEON, (retangulo.x - 15, retangulo.y + 15, 4, 20))
        pygame.draw.rect(TELA, COR_ROXO_NEON, (retangulo.right + 11, retangulo.y + 15, 4, 20))
        
    desenhar_texto(texto, FONTE_MENU, COR_TEXTO, retangulo.centerx, retangulo.centery)

def desenhar_hud_jogo():
    """Desenha uma moldura e uma barra superior com informações do estado do jogo."""
    pygame.draw.rect(TELA, (15, 12, 24), (0, 0, LARGURA, 40))
    pygame.draw.line(TELA, COR_ROXO_NEON, (0, 40), (LARGURA, 40), 2)
    
    desenhar_texto(f"FASE: {fase_atual} / 3", FONTE_PEQUENA, COR_TEXTO, 60, 20)
    desenhar_texto("MÉTODO: GEOMÉTRICO", FONTE_PEQUENA, COR_ROXO_HOVER, LARGURA // 2, 20)
    desenhar_texto("STATUS: ATIVO", FONTE_PEQUENA, (0, 255, 150), LARGURA - 100, 20)

def iniciar_fase(numero_da_fase):
    global lista_paredes_do_seu_mapa, fase_atual
    
    retorno_fase = map.carregar_fase(numero_da_fase)
    
    if retorno_fase is None:
        # Se carregar_fase retornar None, significa que as fases acabaram
        estado_jogo = "CREDITOS"
        return

    fase_atual = numero_da_fase
    lista_paredes_do_seu_mapa = retorno_fase
    atualizar_posicao_portal()

    # Resetando as mecânicas do jogador para a nova fase
    jogador.x, jogador.y = 55.0, 55.0
    jogador.direcao_x, jogador.direcao_y = 0, 0
    if hasattr(jogador, 'buffer_x'):
        jogador.buffer_x, jogador.buffer_y = 0, 0

    # Configuração de posição inicial do inimigo na fase
    if fase_atual == 1:
        inimigos.x, inimigos.y = 505.0, 455.0
    elif fase_atual == 2:
        inimigos.x, inimigos.y = 350.0, 350.0
    elif fase_atual == 3:
        inimigos.x, inimigos.y = 700.0, 500.0

    inimigos.estado = "PATRULHA"
    gerenciador_efeitos.rastros.clear()
    if hasattr(gerenciador_efeitos, 'particulas'):
        gerenciador_efeitos.particulas.clear()

# Inicializa a primeira localização do portal antes do loop começar
atualizar_posicao_portal()

while rodando:
    RELOGIO.tick(60) 
    tempo_animacao += 0.05 
    posicao_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU":
                if botao_jogar.collidepoint(posicao_mouse):
                    iniciar_fase(1)  # Começa sempre da fase 1 ao clicar em Jogar
                    estado_jogo = "JOGANDO"
                elif botao_creditos.collidepoint(posicao_mouse):
                    estado_jogo = "CREDITOS"
                elif botao_sair.collidepoint(posicao_mouse):
                    rodando = False
                        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if estado_jogo in ("JOGANDO", "CREDITOS"):
                    estado_jogo = "MENU"
                    
    TELA.fill(COR_FUNDO)
    
    if estado_jogo == "MENU":
        desenhar_linhas_tecnologicas()
        
        oscilacao = int((math.sin(tempo_animacao * 1.5) + 1) * 20)
        cor_titulo = (140 + oscilacao, 50, 255)
        
        desenhar_texto("CORE_SYNC", FONTE_TITULO, (40, 20, 80), LARGURA // 2 + 5, 135)
        desenhar_texto("CORE_SYNC", FONTE_TITULO, cor_titulo, LARGURA // 2, 130)
        
        pygame.draw.line(TELA, COR_ROXO_NEON, (LARGURA//2 - 180, 195), (LARGURA//2 + 180, 195), 2)
        desenhar_texto("::: M A S K   E D I T I O N :::", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, 215)
        
        desenhar_botao_profissional(botao_jogar, "[ ACESSAR CORE ]", posicao_mouse)
        desenhar_botao_profissional(botao_creditos, "[ CONFIG / CRÉDITOS ]", posicao_mouse)
        desenhar_botao_profissional(botao_sair, "[ DESCONECTAR ]", posicao_mouse)
        
    elif estado_jogo == "JOGANDO":
        # Movimentação e IA passando a lista de colisões correta da fase atual
        jogador.mover(LARGURA, ALTURA, lista_paredes_do_seu_mapa, gerenciador_efeitos)
        inimigos.atualizar_ia(LARGURA, ALTURA, lista_paredes_do_seu_mapa, jogador)
        
        # Game over básico (retorna ao Menu)
        if inimigos.checar_colisao(jogador):
            estado_jogo = "MENU"
        
        # Verificação de mudança de fase ao tocar no Portal
        rect_jogador = jogador.obter_rect()
        if rect_jogador.colliderect(rect_portal):
            if fase_atual < 3:
                iniciar_fase(fase_atual + 1)
            else:
                estado_jogo = "CREDITOS" # Fim do jogo (passou da fase 3)
        
        # Renderização visual respeitando a ordem de camadas
        map.desenhar_mapa(TELA)
        
        try:
            gerenciador_efeitos.atualizar_e_desenhar(TELA)
        except TypeError:
            gerenciador_efeitos.atualizar_e_desenhar(TELA, 1/60)

        jogador.desenhar(TELA)
        inimigos.desenhar(TELA)
        
        # Efeito visual de iluminação dinâmica focado no jogador
        map.aplicar_iluminacao_pro(TELA, jogador.obter_rect().center)
        
        desenhar_hud_jogo()
        desenhar_texto("Pressione ESC para ejetar", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, ALTURA - 25)
        
    elif estado_jogo == "CREDITOS":
        desenhar_linhas_tecnologicas()
        
        moldura_creditos = pygame.Rect(LARGURA // 2 - 280, 120, 560, 360)
        pygame.draw.rect(TELA, COR_ROXO_ESCURO, moldura_creditos, border_radius=8)
        pygame.draw.rect(TELA, COR_ROXO_NEON, moldura_creditos, width=2, border_radius=8)
        
        desenhar_texto("REGISTRO DE DESENVOLVIMENTO", FONTE_MENU, COR_ROXO_NEON, LARGURA // 2, 170)
        
        pygame.draw.line(TELA, COR_ROXO_HOVER, (LARGURA//2 - 200, 210), (LARGURA//2 + 200, 210), 1)
        
        desenhar_texto("EQUIPE CORE:", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, 250)
        desenhar_texto("Ana Cândida", FONTE_MENU, COR_TEXTO, LARGURA // 2, 290)
        desenhar_texto("Emilly Vitória", FONTE_MENU, COR_TEXTO, LARGURA // 2, 330)
        desenhar_texto("Júlia Dutra", FONTE_MENU, COR_TEXTO, LARGURA // 2, 370)
        
        alfa = int((math.cos(tempo_animacao * 2) + 1) * 75) + 105
        desenhar_texto("Pressione ESC para retornar ao painel", FONTE_PEQUENA, (alfa, alfa, 255), LARGURA // 2, 440)
        
    pygame.display.flip()

pygame.quit()
sys.exit()
