# plasma.py
import pygame
from collections import deque

TAMANHO_BLOCO = 50


class Plasma:

    def __init__(self):
        self.ativo = False
        self.mapa_atual = None
        self.linhas = 0
        self.colunas = 0

        self.celulas = set()        
        self.fronteira = deque()    

        self.intervalo_expansao = 0.18 
        self.tempo_pulso = 0.0

    
    def iniciar(self, mapa_atual, pos_jogador_px):
        self.mapa_atual = mapa_atual
        self.linhas = len(mapa_atual)
        self.colunas = len(mapa_atual[0])

        self.celulas.clear()
        self.fronteira.clear()
        self.temporizador = 0.0

        col_jogador = int(pos_jogador_px[0] // TAMANHO_BLOCO)
        linha_jogador = int(pos_jogador_px[1] // TAMANHO_BLOCO)

        origem = self._encontrar_ponto_mais_distante(linha_jogador, col_jogador)

        if origem:
            self.celulas.add(origem)
            self.fronteira.append(origem)
            self.ativo = True
        else:
            self.ativo = False

    def desativar(self):
        self.ativo = False
        self.celulas.clear()
        self.fronteira.clear()

    def definir_velocidade(self, intervalo_segundos: float):
        
        self.intervalo_expansao = intervalo_segundos

   
    def _eh_livre(self, linha, col):
        if 0 <= linha < self.linhas and 0 <= col < self.colunas:
            return self.mapa_atual[linha][col] != 1  
        return False

    def _encontrar_ponto_mais_distante(self, linha_ini, col_ini):
        
        visitado = {(linha_ini, col_ini)}
        fila = deque([(linha_ini, col_ini)])
        mais_distante = (linha_ini, col_ini)

        while fila:
            linha, col = fila.popleft()
            mais_distante = (linha, col)
            for dl, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nl, nc = linha + dl, col + dc
                if (nl, nc) not in visitado and self._eh_livre(nl, nc):
                    visitado.add((nl, nc))
                    fila.append((nl, nc))

        return mais_distante if mais_distante != (linha_ini, col_ini) else None


    def atualizar(self, dt: float):
        if not self.ativo:
            return

        self.tempo_pulso += dt
        self.temporizador += dt

        while self.temporizador >= self.intervalo_expansao:
            self.temporizador -= self.intervalo_expansao
            self._expandir_uma_onda()

    def _expandir_uma_onda(self):
        """Avança uma camada do flood-fill: cada célula da fronteira contamina
        seus vizinhos livres ainda não atingidos."""
        if not self.fronteira:
            return  

        novas = []
        for _ in range(len(self.fronteira)):
            linha, col = self.fronteira.popleft()
            for dl, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nl, nc = linha + dl, col + dc
                if (nl, nc) not in self.celulas and self._eh_livre(nl, nc):
                    self.celulas.add((nl, nc))
                    novas.append((nl, nc))

        self.fronteira.extend(novas)

    
    def checar_colisao(self, rect_jogador: pygame.Rect) -> bool:
        
        if not self.ativo:
            return False

        col_ini = rect_jogador.left // TAMANHO_BLOCO
        col_fim = rect_jogador.right // TAMANHO_BLOCO
        linha_ini = rect_jogador.top // TAMANHO_BLOCO
        linha_fim = rect_jogador.bottom // TAMANHO_BLOCO

        for linha in range(linha_ini, linha_fim + 1):
            for col in range(col_ini, col_fim + 1):
                if (linha, col) in self.celulas:
                    return True
        return False

   
    def desenhar(self, tela: pygame.Surface):
        if not self.ativo:
            return

        pulso = int((abs((self.tempo_pulso * 3.0) % 2.0 - 1.0)) * 70)
        cor_nucleo = (200, 0, 90)
        cor_borda = (255, 60 + pulso, 170 + pulso // 2)

        bordas = self._obter_bordas()

        for (linha, col) in self.celulas:
            x = col * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO
            rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

            if (linha, col) in bordas:
                pygame.draw.rect(tela, cor_borda, rect)
                pygame.draw.rect(tela, (255, 255, 255), rect, 2)
            else:
                pygame.draw.rect(tela, cor_nucleo, rect)

    def _obter_bordas(self):
        
        bordas = set()
        for (linha, col) in self.celulas:
            for dl, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if self._eh_livre(linha + dl, col + dc) and (linha + dl, col + dc) not in self.celulas:
                    bordas.add((linha, col))
                    break
        return bordas
