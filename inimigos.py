import pygame
import random
from personagem import Entidade

class Inimigo(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (255, 50, 50)) # Vermelho Neon
        self.velocidade_patrulha = 3.0
        self.velocidade_investida = 8.0
        self.estado = "PATRULHA"
        self.direcao_x, self.direcao_y = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def atualizar_ia(self, largura_tela: int, altura_tela: int, lista_paredes: list, jogador: Entidade):
        """Gerencia patrulha e investida rápida se avistar o jogador."""
        if self.estado == "PATRULHA":
            # Visão Horizontal
            if abs(self.y - jogador.y) < self.tamanho // 2:
                dir_x = 1 if jogador.x > self.x else -1
                linha_visao = pygame.Rect(int(self.x), int(self.y), int(jogador.x - self.x), self.tamanho)
                if not any(linha_visao.colliderect(p) for p in lista_paredes):
                    self.estado = "ALERTA"
                    self.direcao_x, self.direcao_y = dir_x, 0
            # Visão Vertical
            elif abs(self.x - jogador.x) < self.tamanho // 2:
                dir_y = 1 if jogador.y > self.y else -1
                linha_visao = pygame.Rect(int(self.x), int(self.y), self.tamanho, int(jogador.y - self.y))
                if not any(linha_visao.colliderect(p) for p in lista_paredes):
                    self.estado = "ALERTA"
                    self.direcao_x, self.direcao_y = 0, dir_y

        vel = self.velocidade_investida if self.estado == "ALERTA" else self.velocidade_patrulha

        pos_antiga_x, pos_antiga_y = self.x, self.y
        self.x += self.direcao_x * vel
        self.y += self.direcao_y * vel
        
        rect_inimigo = self.obter_rect()
        colidiu = False
        
        if self.x < 0 or self.x > largura_tela - self.tamanho or self.y < 0 or self.y > altura_tela - self.tamanho:
            colidiu = True
        elif any(rect_inimigo.colliderect(p) for p in lista_paredes):
            colidiu = True

        if colidiu:
            self.x, self.y = pos_antiga_x, pos_antiga_y
            self.estado = "PATRULHA"
            if self.direcao_x != 0:
                self.direcao_x = 0
                self.direcao_y = random.choice([-1, 1])
            else:
                self.direcao_y = 0
                self.direcao_x = random.choice([-1, 1])

    def checar_colisao(self, jogador: Entidade) -> bool:
        return self.obter_rect().colliderect(jogador.obter_rect())
