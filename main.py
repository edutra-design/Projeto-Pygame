import pygame
import sys
from personagem import Jogador
from inimigos import Inimigo

# Inicialização obrigatória do subsistema de hardware
pygame.init()

# Configurações do Display
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("core-sync: mask edition")

# Controle de Clock e Tempo Real
RELOGIO = pygame.time.Clock()
FPS_TARGET = 60

# Diretrizes Estéticas (Paleta de Cores Avançada)
COR_FUNDO = (10, 10, 15)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (45, 45, 60)
COR_BOTAO_HOVER = (110, 40, 220)

# Alocação de Recursos de Tipografia
FONTE_TITULO = pygame.font.SysFont("Arial", 60, bold=True)
FONTE_MENU = pygame.font.SysFont("Arial", 30)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 20)

# Definição dos Retângulos de Interação da UI
botao_jogar = pygame.Rect(LARGURA // 2 - 100, 250, 200, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 100, 330, 200, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 100, 410, 200, 50)

# Instanciação das Entidades do Jogo
jogador = Jogador(40.0, 40.0, 40)
inimigos = Inimigo(400.0, 280.0, 40)

# Gerenciamento de Máquina de Estados
estado_jogo = "MENU"
rodando = True

def desenhar_texto(texto: str, fonte: pygame.font.Font, cor: tuple, x: int, y: int):
    """Auxiliar gráfico para renderização centralizada de fontes."""
    imagem_texto = fonte.render(texto, True, cor)
    TELA.blit(imagem_texto, imagem_texto.get_rect(center=(x, y)))

def desenhar_botao(retangulo: pygame.Rect, texto: str, posicao_mouse: tuple):
    """Renderiza botões de interface reativos com contornos estilizados em feedback visual."""
    cor_atual = COR_BOTAO_HOVER if retangulo.collidepoint(posicao_mouse) else COR_BOTAO
    pygame.draw.rect(TELA, cor_atual, retangulo, border_radius=8)
    pygame.draw.rect(TELA, (180, 50, 255), retangulo, width=2, border_radius=8)
    desenhar_texto(texto, FONTE_MENU, COR_TEXTO, retangulo.centerx, retangulo.centery)

# --- LOOP DE EXECUÇÃO PRINCIPAL ---
while rodando:
    # Captura o Delta Time em segundos (Tempo decorrido desde o último frame)
    dt = RELOGIO.tick(FPS_TARGET) / 1000.0
    posicao_mouse = pygame.mouse.get_pos()
    
    # --- SUBSISTEMA DE EVENTOS DE HARDWARE ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU":
                if botao_jogar.collidepoint(posicao_mouse):
                    # Reinicialização limpa de vetores e posições físicas
                    jogador.x, jogador.y = 40.0, 40.0
                    jogador.direcao_x, jogador.direcao_y = 0, 0
                    jogador.buffer_x, jogador.buffer_y = 0, 0
                    inimigos.x, inimigos.y = 400.0, 280.0
                    estado_jogo = "JOGANDO"
                elif botao_creditos.collidepoint(posicao_mouse):
                    estado_jogo = "CREDITOS"
                elif botao_sair.collidepoint(posicao_mouse):
                    rodando = False
                        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if estado_jogo in ("JOGANDO", "CREDITOS"):
                    estado_jogo = "MENU"
                    
    # --- SUBSISTEMA DE PROCESSAMENTO GRÁFICO ---
    TELA.fill(COR_FUNDO)
    
    if estado_jogo == "MENU":
        desenhar_texto("CORE-SYNC", FONTE_TITULO, (180, 50, 255), LARGURA // 2, 130)
        desenhar_botao(botao_jogar, "JOGAR", posicao_mouse)
        desenhar_botao(botao_creditos, "CRÉDITOS", posicao_mouse)
        desenhar_botao(botao_sair, "SAIR", posicao_mouse)
        
    elif estado_jogo == "JOGANDO":
        # ⚠️ INTEGRAÇÃO COM SEU PROJETO: Atribua aqui a lista de Rects do SEU módulo de mapa
        lista_paredes_do_seu_mapa = [] 

        # --- PROCESSAMENTO DOS SEUS MÓDULOS DE EFEITOS ---
        # [Insira aqui as chamadas do seu arquivo de efeitos, ex: seu_plasma.atualizar()]

        # --- PROCESSAMENTO DA LÓGICA DE FÍSICA ---
        jogador.mover(LARGURA, ALTURA, lista_paredes_do_seu_mapa, dt)
        inimigos.patrulhar(LARGURA, ALTURA, lista_paredes_do_seu_mapa, dt)
        
        # Processamento de condições de Game Over
        if inimigos.checar_colisao(jogador):
            estado_jogo = "MENU"
        
        # --- DESENHOS DOS SEUS ELEMENTOS VISUAIS DE MAPA ---
        # [Insira aqui a chamada para desenhar o seu mapa, ex: seu_mapa.desenhar(TELA)]
        
        # Desenho das Entidades por herança
        jogador.desenhar(TELA)
        inimigos.desenhar(TELA)
        
        desenhar_texto("ESC para voltar", FONTE_PEQUENA, COR_TEXTO, LARGURA // 2, ALTURA - 20)
        
    elif estado_jogo == "CREDITOS":
        desenhar_texto("CRÉDITOS", FONTE_TITULO, COR_TEXTO, LARGURA // 2, 150)
        desenhar_texto("Desenvolvido por: Ana Cândida, Emilly Vitória e Júlia Dutra", FONTE_MENU, (200, 200, 200), LARGURA // 2, ALTURA // 2 - 20)
        desenhar_texto("Pressione ESC para voltar ao Menu", FONTE_MENU, COR_TEXTO, LARGURA // 2, ALTURA // 2 + 120)
        
    # Envia o frame processado para o buffer da placa de vídeo / monitor
    pygame.display.flip()

# Desalocação limpa de memória
pygame.quit()
sys.exit()
