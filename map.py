# mapa.py
import pygame

TAMANHO_BLOCO = 50

# Matriz do Mapa
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
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
# Nota: Aumentei levemente a largura para 16 colunas para fechar os 800px de largura da sua tela (16 * 50 = 800)

CORES_BLOCOS = {
    0: (18, 18, 26),     # Chão (Quase preto, combinando com o fundo do seu menu)
    1: (45, 40, 65),     # Parede/Obstáculo (Roxo escuro acinzentado)
    4: (255, 215, 0),    # Moeda/Item (Dourado)
    5: (0, 100, 200),    # Água/Lentidão (Azul escuro)
    6: (180, 50, 255)    # Saída/Portal (Roxo Neon)
}

def carregar_mapa():
    """Gera a lista de blocos de colisão e a lista de itens do mapa."""
    paredes = []
    # Se quiser criar mecânicas para moedas ou água depois, pode rastrear aqui
    
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            if tipo == 1: # Se for parede
                x = col_idx * TAMANHO_BLOCO
                y = linha_idx * TAMANHO_BLOCO
                paredes.append(pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                
    return paredes

def desenhar_mapa(tela: pygame.Surface):
    """Renderiza visualmente o mapa na tela."""
    for linha_idx, linha in enumerate(MAPA):
        for col_idx, tipo in enumerate(linha):
            x = col_idx * TAMANHO_BLOCO
            y = linha_idx * TAMANHO_BLOCO
            rect_bloco = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
            
            # Pega a cor correspondente (se for jogador (3) ou inimigo (2), desenha chão comum por baixo)
            cor = CORES_BLOCOS.get(tipo, CORES_BLOCOS[0])
            
            pygame.draw.rect(tela, cor, rect_bloco)
            
            # Desenha uma borda estética neon suave para as paredes
            if tipo == 1:
                pygame.draw.rect(tela, (100, 40, 180), rect_bloco, 1)
