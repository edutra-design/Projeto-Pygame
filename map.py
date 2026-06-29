# mapa.py
import pygame

TAMANHO_BLOCO = 50

# Matriz do Mapa (16 colunas x 12 linhas)
MAPA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,3,0,0,0,1,0,0,0,0,2,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,0,0,1,1,1,0,1],
    [1,0,0,1,0,0,0,0,1,0,1,1,0,0,0,1],
    [1,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1],
    [1,0,0,0,0,4,1,0,1,1,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,0,0,0,0,1,1,1,0,1],
    [1,0,1,5,0,1,1,1,1,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,6,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

CORES = {
    "FUNDO": (12, 11, 20),          # Chão escuro
    "PAREDE_INTERNA": (28, 22, 41), # Estrutura interna da parede
    "NEON_PRINCIPAL": (180, 50, 255),# Roxo neon idêntico ao do menu
    "NEON_BRILHO": (95, 20, 145),   # Brilho de profundidade do neon
    "MOEDA": (255, 230, 0),         
    "AGUA": (0, 180, 255),          
    "PORTAL": (0, 255, 150)         # Verde neon para destacar a saída do roxo
}

superficie_escuridao = None

def inicializar_iluminacao(largura, altura):
    """Cria a máscara de escuridão nativamente em memória."""
    global superficie_escuridao
    superficie_escuridao = pygame.Surface((largura, altura), pygame.SRCALPHA)

def carregar_mapa():
    """Gera a lista de blocos de colisão do mapa."""
    paredes = []
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            if tipo == 1:
                x = col_idx * TAMANHO_BLOCO
                y = linha_idx * TAMANHO_BLOCO
                paredes.append(pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
    return paredes

def eh_parede(linha, col):
    """Verifica se uma coordenada específica da matriz é parede."""
    if 0 <= linha < len(MAPA) and 0 <= col < len(MAPA[0]):
        return MAPA[linha][col] == 1
    return True # Bordas externas contam como parede

def desenhar_mapa(tela: pygame.Surface):
    """Renderiza o mapa com conexões inteligentes nas paredes e detalhes avançados."""
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            x = col_idx * TAMANHO_BLOCO
            y = linha_idx * TAMANHO_BLOCO
            rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
            
            # 1. Desenho do Chão Técnico (com micro-grade)
            pygame.draw.rect(tela, CORES["FUNDO"], rect)
            pygame.draw.rect(tela, (22, 20, 32), rect, 1)

            if tipo == 1:  # --- PAREDE COM CONEXÃO INTELIGENTE ---
                pygame.draw.rect(tela, CORES["PAREDE_INTERNA"], rect)
                
                # Checa os vizinhos para saber onde desenhar as bordas neon
                cima   = eh_parede(linha_idx - 1, col_idx)
                baixo  = eh_parede(linha_idx + 1, col_idx)
                esquerda = eh_parede(linha_idx, col_idx - 1)
                direita  = eh_parede(linha_idx, col_idx + 1)
                
                # Desenha o contorno Neon Principal apenas onde NÃO há outra parede encostada
                if not cima:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y), (x + TAMANHO_BLOCO, y), 2)
                if not baixo:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y + TAMANHO_BLOCO - 1), (x + TAMANHO_BLOCO, y + TAMANHO_BLOCO - 1), 2)
                if not esquerda:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y), (x, y + TAMANHO_BLOCO), 2)
                if not direita:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x + TAMANHO_BLOCO - 1, y), (x + TAMANHO_BLOCO - 1, y + TAMANHO_BLOCO), 2)
                
                # Detalhes geométricos internos (quadradinhos de runas centrais)
                # Só desenha se for um bloco de parede isolado ou de quina para não poluir
                if not (cima and baixo and esquerda and direita):
                    centro_x, centro_y = x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2
                    pygame.draw.rect(tela, CORES["NEON_BRILHO"], (centro_x - 4, centro_y - 4, 8, 8), 1)

            elif tipo == 4: # --- MOEDAS ESTILO TOTM ---
                centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
                # Efeito de brilho losango (dois retângulos cruzados pequenos)
                pygame.draw.circle(tela, (60, 50, 0), centro, 8)
                pygame.draw.circle(tela, CORES["MOEDA"], centro, 4)

            elif tipo == 5: # --- ARMADILHA DE ÁGUA NEON ---
                pygame.draw.rect(tela, (10, 30, 60), rect)
                pygame.draw.rect(tela, CORES["AGUA"], rect, 2)
                # Ondas estilizadas estáveis por linhas
                pygame.draw.line(tela, CORES["AGUA"], (x + 5, y + 15), (x + 20, y + 15), 2)
                pygame.draw.line(tela, CORES["AGUA"], (x + 25, y + 35), (x + 45, y + 35), 2)

            elif tipo == 6: # --- PORTAL DE SAÍDA ANIT-ALINHADO ---
                pygame.draw.rect(tela, CORES["PORTAL"], rect, 2, border_radius=10)
                for r in range(4, 20, 4):
                    rect_interno = rect.inflate(-r, -r)
                    pygame.draw.rect(tela, (0, 100, 60), rect_interno, 1, border_radius=6)

def aplicar_iluminacao_pro(tela: pygame.Surface, centro_jogador: tuple):
    """Gera o efeito de lanterna degradê ao redor do jogador por código."""
    if superficie_escuridao is None:
        return
    superficie_escuridao.fill((8, 8, 14, 242)) # Vinheta escura

    raio_maximo = 190
    passos = 18 # Mais passos deixa o degradê perfeitamente suave
    for i in range(passos):
        raio = raio_maximo - (i * (raio_maximo // passos))
        alfa = int(242 * (i / passos))
        pygame.draw.circle(superficie_escuridao, (8, 8, 14, alfa), centro_jogador, raio)

    tela.blit(superficie_escuridao, (0, 0))
