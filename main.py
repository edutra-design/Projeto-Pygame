#main.py
import pygame
import sys

from personagem import Jogador
from inimigos import Inimigo

pygame.init()

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

jogador = Jogador(100, 100, 40)
inimigo = Inimigo(300, 300, 40)

rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    TELA.fill((10, 10, 25))

    jogador.desenhar(TELA)
    inimigo.desenhar(TELA)

    pygame.display.flip()

pygame.quit()
sys.exit()
