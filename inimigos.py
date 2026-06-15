#inimigos.py
import pygame
from personagem import Entidade

class Inimigo(Entidade):

    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho, (255, 0, 0))

    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            self.cor,
            (self.x, self.y, self.tamanho, self.tamanho)
        )
