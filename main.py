#main.py
import pygame
import sys
import math 
from personagem import Jogador
from inimigos import Inimigo
from efeitos import EfeitoRastro
import map

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("core-sync: mask edition")
RELOGIO = pygame.time.Clock()

map.inicializar_iluminacao(LARGURA, ALTURA)

# --- PALETA DE CORES ROXA & NEON PROFISSIONAL ---
COR_FUNDO = (10, 10, 18)          
COR_TEXTO = (240, 240, 255)       
COR_ROXO_NEON = (180, 50, 255)    
COR_ROXO_ESCURO = (32, 24, 48)     
COR_ROXO_HOVER = (120, 40, 220)   
COR_MOLDURA_ARCADE = (45, 30, 70)

# Configuração de Fontes com anti-aliasing e peso consistentes
FONTE_TITULO = pygame.font.SysFont("Impact", 85) 
FONTE_MENU = pygame.font.SysFont("Lucida Console", 20, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Consolas", 16, bold=True)

# Layout dos Botões (Estilo Painel de Navegação)
botao_jogar = pygame.Rect(LARGURA // 2 - 150, 270, 300, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 150, 350, 300, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 150, 430, 300, 50)

# Instanciação das entidades (Física clássica original restaurada)
jogador = Jogador(55.0, 55.0, 40)
inimigos = Inimigo(505.0, 455.0, 40)
gerenciador_efeitos = EfeitoRastro() 

lista_paredes_do_seu_mapa = map.carregar_mapa()

estado_jogo = "MENU"
rodando = True
tempo_animacao = 0 

def desenhar_linhas_tecnologicas():
    """Desenha detalhes de fundo e linhas angulares de alta tecnologia no menu."""
    # Linhas de grade sutis
    for x in range(0, LARGURA, 40):
        pygame.draw.line(TELA, (18, 15, 28), (x, 0), (x, ALTURA), 1)
    for y in range(0, ALTURA, 40):
        pygame.draw.line(TELA, (18, 15, 28), (0, y), (LARGURA, y), 1)
    
    # Molduras de canto estilizadas (Estilo interface hacker/cyberpunk)
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
    
    # Corpo do botão
    pygame.draw.rect(TELA, cor_fundo, retangulo, border_radius=6)
    pygame.draw.rect(TELA, cor_borda, retangulo, width=2, border_radius=6)
    
    # Se o mouse estiver em cima, desenha pequenas setas/colchetes neon nas pontas
    if colidindo:
        # Colchete esquerdo
        pygame.draw.rect(TELA, COR_ROXO_NEON, (retangulo.x - 15, retangulo.y + 15, 4, 20))
        # Colchete direito
        pygame.draw.rect(TELA, COR_ROXO_NEON, (retangulo.right + 11, retangulo.y + 15, 4, 20))
        
    desenhar_texto(texto, FONTE_MENU, COR_TEXTO, retangulo.centerx, retangulo.centery)

def desenhar_hud_jogo():
    """Desenha uma moldura e uma barra superior para deixar a gameplay com cara de produto final."""
    # Painel do topo
    pygame.draw.rect(TELA, (15, 12, 24), (0, 0, LARGURA, 40))
    pygame.draw.line(TELA, COR_ROXO_NEON, (0, 40), (LARGURA, 40), 2)
    
    # Textos informativos estilizados na barra
    desenhar_texto("MÉTODO: GEOMÉTRICO", FONTE_PEQUENA, COR_ROXO_HOVER, 120, 20)
    desenhar_texto("STATUS: ATIVO", FONTE_PEQUENA, (0, 255, 150), LARGURA - 100, 20)

# --- GAME LOOP ---
while rodando:
    # Mantém o FPS cravado a 60 estável (Física clássica estável)
    RELOGIO.tick(60) 
    tempo_animacao += 0.05 
    posicao_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU":
                if botao_jogar.collidepoint(posicao_mouse):
                    jogador.x, jogador.y = 55.0, 55.0
                    jogador.direcao_x, jogador.direcao_y = 0, 0
                    jogador.buffer_x, jogador.buffer_y = 0, 0
                    inimigos.x, inimigos.y = 505.0, 455.0
                    inimigos.estado = "PATRULHA"
                    gerenciador_efeitos.rastros.clear() 
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
        
        # Pulsação sutil e elegante do título principal
        oscilacao = int((math.sin(tempo_animacao * 1.5) + 1) * 20)
        cor_titulo = (140 + oscilacao, 50, 255)
        
        # Sombra estilizada de deslocamento
        desenhar_texto("CORE_SYNC", FONTE_TITULO, (40, 20, 80), LARGURA // 2 + 5, 135)
        desenhar_texto("CORE_SYNC", FONTE_TITULO, cor_titulo, LARGURA // 2, 130)
        
        # Linhas decorativas abaixo do título
        pygame.draw.line(TELA, COR_ROXO_NEON, (LARGURA//2 - 180, 195), (LARGURA//2 + 180, 195), 2)
        desenhar_texto("::: M A S K   E D I T I O N :::", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, 215)
        
        # Renderização dos botões profissionais
        desenhar_botao_profissional(botao_jogar, "[ ACESSAR CORE ]", posicao_mouse)
        desenhar_botao_profissional(botao_creditos, "[ CONFIG / CRÉDITOS ]", posicao_mouse)
        desenhar_botao_profissional(botao_sair, "[ DESCONECTAR ]", posicao_mouse)
        
    elif estado_jogo == "JOGANDO":
        # --- PROCESSAMENTO LÓGICO HISTÓRICO ---
        # Removido completamente o Delta Time para manter sua física e velocidade originais intactas
        jogador.mover(LARGURA, ALTURA, lista_paredes_do_seu_mapa, gerenciador_efeitos)
        inimigos.atualizar_ia(LARGURA, ALTURA, lista_paredes_do_seu_mapa, jogador)
        
        if inimigos.checar_colisao(jogador):
            estado_jogo = "MENU"
        
        # --- PROCESSAMENTO GRÁFICO ---
        map.desenhar_mapa(TELA)
        
        # Atualização clássica do rastro (Sem os fragmentos estourando)
        # Se o seu efeitos.py pede o parâmetro dt na assinatura, mude a chamada abaixo para usar apenas 'atualizar_e_desenhar(TELA)' tirando o parâmetro interno
        try:
            gerenciador_efeitos.atualizar_e_desenhar(TELA)
        except TypeError:
            gerenciador_efeitos.atualizar_e_desenhar(TELA, 1/60)

        jogador.desenhar(TELA)
        inimigos.desenhar(TELA)
        map.aplicar_iluminacao_pro(TELA, jogador.obter_rect().center)
        
        # Interface de jogo integrada (HUD)
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
        
        # Texto auxiliar piscante usando cosseno
        alfa = int((math.cos(tempo_animacao * 2) + 1) * 75) + 105
        desenhar_texto("Pressione ESC para retornar ao painel", FONTE_PEQUENA, (alfa, alfa, 255), LARGURA // 2, 440)
        
    pygame.display.flip()

pygame.quit()
sys.exit()
