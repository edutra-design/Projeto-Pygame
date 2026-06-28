import pygame
import random
from personagem import Entidade

class Inimigo(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (255, 50, 50))
        self.velocidade = 240.0  # Pixels por segundo
        
        # Inicia patrulhando em um eixo aleatório
        self.direcao_x, self.direcao_y = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def patrulhar(self, largura_tela: int, altura_tela: int, lista_paredes: list, dt: float):
        """Realiza patrulha retilínea contínua, alterando a rota de forma perpendicular sob impacto."""
        passo_x = self.direcao_x * self.velocidade * dt
        passo_y = self.direcao_y * self.velocidade * dt
        colidiu = False

        # Processamento físico no eixo X
        if passo_x != 0:
            self.x += passo_x
            rect_atual = self.obter_rect()
            if self.x < 0 or self.x > largura_tela - self.tamanho:
                colidiu = True
            else:
                for parede in lista_paredes:
                    if rect_atual.colliderect(parede):
                        colidiu = True
                        break
            if colidiu:
                self.x -= passo_x  # Desfaz o passo para não entrar no bloco
                self._rotacionar_direcao()

        # Processamento físico no eixo Y
        elif passo_y != 0:
            self.y += passo_y
            rect_atual = self.obter_rect()
            if self.y < 0 or self.y > altura_tela - self.tamanho:
                colidiu = True
            else:
                for parede in lista_paredes:
                    if rect_atual.colliderect(parede):
                        colidiu = True
                        break
            if colidiu:
                self.y -= passo_y  # Desfaz o passo
                self._rotacionar_direcao()

    def _rotacionar_direcao(self):
        """Altera a direção do movimento em 90 graus (eixo perpendicular) de forma determinística."""
        if self.direcao_x != 0:
            self.direcao_x = 0
            self.direcao_y = random.choice([-1, 1])
        else:
            self.direcao_y = 0
            self.direcao_x = random.choice([-1, 1])

    def checar_colisao(self, jogador: Entidade) -> bool:
        """Verifica intersecção entre hitboxes (Detecção de Dano/Fim de jogo)."""
        return self.obter_rect().colliderect(jogador.obter_rect())
