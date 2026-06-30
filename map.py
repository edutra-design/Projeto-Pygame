# map.py
import pygame

TAMANHO_BLOCO = 50

Fases = { 
    
    1: [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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
    
],


    2: [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
         [1,0,1,4,0,0,0,0,0,0,0,0,4,1,0,1],
         [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
         [1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
         [1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1],
         [1,0,1,0,0,0,1,4,4,1,0,0,0,1,0,1],
         [1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1],
         [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
         [1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
] }

MAPA_ATUAL = Fases[1]

def carregar_fase(numero_fase):
    global MAPA_ATUAL

    if numero_fase in Fases:
        MAPA_ATUAL = Fases[numero_fase]
    else:
        print("Fases concluídas!")
        return None
    
    paredes = []

    for linha_idx, linha in enumerate(MAPA_ATUAL):
        for col_idx, tipo in enumerate(linha):
            if tipo ==1:
CORES = {
    "FUNDO": (10, 10, 18),          # Fundo escuro do labirinto
    "NEON_PRINCIPAL": (180, 50, 255),# Linhas roxas neon vazadas
    "NEON_TRILHA": (40, 30, 65),     # Tracinhos do chão
    "MOEDA": (255, 230, 0),         
    "AGUA": (0, 180, 255),          
    "PORTAL": (0, 255, 150)         
}

superficie_escuridao = None

def inicializar_iluminacao(largura, altura):
    global superficie_escuridao
    superficie_escuridao = pygame.Surface((largura, altura), pygame.SRCALPHA)

def carregar_mapa():
    paredes = []
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            if tipo == 1:
                x = col_idx * TAMANHO_BLOCO
                y = linha_idx * TAMANHO_BLOCO
                paredes.append(pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
    return paredes

def eh_parede(linha, col):
    if 0 <= linha < len(MAPA) and 0 <= col < len(MAPA[0]):
        return MAPA[linha][col] == 1
    return True

def desenhar_mapa(tela: pygame.Surface):
    """Desenha o labirinto usando apenas traços e linhas de estilo neon vazadas."""
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            x = col_idx * TAMANHO_BLOCO
            y = linha_idx * TAMANHO_BLOCO
            rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
            
            pygame.draw.rect(tela, CORES["FUNDO"], rect)

            # --- TRACINHOS DE TRILHA NO CHÃO VAZIO ---
            if tipo == 0 or tipo in (2, 3, 4):
                centro_x, centro_y = x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2
                pygame.draw.line(tela, CORES["NEON_TRILHA"], (centro_x - 4, centro_y), (centro_x + 4, centro_y), 1)
                pygame.draw.line(tela, CORES["NEON_TRILHA"], (centro_x, centro_y - 4), (centro_x, centro_y + 4), 1)

            if tipo == 1: # --- PAREDES SÓ COM TRACINHOS NEON ---
                cima   = eh_parede(linha_idx - 1, col_idx)
                baixo  = eh_parede(linha_idx + 1, col_idx)
                esquerda = eh_parede(linha_idx, col_idx - 1)
                direita  = eh_parede(linha_idx, col_idx + 1)
                
                if not cima:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y), (x + TAMANHO_BLOCO, y), 2)
                if not baixo:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y + TAMANHO_BLOCO - 1), (x + TAMANHO_BLOCO, y + TAMANHO_BLOCO - 1), 2)
                if not esquerda:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x, y), (x, y + TAMANHO_BLOCO), 2)
                if not direita:
                    pygame.draw.line(tela, CORES["NEON_PRINCIPAL"], (x + TAMANHO_BLOCO - 1, y), (x + TAMANHO_BLOCO - 1, y + TAMANHO_BLOCO), 2)

            elif tipo == 4: 
                centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
                pygame.draw.circle(tela, CORES["MOEDA"], centro, 4)

            elif tipo == 5: 
                pygame.draw.rect(tela, (15, 20, 35), rect)
                pygame.draw.rect(tela, CORES["AGUA"], rect, 1)

            elif tipo == 6: 
                pygame.draw.rect(tela, CORES["PORTAL"], rect, 2, border_radius=12)

def aplicar_iluminacao_pro(tela: pygame.Surface, centro_jogador: tuple):
    if superficie_escuridao is None:
        return
    superficie_escuridao.fill((8, 8, 14, 245)) 

    raio_maximo = 190
    passos = 15 
    for i in range(passos):
        raio = raio_maximo - (i * (raio_maximo // passos))
        alfa = int(245 * (i / passos))
        pygame.draw.circle(superficie_escuridao, (8, 8, 14, alfa), centro_jogador, raio)

    tela.blit(superficie_escuridao, (0, 0))
