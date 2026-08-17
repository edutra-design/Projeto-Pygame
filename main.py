import pygame

import pygame
import sys
import math
from personagem import Jogador
from inimigos import Inimigo
from efeitos import EfeitoRastro
import map

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("core-sync: mask edition")
RELOGIO = pygame.time.Clock()

map.inicializar_iluminacao(LARGURA, ALTURA)

COR_FUNDO = (10, 10, 18)
COR_TEXTO = (240, 240, 255)
COR_ROXO_NEON = (180, 50, 255)
COR_ROXO_ESCURO = (32, 24, 48)
COR_ROXO_HOVER = (120, 40, 220)
COR_MOLDURA_ARCADE = (45, 30, 70)

FONTE_TITULO = pygame.font.SysFont("Impact", 85)
FONTE_MENU = pygame.font.SysFont("Lucida Console", 20, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Consolas", 16, bold=True)

# --------------------------------------------------
# BOTÕES DO MENU
# --------------------------------------------------

botao_jogar = pygame.Rect(LARGURA // 2 - 150, 270, 300, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 150, 350, 300, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 150, 430, 300, 50)

# --------------------------------------------------
# BOTÕES DO GAME OVER
# --------------------------------------------------

botao_tentar_novamente = pygame.Rect(
    LARGURA // 2 - 150, 330, 300, 50
)

botao_voltar_menu = pygame.Rect(
    LARGURA // 2 - 150, 410, 300, 50
)

# --------------------------------------------------
# OBJETOS DO JOGO
# --------------------------------------------------

jogador = Jogador(55.0, 55.0, 40)
inimigos = Inimigo(505.0, 455.0, 40)
gerenciador_efeitos = EfeitoRastro()

fase_atual = 1

lista_paredes_do_seu_mapa = map.carregar_fase(fase_atual)

rect_portal = pygame.Rect(0, 0, 0, 0)

# --------------------------------------------------
# ESTADOS DO JOGO
# --------------------------------------------------

estado_jogo = "MENU"
rodando = True
tempo_animacao = 0


# ==================================================
# PORTAL
# ==================================================

def atualizar_posicao_portal():

    global rect_portal

    for linha_idx, linha in enumerate(map.MAPA_ATUAL):

        for col_idx, tipo in enumerate(linha):

            if tipo == 6:

                x = col_idx * map.TAMANHO_BLOCO
                y = linha_idx * map.TAMANHO_BLOCO

                rect_portal = pygame.Rect(
                    x,
                    y,
                    map.TAMANHO_BLOCO,
                    map.TAMANHO_BLOCO
                )

                return

    rect_portal = pygame.Rect(-100, -100, 0, 0)


# ==================================================
# FUNDO DO MENU
# ==================================================

def desenhar_linhas_tecnologicas():

    for x in range(0, LARGURA, 40):

        pygame.draw.line(
            TELA,
            (18, 15, 28),
            (x, 0),
            (x, ALTURA),
            1
        )

    for y in range(0, ALTURA, 40):

        pygame.draw.line(
            TELA,
            (18, 15, 28),
            (0, y),
            (LARGURA, y),
            1
        )

    pygame.draw.rect(
        TELA,
        COR_ROXO_NEON,
        (20, 20, 30, 4),
        border_radius=2
    )

    pygame.draw.rect(
        TELA,
        COR_ROXO_NEON,
        (20, 20, 4, 30),
        border_radius=2
    )

    pygame.draw.rect(
        TELA,
        COR_ROXO_NEON,
        (LARGURA - 50, 20, 30, 4),
        border_radius=2
    )

    pygame.draw.rect(
        TELA,
        COR_ROXO_NEON,
        (LARGURA - 24, 20, 4, 30),
        border_radius=2
    )


# ==================================================
# TEXTO
# ==================================================

def desenhar_texto(
    texto: str,
    fonte: pygame.font.Font,
    cor: tuple,
    x: int,
    y: int
):

    imagem_texto = fonte.render(
        texto,
        True,
        cor
    )

    TELA.blit(
        imagem_texto,
        imagem_texto.get_rect(
            center=(x, y)
        )
    )


# ==================================================
# BOTÕES
# ==================================================

def desenhar_botao_profissional(
    retangulo: pygame.Rect,
    texto: str,
    posicao_mouse: tuple
):

    colidindo = retangulo.collidepoint(
        posicao_mouse
    )

    cor_fundo = (
        COR_ROXO_ESCURO
        if not colidindo
        else (45, 32, 68)
    )

    cor_borda = (
        COR_ROXO_HOVER
        if not colidindo
        else COR_ROXO_NEON
    )

    pygame.draw.rect(
        TELA,
        cor_fundo,
        retangulo,
        border_radius=6
    )

    pygame.draw.rect(
        TELA,
        cor_borda,
        retangulo,
        width=2,
        border_radius=6
    )

    if colidindo:

        pygame.draw.rect(
            TELA,
            COR_ROXO_NEON,
            (
                retangulo.x - 15,
                retangulo.y + 15,
                4,
                20
            )
        )

        pygame.draw.rect(
            TELA,
            COR_ROXO_NEON,
            (
                retangulo.right + 11,
                retangulo.y + 15,
                4,
                20
            )
        )

    desenhar_texto(
        texto,
        FONTE_MENU,
        COR_TEXTO,
        retangulo.centerx,
        retangulo.centery
    )


# ==================================================
# HUD
# ==================================================

def desenhar_hud_jogo():

    pygame.draw.rect(
        TELA,
        (15, 12, 24),
        (0, 0, LARGURA, 40)
    )

    pygame.draw.line(
        TELA,
        COR_ROXO_NEON,
        (0, 40),
        (LARGURA, 40),
        2
    )

    desenhar_texto(
        f"FASE: {fase_atual} / 3",
        FONTE_PEQUENA,
        COR_TEXTO,
        60,
        20
    )

    desenhar_texto(
        "MÉTODO: GEOMÉTRICO",
        FONTE_PEQUENA,
        COR_ROXO_HOVER,
        LARGURA // 2,
        20
    )

    desenhar_texto(
        "STATUS: ATIVO",
        FONTE_PEQUENA,
        (0, 255, 150),
        LARGURA - 100,
        20
    )


# ==================================================
# INICIAR FASE
# ==================================================

def iniciar_fase(numero_da_fase):

    global lista_paredes_do_seu_mapa
    global fase_atual
    global estado_jogo

    retorno_fase = map.carregar_fase(
        numero_da_fase
    )

    if retorno_fase is None:

        estado_jogo = "CREDITOS"
        return

    fase_atual = numero_da_fase

    lista_paredes_do_seu_mapa = retorno_fase

    atualizar_posicao_portal()

    # RESET DO JOGADOR

    jogador.x = 55.0
    jogador.y = 55.0

    jogador.direcao_x = 0
    jogador.direcao_y = 0

    if hasattr(jogador, "buffer_x"):

        jogador.buffer_x = 0
        jogador.buffer_y = 0

    # POSIÇÃO DO INIMIGO

    if fase_atual == 1:

        inimigos.x = 505.0
        inimigos.y = 455.0

    elif fase_atual == 2:

        inimigos.x = 350.0
        inimigos.y = 350.0

    elif fase_atual == 3:

        inimigos.x = 700.0
        inimigos.y = 500.0

    inimigos.estado = "PATRULHA"

    # LIMPA EFEITOS

    gerenciador_efeitos.rastros.clear()

    if hasattr(
        gerenciador_efeitos,
        "particulas"
    ):

        gerenciador_efeitos.particulas.clear()


# ==================================================
# INICIALIZA PORTAL
# ==================================================

atualizar_posicao_portal()


# ==================================================
# LOOP PRINCIPAL
# ==================================================

while rodando:

    RELOGIO.tick(60)

    tempo_animacao += 0.05

    posicao_mouse = pygame.mouse.get_pos()

    # ==================================================
    # EVENTOS
    # ==================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        elif (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):

            # MENU

            if estado_jogo == "MENU":

                if botao_jogar.collidepoint(
                    posicao_mouse
                ):

                    iniciar_fase(1)

                    estado_jogo = "JOGANDO"

                elif botao_creditos.collidepoint(
                    posicao_mouse
                ):

                    estado_jogo = "CREDITOS"

                elif botao_sair.collidepoint(
                    posicao_mouse
                ):

                    rodando = False

            # GAME OVER

            elif estado_jogo == "GAME_OVER":

                if botao_tentar_novamente.collidepoint(
                    posicao_mouse
                ):

                    iniciar_fase(
                        fase_atual
                    )

                    estado_jogo = "JOGANDO"

                elif botao_voltar_menu.collidepoint(
                    posicao_mouse
                ):

                    estado_jogo = "MENU"

        elif evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                if estado_jogo in (
                    "JOGANDO",
                    "CREDITOS",
                    "GAME_OVER"
                ):

                    estado_jogo = "MENU"

    # ==================================================
    # LIMPA TELA
    # ==================================================

    TELA.fill(COR_FUNDO)

    # ==================================================
    # MENU
    # ==================================================

    if estado_jogo == "MENU":

        desenhar_linhas_tecnologicas()

        oscilacao = int(
            (
                math.sin(
                    tempo_animacao * 1.5
                ) + 1
            ) * 20
        )

        cor_titulo = (
            140 + oscilacao,
            50,
            255
        )

        desenhar_texto(
            "CORE_SYNC",
            FONTE_TITULO,
            (40, 20, 80),
            LARGURA // 2 + 5,
            135
        )

        desenhar_texto(
            "CORE_SYNC",
            FONTE_TITULO,
            cor_titulo,
            LARGURA // 2,
            130
        )

        pygame.draw.line(
            TELA,
            COR_ROXO_NEON,
            (
                LARGURA // 2 - 180,
                195
            ),
            (
                LARGURA // 2 + 180,
                195
            ),
            2
        )

        desenhar_texto(
            "::: M A S K   E D I T I O N :::",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            215
        )

        desenhar_botao_profissional(
            botao_jogar,
            "[ ACESSAR CORE ]",
            posicao_mouse
        )

        desenhar_botao_profissional(
            botao_creditos,
            "[ CONFIG / CRÉDITOS ]",
            posicao_mouse
        )

        desenhar_botao_profissional(
            botao_sair,
            "[ DESCONECTAR ]",
            posicao_mouse
        )

    # ==================================================
    # JOGANDO
    # ==================================================

    elif estado_jogo == "JOGANDO":

        # MOVIMENTO DO JOGADOR

        jogador.mover(
            LARGURA,
            ALTURA,
            lista_paredes_do_seu_mapa,
            gerenciador_efeitos
        )

        # IA DO INIMIGO

        inimigos.atualizar_ia(
            LARGURA,
            ALTURA,
            lista_paredes_do_seu_mapa,
            jogador
        )

        # GAME OVER

        if inimigos.checar_colisao(
            jogador
        ):

            estado_jogo = "GAME_OVER"

        # PORTAL

        rect_jogador = jogador.obter_rect()

        if rect_jogador.colliderect(
            rect_portal
        ):

            if fase_atual < 3:

                iniciar_fase(
                    fase_atual + 1
                )

            else:

                estado_jogo = "CREDITOS"

        # ==================================================
        # MAPA
        # ==================================================

        map.desenhar_mapa(TELA)

        # ==================================================
        # EFEITOS
        # ==================================================

        try:

            gerenciador_efeitos.atualizar_e_desenhar(
                TELA
            )

        except TypeError:

            gerenciador_efeitos.atualizar_e_desenhar(
                TELA,
                1 / 60
            )

        # ==================================================
        # INIMIGO
        # ==================================================

        inimigos.desenhar(TELA)

        # ==================================================
        # ILUMINAÇÃO
        # ==================================================

        map.aplicar_iluminacao_pro(
            TELA,
            jogador.obter_rect().center
        )

        # ==================================================
        # JOGADOR
        # DESENHADO DEPOIS DA ILUMINAÇÃO
        # PARA FICAR CLARO
        # ==================================================

        jogador.desenhar(TELA)

        # ==================================================
        # HUD
        # ==================================================

        desenhar_hud_jogo()

        desenhar_texto(
            "Pressione ESC para ejetar",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            ALTURA - 25
        )

    # ==================================================
    # CREDITOS
    # ==================================================

    elif estado_jogo == "CREDITOS":

        desenhar_linhas_tecnologicas()

        moldura_creditos = pygame.Rect(
            LARGURA // 2 - 280,
            120,
            560,
            360
        )

        pygame.draw.rect(
            TELA,
            COR_ROXO_ESCURO,
            moldura_creditos,
            border_radius=8
        )

        pygame.draw.rect(
            TELA,
            COR_ROXO_NEON,
            moldura_creditos,
            width=2,
            border_radius=8
        )

        desenhar_texto(
            "CRÉDITOS",
            FONTE_MENU,
            COR_ROXO_NEON,
            LARGURA // 2,
            170
        )

        pygame.draw.line(
            TELA,
            COR_ROXO_HOVER,
            (
                LARGURA // 2 - 200,
                210
            ),
            (
                LARGURA // 2 + 200,
                210
            ),
            1
        )

        desenhar_texto(
            "EQUIPE CORE:",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            250
        )

        desenhar_texto(
            "Ana Cândida",
            FONTE_MENU,
            COR_TEXTO,
            LARGURA // 2,
            290
        )

        desenhar_texto(
            "Emilly Vitória",
            FONTE_MENU,
            COR_TEXTO,
            LARGURA // 2,
            330
        )

        desenhar_texto(
            "Júlia Dutra",
            FONTE_MENU,
            COR_TEXTO,
            LARGURA // 2,
            370
        )

        alfa = int(
            (
                math.cos(
                    tempo_animacao * 2
                ) + 1
            ) * 75
        ) + 105

        desenhar_texto(
            "Pressione ESC para retornar ao painel",
            FONTE_PEQUENA,
            (alfa, alfa, 255),
            LARGURA // 2,
            440
        )

    # ==================================================
    # GAME OVER
    # ==================================================

    elif estado_jogo == "GAME_OVER":

        desenhar_linhas_tecnologicas()

        moldura_game_over = pygame.Rect(
            LARGURA // 2 - 300,
            80,
            600,
            450
        )

        pygame.draw.rect(
            TELA,
            (25, 12, 30),
            moldura_game_over,
            border_radius=10
        )

        pygame.draw.rect(
            TELA,
            (255, 40, 80),
            moldura_game_over,
            width=2,
            border_radius=10
        )

        desenhar_texto(
            "GAME OVER",
            FONTE_TITULO,
            (70, 10, 30),
            LARGURA // 2 + 5,
            150
        )

        desenhar_texto(
            "GAME OVER",
            FONTE_TITULO,
            (255, 30, 70),
            LARGURA // 2,
            145
        )

        pygame.draw.line(
            TELA,
            (255, 40, 80),
            (
                LARGURA // 2 - 180,
                215
            ),
            (
                LARGURA // 2 + 180,
                215
            ),
            2
        )

        desenhar_texto(
            "::: CONEXÃO PERDIDA :::",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            245
        )

        desenhar_texto(
            "O NÚCLEO FOI COMPROMETIDO",
            FONTE_PEQUENA,
            (255, 100, 120),
            LARGURA // 2,
            275
        )

        desenhar_texto(
            f"FASE {fase_atual}",
            FONTE_MENU,
            COR_ROXO_NEON,
            LARGURA // 2,
            305
        )

        desenhar_botao_profissional(
            botao_tentar_novamente,
            "[ TENTAR NOVAMENTE ]",
            posicao_mouse
        )

        desenhar_botao_profissional(
            botao_voltar_menu,
            "[ VOLTAR AO MENU ]",
            posicao_mouse
        )

        desenhar_texto(
            "ESC — VOLTAR AO MENU",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            500
        )

    # ==================================================
    # ATUALIZA TELA
    # ==================================================

    pygame.display.flip()


# ==================================================
# FINALIZAÇÃO
# ==================================================

pygame.quit()
sys.exit()
