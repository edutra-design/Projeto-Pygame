import pygame 
import sys
import os 

from personagem import Jogador
from inimigo import Inimigo

pygame.init()

largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("core-sync")

cor_fundo = (30, 30, 30)
cor_texto = (255, 255, 255)
cor_botao = (50, 150, 250)
cor_botao_hover = (80, 180, 255)

fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 30)

# O jogo agora pode alternar entre "MENU", "JOGANDO" e "CREDITOS"
estado_jogo = "MENU"

def desenhar_texto(texto, fonte, cor, x, y):
    """função utilitaria para renderizar texto centralizado na tela"""
    imagem_texto = fonte.render(texto, True, cor)
    retangulo_texto = imagem_texto.get_rect(center=(x, y))
    tela.blit(imagem_texto, retangulo_texto)

# Definição física dos botões da tela inicial
botao_jogar = pygame.Rect(largura // 2 - 100, 250, 200, 50)
botao_creditos = pygame.Rect(largura // 2 - 100, 330, 200, 50)  # Novo botão de Créditos
botao_sair = pygame.Rect(largura // 2 - 100, 410, 200, 50)     # Ajustada a altura do botão Sair

jogador = Jogador(100, 100, 40)
inimigo = Inimigo(300, 300, 40)

rodando = True
while rodando:
    posicao_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if estado_jogo == "MENU":
                    if botao_jogar.collidepoint(posicao_mouse):
                        estado_jogo = "JOGANDO"
                    elif botao_creditos.collidepoint(posicao_mouse):
                        estado_jogo = "CREDITOS"  # Muda para a tela de créditos
                    elif botao_sair.collidepoint(posicao_mouse):
                        rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                # Se estiver jogando OU nos créditos, o ESC volta para o Menu
                if estado_jogo == "JOGANDO" or estado_jogo == "CREDITOS":
                    estado_jogo = "MENU"

    tela.fill(cor_fundo)

    jogador.desenhar(tela)
    inimigo.desenhar(tela)

    if estado_jogo == "MENU":
        desenhar_texto("CORE-SYNC", fonte_titulo, cor_texto, largura // 2, 130)
        
        # Lógica de Hover (mudar de cor quando o mouse passa por cima)
        cor_atual_jogar = cor_botao_hover if botao_jogar.collidepoint(posicao_mouse) else cor_botao
        cor_atual_creditos = cor_botao_hover if botao_creditos.collidepoint(posicao_mouse) else cor_botao
        cor_atual_sair = cor_botao_hover if botao_sair.collidepoint(posicao_mouse) else cor_botao

        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, cor_atual_jogar, botao_jogar, border_radius=10)
        pygame.draw.rect(tela, cor_atual_creditos, botao_creditos, border_radius=10)
        pygame.draw.rect(tela, cor_atual_sair, botao_sair, border_radius=10)

        # Desenha os textos internos dos botões
        desenhar_texto("JOGAR", fonte_menu, cor_texto, largura // 2, 275)
        desenhar_texto("CRÉDITOS", fonte_menu, cor_texto, largura // 2, 355)
        desenhar_texto("SAIR", fonte_menu, cor_texto, largura // 2, 435)

    elif estado_jogo == "JOGANDO":
        desenhar_texto("Você está dentro do jogo!", fonte_titulo, (100, 255, 100), largura // 2, altura // 2)
        desenhar_texto("Pressione ESC para voltar ao Menu", fonte_menu, cor_texto, largura // 2, altura // 2 + 80)

    elif estado_jogo == "CREDITOS":
        # Nova tela de créditos exibida ao mudar o estado do jogo
        desenhar_texto("CRÉDITOS", fonte_titulo, cor_texto, largura // 2, 150)
        desenhar_texto("Desenvolvido por: Ana Cândida, Emilly Vitória e Júlia Dutra", fonte_menu, (200, 200, 200), largura // 2, altura // 2 - 20)
        desenhar_texto("Jogo criado em Python com Pygame", fonte_menu, (200, 200, 200), largura // 2, altura // 2 + 30)
        desenhar_texto("Pressione ESC para voltar ao Menu", fonte_menu, cor_texto, largura // 2, altura // 2 + 120)

    pygame.display.flip()

pygame.quit()
sys.exit()
