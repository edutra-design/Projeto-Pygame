#main.py
import pygame
import sys
import math # 🔥 Importado para fazer o efeito de pulsação neon
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

# --- PALETA DE CORES ROXA & NEON ULTRA-CORRIGIDA ---
COR_FUNDO = (10, 10, 18)          # Roxo escuro profundo (fundo do mapa)
COR_TEXTO = (240, 240, 255)       # Branco gelo azulado
COR_ROXO_NEON = (180, 50, 255)    # Roxo principal brilhante
COR_ROXO_ESCURO = (40, 30, 60)     # Fundo dos botões em repouso
COR_ROXO_HOVER = (100, 40, 180)   # Cor de transição do botão (borda)

FONTE_TITULO = pygame.font.SysFont("Impact", 80) # Fonte mais robusta para jogos arcades
FONTE_MENU = pygame.font.SysFont("Arial", 24, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 18)

# Botões centralizados e mais elegantes (estilo barra comprida)
botao_jogar = pygame.Rect(LARGURA // 2 - 140, 260, 280, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 140, 340, 280, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 140, 420, 280, 50)

# Instanciação
jogador = Jogador(55.0, 55.0, 36)
inimigos = Inimigo(500.0, 450.0, 36)
gerenciador_efeitos = EfeitoRastro() 

lista_paredes_do_seu_mapa = map.carregar_mapa()

estado_jogo = "MENU"
rodando = True
tempo_menu = 0 # 🔥 Contador para animações matemáticas (seno/cosseno)

def desenhar_grade_fundo():
    """Desenha linhas de grade roxas bem escuras e sutis para dar profundidade ao menu."""
    espacamento = 50
    for x in range(0, LARGURA, espacamento):
        pygame.draw.line(TELA, (20, 15, 35), (x, 0), (x, ALTURA), 1)
    for y in range(0, ALTURA, espacamento):
        pygame.draw.line(TELA, (20, 15, 35), (0, y), (LARGURA, y), 1)

def desenhar_texto(texto: str, fonte: pygame.font.Font, cor: tuple, x: int, y: int):
    imagem_texto = fonte.render(texto, True, cor)
    TELA.blit(imagem_texto, imagem_texto.get_rect(center=(x, y)))

def desenhar_botao_neon(retangulo: pygame.Rect, texto: str, posicao_mouse: tuple):
    """Desenha botões modernos com preenchimento escuro e bordas que brilham no hover."""
    colidindo = retangulo.collidepoint(posicao_mouse)
    
    # Se o mouse estiver em cima, o botão ganha um fundo levemente mais claro e borda viva
    cor_fundo_atual = (50, 35, 75) if colidindo else COR_ROXO_ESCURO
    cor_borda_atual = COR_ROXO_NEON if colidindo else COR_ROXO_HOVER
    largura_borda = 3 if colidindo else 1
    
    # Desenha preenchimento do botão
    pygame.draw.rect(TELA, cor_fundo_atual, retangulo, border_radius=12)
    # Desenha contorno neon
    pygame.draw.rect(TELA, cor_borda_atual, retangulo, width=largura_borda, border_radius=12)
    
    # Desloca o texto um pouco para cima se estiver no hover (efeito de clique/feedback visual)
    offset_y = -2 if colidindo else 0
    desenhar_texto(texto, FONTE_MENU, COR_TEXTO, retangulo.centerx, retangulo.centery + offset_y)

# --- GAME LOOP ---
while rodando:
    RELOGIO.tick(60)
    tempo_menu += 0.05 # Incrementa o tempo para as animações
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
                    inimigos.x, inimigos.y = 500.0, 450.0
                    inimigos.estado = "PATRULHA"
                    gerenciador_efeitos.rastros.clear() 
                    gerenciador_efeitos.particulas.clear() 
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
        desenhar_grade_fundo()
        
        # 🔥 EFEITO DE PULSAÇÃO NEON NO TÍTULO (Glow dinâmico usando math.sin)
        pulsacao = int((math.sin(tempo_menu * 2) + 1) * 30) # Varia de 0 a 60
        cor_titulo_glow = (120 + pulsacao, 50, 255) # Modifica o canal vermelho dinamicamente
        
        # Sombra estilizada roxa atrás do título
        desenhar_texto("CORE - SYNC", FONTE_TITULO, (60, 20, 110), LARGURA // 2 + 4, 134)
        # Título Principal brilhante
        desenhar_texto("CORE - SYNC", FONTE_TITULO, cor_titulo_glow, LARGURA // 2, 130)
        
        # Rodapé decorativo estilo Cyberpunk
        desenhar_texto("MASK EDITION", FONTE_PEQUENA, COR_ROXO_NEON, LARGURA // 2, 185)
        
        # Desenha os botões renovados
        desenhar_botao_neon(botao_jogar, "INICIAR JOGO", posicao_mouse)
        desenhar_botao_neon(botao_creditos, "CRÉDITOS", posicao_mouse)
        desenhar_botao_neon(botao_sair, "SAIR DO JOGO", posicao_mouse)
        
    elif estado_jogo == "JOGANDO":
        # --- PROCESSAMENTO LOGICO ---
        jogador.mover(LARGURA, ALTURA, lista_paredes_do_seu_mapa, gerenciador_efeitos)
        inimigos.atualizar_ia(LARGURA, ALTURA, lista_paredes_do_seu_mapa, jogador)
        
        if inimigos.checar_colisao(jogador):
            estado_jogo = "MENU"
        
        # --- PROCESSAMENTO GRÁFICO (ORDEM DE CAMADAS) ---
        map.desenhar_mapa(TELA)
        gerenciador_efeitos.atualizar_e_desenhar(TELA)
        jogador.desenhar(TELA)
        inimigos.desenhar(TELA)
        map.aplicar_iluminacao_pro(TELA, jogador.obter_rect().center)
        
        desenhar_texto("ESC para voltar", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, ALTURA - 25)
        
    elif estado_jogo == "CREDITOS":
        desenhar_grade_fundo()
        # Caixa de vidro roxa para emoldurar os créditos
        moldura_creditos = pygame.Rect(LARGURA // 2 - 300, 100, 600, 400)
        pygame.draw.rect(TELA, COR_ROXO_ESCURO, moldura_creditos, border_radius=15)
        pygame.draw.rect(TELA, COR_ROXO_NEON, moldura_creditos, width=2, border_radius=15)
        
        desenhar_texto("CRÉDITOS", FONTE_TITULO, COR_ROXO_NEON, LARGURA // 2, 170)
        desenhar_texto("Desenvolvido por:", FONTE_MENU, COR_TEXTO, LARGURA // 2, 260)
        desenhar_texto("Ana Cândida, Emilly Vitória e Júlia Dutra", FONTE_MENU, (180, 180, 220), LARGURA // 2, 310)
        
        # Texto piscante para instrução de saída do menu
        alfa_esc = int((math.sin(tempo_menu * 3) + 1) * 50) + 150
        desenhar_texto("Pressione ESC para voltar ao Menu", FONTE_PEQUENA, (alfa_esc, alfa_esc, 255), LARGURA // 2, 440)
        
    pygame.display.flip()

pygame.quit()
sys.exit()
