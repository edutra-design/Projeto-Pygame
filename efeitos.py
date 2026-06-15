#efeitos.py
import pygame
from personagem import Entidade

class Efeito(Entidade):

    def __init__(self, x, y, tamanho):
        super()._init_(x, y, tamanho, (255, 255, 0))

    def desenhar(self, tela):

        pygame.draw.circle(
            tela,
            self.cor,
            (self.x, self.y),
            self.tamanho
        )
