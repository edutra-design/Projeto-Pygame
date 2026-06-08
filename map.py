#map.py
import pygame
from personagem import Entidade

class Parede(Entidade):

    def _init_(self, x, y, tamanho):
        super()._init_(x, y, tamanho, (138, 0, 196))

    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            self.cor,
            (self.x, self.y, self.tamanho, self.tamanho)
        )
