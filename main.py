#main.py
import pygame
import sys
from personagem import Jogador
from inimigos import Inimigo
from efeitos import EfeitoRastro 
import map # 🔥 IMPORTA O SEU NOVO ARQUIVO DE MAPA

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("core-sync: mask edition")
RELOGIO = pygame.time.Clock()

COR_FUNDO = (12, 12, 18)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (40, 40, 55)
COR_BOTAO_HOVER = (120, 50, 240)

FONTE_TITULO = pygame.font.SysFont("Arial", 60, bold=True)
FONTE_MENU = pygame.font.SysFont("Arial", 30)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 20)

botao_jogar = pygame.Rect(LARGURA // 2 - 100, 250, 200, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 100, 330, 200, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 100, 410, 200, 50)

# Instanciação das Entidades e do Gerenciador de Efeitos
# 💡 Ajustei o tamanho para 38 para o jogador e inimigo caberem e se moverem livremente dentro dos blocos de 50
jogador = Jogador(55.0, 55.0, 38) 
inimigos = Inimigo(500.0, 400.0, 38)
gerenciador_efeitos = EfeitoRastro() 

# 🔥 CARREGA AS COLISÕES BASEADO NA MATRIZ DO MAPA
lista_paredes_do_seu_mapa = map.carregar_mapa()

estado_jogo = "MENU"
rodando = True

def desenhar_texto(texto: str, fonte: pygame.font.Font, cor: tuple, x: int, y: int):
    imagem_texto = fonte.render(texto, True, cor)
    TELA.blit(imagem_texto, imagem_texto.get_rect(center=(x, y)))

def desenhar_botao(retangulo: pygame.Rect, texto: str, posicao_mouse: tuple):
    cor_atual = COR_BOTAO_HOVER if retangulo.collidepoint(posicao_mouse) else COR_BOTAO
    pygame.draw.rect(TELA, cor_atual, retangulo, border_radius=8)
    pygame.draw.rect(TELA, (180, 50, 255), retangulo, width=2, border_radius=8)
    desenhar_texto(texto, FONTE_MENU, COR_TEXTO, retangulo.centerx, retangulo.centery)

# --- GAME LOOP ---
while rodando:
    RELOGIO.tick(60)
    posicao_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU":
                if botao_jogar.collidepoint(posicao_mouse):
                    # Reinicia posições dentro do primeiro bloco livre do mapa
                    jogador.x, jogador.y = 55.0, 55.0
                    jogador.direcao_x, jogador.direcao_y = 0, 0
                    jogador.buffer_x, jogador.buffer_y = 0, 0
                    inimigos.x, inimigos.y = 500.0, 400.0
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
        desenhar_texto("CORE-SYNC", FONTE_TITULO, (180, 50, 255), LARGURA // 2, 130)
        desenhar_botao(botao_jogar, "JOGAR", posicao_mouse)
        desenhar_botao(botao_creditos, "CRÉDITOS", posicao_mouse)
        desenhar_botao(botao_sair, "SAIR", posicao_mouse)
        
    elif estado_jogo == "JOGANDO":
        # --- PROCESSAMENTO LOGICO ---
        jogador.mover(LARGURA, ALTURA, lista_paredes_do_seu_mapa, gerenciador_efeitos)
        inimigos.atualizar_ia(LARGURA, ALTURA, lista_paredes_do_seu_mapa, jogador)
        
        if inimigos.checar_colisao(jogador):
            estado_jogo = "MENU"
        
        # --- PROCESSAMENTO GRÁFICO (ORDEM DE CAMADAS) ---
        # 1. 🔥 DESENHA O MAPA NO FUNDO
        map.desenhar_mapa(TELA)
        
        # 2. ATUALIZA E DESENHA O RASTRO/PLASMA (Fica na frente do chão, mas atrás do jogador)
        gerenciador_efeitos.atualizar_e_desenhar(TELA)
        
        # 3. Desenha as entidades na camada superior
        jogador.desenhar(TELA)
        inimigos.desenhar(TELA)
        
        desenhar_texto("ESC para voltar", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, ALTURA - 25)
        
    elif estado_jogo == "CREDITOS":
        desenhar_texto("CRÉDITOS", FONTE_TITULO, COR_TEXTO, LARGURA // 2, 150)
        desenhar_texto("Desenvolvido por: Ana Cândida, Emilly Vitória e Júlia Dutra", FONTE_MENU, (200, 200, 200), LARGURA // 2, ALTURA // 2 - 20)
        desenhar_texto("Pressione ESC para voltar ao Menu", FONTE_MENU, COR_TEXTO, LARGURA // 2, ALTURA // 2 + 120)
        
    pygame.display.flip()

pygame.quit()
sys.exit()
