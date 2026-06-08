#main.py
import pygame
import sys
import os

from personagem import Jogador
from inimigos import Inimigo

pygame.init()

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

cor_texto = (255,255,255)
cor_destaque = (0,255,255)

fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
font_opcoes = pygame.font.SysFont("Arial", 40)

estado_atual = "menu"
def desenhar_opcao(texto, fonte, cor, centro_y):
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(LARGURA // 2, centro_y))
    TELA.blit(superficie, retangulo)
    return retangulo 
    
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
