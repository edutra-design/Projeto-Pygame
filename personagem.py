#personagem.py
import pygame

class Entidade:

    def _init_(self, x, y, tamanho, cor):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.cor = cor


class Jogador(Entidade):

    def _init_(self, x, y, tamanho):
        super()._init_(x, y, tamanho, (0, 255, 255))

    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            self.cor,
            (self.x, self.y, self.tamanho, self.tamanho)
        )
