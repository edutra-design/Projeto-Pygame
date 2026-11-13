import pygame
import sys
import math
import json
import os
from personagem import Jogador
from inimigos import Inimigo
from efeitos import EfeitoRastro
from plasma import Plasma
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

COR_VERMELHO_NEON = (255, 40, 60)
COR_VERMELHO_ESCURO = (35, 10, 15)

FONTE_TITULO = pygame.font.SysFont("Impact", 85)
FONTE_MENU = pygame.font.SysFont("Lucida Console", 20, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Consolas", 16, bold=True)


botao_jogar = pygame.Rect(LARGURA // 2 - 150, 270, 300, 50)
botao_creditos = pygame.Rect(LARGURA // 2 - 150, 350, 300, 50)
botao_sair = pygame.Rect(LARGURA // 2 - 150, 430, 300, 50)


botao_tentar_novamente = pygame.Rect(
    LARGURA // 2 - 150, 330, 300, 50
)

botao_voltar_menu = pygame.Rect(
    LARGURA // 2 - 150, 410, 300, 50
)

botao_continuar = pygame.Rect(
    LARGURA // 2 - 150, 420, 300, 50
)


jogador = Jogador(55.0, 55.0, 40)
lista_inimigos = []   # os inimigos de cada fase vêm de map.SPAWNS_INIMIGOS
gerenciador_efeitos = EfeitoRastro()
gerenciador_plasma = Plasma()

FASE_MINIMA_DO_PLASMA = 3

# --- PONTUAÇÃO ---
PONTOS_MOEDA = 10
PONTOS_ESTRELA = 50

# NOTA DA FASE (1 a 3 estrelas): % dos pontos possíveis da fase que o jogador pegou
LIMITE_3_ESTRELAS = 0.90   # 90% ou mais  -> 3 estrelas
LIMITE_2_ESTRELAS = 0.60   # 60% ou mais  -> 2 estrelas (abaixo disso, 1 estrela)

fase_atual = 1
moedas_coletadas = 0     # da fase atual
estrelas_coletadas = 0   # da fase atual
pontos_fase = 0          # pontos da fase atual
pontos_maximos_fase = 0  # máximo que dá para pegar na fase atual
pontos_por_fase = {}     # {numero_da_fase: MELHOR pontuação} das fases já concluídas
melhor_nota = {}         # {numero_da_fase: melhor nota (1 a 3)}; a fase só entra aqui depois de concluída
resumo_fase = {}         # dados da fase que acabou de ser concluída (tela de resumo)


def calcular_nota(pontos, maximo):
    """Devolve 1, 2 ou 3 estrelas conforme a % de pontos pega na fase."""
    if maximo <= 0:
        return 3

    proporcao = pontos / maximo

    if proporcao >= LIMITE_3_ESTRELAS:
        return 3
    if proporcao >= LIMITE_2_ESTRELAS:
        return 2
    return 1


def pontos_total():
    """Soma das fases concluídas + o que já foi pego na fase atual."""
    # a fase atual conta o maior entre o recorde dela e o que está pegando agora
    anteriores = sum(p for f, p in pontos_por_fase.items() if f != fase_atual)
    return anteriores + max(pontos_por_fase.get(fase_atual, 0), pontos_fase)

lista_paredes_do_seu_mapa = map.carregar_fase(fase_atual)

rect_portal = pygame.Rect(0, 0, 0, 0)


# --- MUNDO MAIOR QUE A TELA (os mapas agora são maiores que 800x600) ---
LARGURA_MUNDO, ALTURA_MUNDO = LARGURA, ALTURA
MUNDO = pygame.Surface((LARGURA, ALTURA))        # onde tudo é desenhado
MAPA_PRONTO = pygame.Surface((LARGURA, ALTURA))  # labirinto pré-desenhado (só 1x por fase)
camera_x, camera_y = 0.0, 0.0


def preparar_mundo():
    """Ajusta o tamanho do mundo ao mapa atual e pré-desenha o labirinto."""
    global LARGURA_MUNDO, ALTURA_MUNDO, MUNDO, MAPA_PRONTO

    LARGURA_MUNDO = len(map.MAPA_ATUAL[0]) * map.TAMANHO_BLOCO
    ALTURA_MUNDO = len(map.MAPA_ATUAL) * map.TAMANHO_BLOCO

    MUNDO = pygame.Surface((LARGURA_MUNDO, ALTURA_MUNDO))
    MAPA_PRONTO = pygame.Surface((LARGURA_MUNDO, ALTURA_MUNDO))
    map.desenhar_mapa(MAPA_PRONTO)


def atualizar_camera(instantanea=False):
    """Centraliza a câmera no jogador sem sair dos limites do mapa."""
    global camera_x, camera_y

    alvo_x = jogador.x + jogador.tamanho / 2 - LARGURA / 2
    alvo_y = jogador.y + jogador.tamanho / 2 - ALTURA / 2

    alvo_x = max(0, min(alvo_x, LARGURA_MUNDO - LARGURA))
    alvo_y = max(0, min(alvo_y, ALTURA_MUNDO - ALTURA))

    if instantanea:
        camera_x, camera_y = alvo_x, alvo_y
    else:
        camera_x += (alvo_x - camera_x) * 0.15
        camera_y += (alvo_y - camera_y) * 0.15


estado_jogo = "MENU"
rodando = True
tempo_animacao = 0


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


def desenhar_estrela_nota(cx, cy, raio, cheia):
    """Estrela de 5 pontas: dourada se conquistada, apagada se não."""
    pontos = []

    for i in range(10):
        angulo = -math.pi / 2 + i * math.pi / 5
        r = raio if i % 2 == 0 else raio * 0.45
        pontos.append((cx + math.cos(angulo) * r, cy + math.sin(angulo) * r))

    if cheia:
        pygame.draw.polygon(TELA, (255, 215, 40), pontos)
        pygame.draw.polygon(TELA, (255, 250, 190), pontos, 2)
    else:
        pygame.draw.polygon(TELA, (30, 24, 44), pontos)
        pygame.draw.polygon(TELA, (90, 75, 120), pontos, 2)


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
        f"FASE: {fase_atual} / {len(map.Fases)}",
        FONTE_PEQUENA,
        COR_TEXTO,
        70,
        20
    )

    desenhar_texto(
        f"PONTOS DA FASE: {pontos_fase}",
        FONTE_PEQUENA,
        (255, 215, 40),
        270,
        20
    )

    desenhar_texto(
        f"TOTAL: {pontos_total()}",
        FONTE_PEQUENA,
        (0, 255, 150),
        480,
        20
    )

    desenhar_texto(
        f"MOEDAS: {moedas_coletadas}  ESTRELAS: {estrelas_coletadas}",
        FONTE_PEQUENA,
        (255, 255, 120),
        LARGURA - 130,
        20
    )


def iniciar_fase(numero_da_fase):

    global lista_paredes_do_seu_mapa
    global fase_atual
    global estado_jogo
    global pontos_fase, moedas_coletadas, estrelas_coletadas, pontos_maximos_fase

    retorno_fase = map.carregar_fase(
        numero_da_fase
    )

    if retorno_fase is None:

        estado_jogo = "CREDITOS"
        return

    fase_atual = numero_da_fase

    # a fase começa do zero (o mapa foi recarregado com todos os itens)
    pontos_fase = 0
    moedas_coletadas = 0
    estrelas_coletadas = 0

    # máximo de pontos da fase = todas as moedas e estrelas do mapa recém-carregado
    pontos_maximos_fase = sum(
        PONTOS_MOEDA if tipo == 4 else PONTOS_ESTRELA
        for linha in map.MAPA_ATUAL
        for tipo in linha
        if tipo in (4, 7)
    )

    lista_paredes_do_seu_mapa = retorno_fase

    atualizar_posicao_portal()
    preparar_mundo()


    jogador.x = 55.0
    jogador.y = 55.0

    jogador.direcao_x = 0
    jogador.direcao_y = 0

    if hasattr(jogador, "buffer_x"):

        jogador.buffer_x = 0
        jogador.buffer_y = 0


    lista_inimigos.clear()

    for ex, ey in map.SPAWNS_INIMIGOS.get(fase_atual, []):

        novo_inimigo = Inimigo(float(ex), float(ey), 40)

        ajuste = map.DIFICULDADE_INIMIGOS.get(fase_atual)

        if ajuste:

            novo_inimigo.velocidade_patrulha = ajuste["patrulha"]
            novo_inimigo.velocidade_investida = ajuste["investida"]

        lista_inimigos.append(novo_inimigo)


    if fase_atual >= FASE_MINIMA_DO_PLASMA:

        gerenciador_plasma.definir_velocidade(max(0.60, 0.18 - (fase_atual - FASE_MINIMA_DO_PLASMA) * 0.03))

        gerenciador_plasma.iniciar(map.MAPA_ATUAL, (jogador.x, jogador.y))

    else: 
        gerenciador_plasma.desativar()


    atualizar_camera(True)

    gerenciador_efeitos.rastros.clear()

    if hasattr(
        gerenciador_efeitos,
        "particulas"
    ):

        gerenciador_efeitos.particulas.clear()



# --- TELA DE SELEÇÃO DE FASES (mapa de fases com bloqueio) ---
COR_AMARELO_FASE = (255, 225, 0)
TILE_W, TILE_H = 90, 70
PASSO_X, PASSO_Y = 130, 120
CAIXA_W, CAIXA_FOLGA = 200, 50

FONTE_SELECAO = pygame.font.SysFont("Impact", 46)
FONTE_NUMERO = pygame.font.SysFont("Impact", 38)

ARQUIVO_PROGRESSO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "progresso.json"
)


DURACAO_AVISO = 2000          # ms que a mensagem de fase bloqueada fica na tela
aviso_bloqueio = {"fase": 0, "ate": 0}


def avisar_fase_bloqueada(numero):
    """Chamada quando o jogador clica numa fase bloqueada."""
    aviso_bloqueio["fase"] = numero
    aviso_bloqueio["ate"] = pygame.time.get_ticks() + DURACAO_AVISO


def desenhar_aviso_bloqueio():
    """Faixa 'fase bloqueada' que some suavemente nos últimos 400 ms. Devolve True se está visível."""
    restante = aviso_bloqueio["ate"] - pygame.time.get_ticks()

    if restante <= 0:
        return False

    alfa = 255 if restante > 400 else int(255 * restante / 400)
    numero = aviso_bloqueio["fase"]

    faixa = pygame.Surface((520, 56), pygame.SRCALPHA)
    pygame.draw.rect(faixa, COR_VERMELHO_ESCURO, (0, 0, 520, 56), border_radius=8)
    pygame.draw.rect(faixa, COR_VERMELHO_NEON, (0, 0, 520, 56), width=2, border_radius=8)

    titulo = FONTE_MENU.render(f"FASE {numero} BLOQUEADA", True, COR_VERMELHO_NEON)
    detalhe = FONTE_PEQUENA.render(
        f"Conclua a fase {numero - 1} para desbloquear.", True, COR_TEXTO
    )
    faixa.blit(titulo, titulo.get_rect(center=(260, 18)))
    faixa.blit(detalhe, detalhe.get_rect(center=(260, 41)))

    faixa.set_alpha(alfa)
    TELA.blit(faixa, (LARGURA // 2 - 260, ALTURA - 82))

    return True


def fase_liberada(numero):
    """A fase 1 é sempre liberada; as outras abrem quando a anterior é concluída."""
    return numero == 1 or (numero - 1) in melhor_nota


def salvar_progresso():
    try:
        with open(ARQUIVO_PROGRESSO, "w", encoding="utf-8") as arquivo:
            json.dump({"pontos": pontos_por_fase, "notas": melhor_nota}, arquivo)
    except OSError:
        pass


def carregar_progresso():
    try:
        with open(ARQUIVO_PROGRESSO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        for chave, valor in dados.get("pontos", {}).items():
            if int(chave) in map.Fases:
                pontos_por_fase[int(chave)] = int(valor)

        for chave, valor in dados.get("notas", {}).items():
            if int(chave) in map.Fases:
                melhor_nota[int(chave)] = max(1, min(3, int(valor)))
    except (OSError, ValueError, TypeError, AttributeError):
        pass


def calcular_layout_selecao():
    """Posiciona as fases em colunas de 3, subindo e descendo (como no mapa de fases)."""
    total = len(map.Fases)
    colunas = (total + 2) // 3
    largura_total = (colunas - 1) * PASSO_X + TILE_W + CAIXA_FOLGA + CAIXA_W
    x_esq = (LARGURA - largura_total) // 2
    y_topo = 190

    rects = {}
    for numero in range(1, total + 1):
        indice = numero - 1
        coluna = indice // 3
        linha = indice % 3

        if coluna % 2 == 1:
            linha = 2 - linha

        cx = x_esq + TILE_W // 2 + coluna * PASSO_X
        cy = y_topo + linha * PASSO_Y
        rects[numero] = pygame.Rect(cx - TILE_W // 2, cy - TILE_H // 2, TILE_W, TILE_H)

    caixa_x = x_esq + (colunas - 1) * PASSO_X + TILE_W + CAIXA_FOLGA
    caixa = pygame.Rect(caixa_x, 150, CAIXA_W, 330)

    return rects, caixa


RECTS_FASES, CAIXA_FINAL = calcular_layout_selecao()
carregar_progresso()


def desenhar_cadeado(cx, cy, cor):
    pygame.draw.arc(TELA, cor, (cx - 9, cy - 24, 18, 20), 0, math.pi, 3)
    pygame.draw.line(TELA, cor, (cx - 9, cy - 14), (cx - 9, cy - 8), 3)
    pygame.draw.line(TELA, cor, (cx + 8, cy - 14), (cx + 8, cy - 8), 3)
    pygame.draw.rect(TELA, cor, (cx - 13, cy - 8, 26, 20), border_radius=3)
    pygame.draw.circle(TELA, (36, 30, 54), (cx, cy + 2), 3)


def desenhar_tile_fase(numero, ret, liberada, sobre, erro=False):
    cor = COR_AMARELO_FASE if liberada else (36, 30, 54)

    # "orelhas" no topo do quadradinho
    pygame.draw.rect(TELA, cor, (ret.left + 8, ret.top - 6, 16, 8))
    pygame.draw.rect(TELA, cor, (ret.right - 24, ret.top - 6, 16, 8))
    pygame.draw.rect(TELA, cor, ret, border_radius=4)

    if liberada:
        if sobre:
            pygame.draw.rect(TELA, (255, 255, 255), ret, width=3, border_radius=4)

        imagem = FONTE_NUMERO.render(str(numero), True, (20, 16, 30))
        TELA.blit(imagem, imagem.get_rect(center=ret.center))

        nota = melhor_nota.get(numero, 0)
        for i in range(3):
            desenhar_estrela_nota(ret.centerx + (i - 1) * 28, ret.bottom + 18, 10, i < nota)
    else:
        if erro:
            pygame.draw.rect(TELA, COR_VERMELHO_NEON, ret, width=3, border_radius=4)
            desenhar_cadeado(ret.centerx, ret.centery + 6, COR_VERMELHO_NEON)
        else:
            pygame.draw.rect(TELA, (70, 60, 100), ret, width=2, border_radius=4)
            desenhar_cadeado(ret.centerx, ret.centery + 6, (120, 105, 150))


def desenhar_ligacao(a, b, ativa):
    cor = COR_AMARELO_FASE if ativa else (60, 52, 84)

    if a.centerx == b.centerx:
        if b.top > a.top:    # descendo (passa por baixo das estrelas)
            p1, p2 = (a.centerx, a.bottom + 32), (b.centerx, b.top)
        else:                # subindo
            p1, p2 = (a.centerx, a.top), (b.centerx, b.bottom + 32)
    else:                    # coluna seguinte, à direita
        p1, p2 = (a.right, a.centery), (b.left, b.centery)

    pygame.draw.line(TELA, cor, p1, p2, 3)


def desenhar_caixa_pontilhada(ret, cor):
    for x in range(ret.left, ret.right, 8):
        pygame.draw.rect(TELA, cor, (x, ret.top, 3, 3))
        pygame.draw.rect(TELA, cor, (x, ret.bottom - 3, 3, 3))

    for y in range(ret.top, ret.bottom, 8):
        pygame.draw.rect(TELA, cor, (ret.left, y, 3, 3))
        pygame.draw.rect(TELA, cor, (ret.right - 3, y, 3, 3))


def desenhar_selecao_fase(posicao_mouse):
    desenhar_linhas_tecnologicas()

    desenhar_texto("SELECIONE A FASE", FONTE_SELECAO, COR_AMARELO_FASE, LARGURA // 2, 70)

    desenhar_texto(
        f"PONTUAÇÃO TOTAL: {sum(pontos_por_fase.values())}",
        FONTE_PEQUENA,
        COR_TEXTO,
        LARGURA // 2,
        115
    )

    total = len(map.Fases)

    # ligações primeiro, para os quadradinhos ficarem por cima
    for numero in range(1, total):
        desenhar_ligacao(RECTS_FASES[numero], RECTS_FASES[numero + 1], fase_liberada(numero + 1))

    ultimo = RECTS_FASES[total]
    pygame.draw.line(
        TELA,
        COR_AMARELO_FASE if total in melhor_nota else (60, 52, 84),
        (ultimo.right, ultimo.centery),
        (CAIXA_FINAL.left, ultimo.centery),
        3
    )

    restante = aviso_bloqueio["ate"] - pygame.time.get_ticks()

    for numero, ret in RECTS_FASES.items():
        liberada = fase_liberada(numero)
        erro = restante > 0 and aviso_bloqueio["fase"] == numero
        ret_desenho = ret

        if erro:
            passou = DURACAO_AVISO - restante
            if passou < 400:    # treme só no começo
                deslocamento = int(math.sin(passou * 0.06) * 7 * (1 - passou / 400))
                ret_desenho = ret.move(deslocamento, 0)

        desenhar_tile_fase(
            numero,
            ret_desenho,
            liberada,
            liberada and ret.collidepoint(posicao_mouse),
            erro
        )

    desenhar_caixa_pontilhada(CAIXA_FINAL, COR_ROXO_NEON)
    desenhar_texto("NOVAS AVENTURAS", FONTE_PEQUENA, COR_ROXO_NEON, CAIXA_FINAL.centerx, CAIXA_FINAL.centery - 35)
    desenhar_texto("ESTÃO", FONTE_MENU, COR_ROXO_NEON, CAIXA_FINAL.centerx, CAIXA_FINAL.centery + 5)
    desenhar_texto("CHEGANDO", FONTE_MENU, COR_ROXO_NEON, CAIXA_FINAL.centerx, CAIXA_FINAL.centery + 35)

    if not desenhar_aviso_bloqueio():
        desenhar_texto(
            "CLIQUE EM UMA FASE LIBERADA   |   ESC: MENU",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            ALTURA - 40
        )


def concluir_fase():
    """Guarda os pontos da fase e abre a tela de resumo."""
    global estado_jogo, resumo_fase

    nota = calcular_nota(pontos_fase, pontos_maximos_fase)

    # guarda o recorde da fase; concluir libera a próxima
    pontos_por_fase[fase_atual] = max(pontos_por_fase.get(fase_atual, 0), pontos_fase)
    melhor_nota[fase_atual] = max(melhor_nota.get(fase_atual, 0), nota)
    salvar_progresso()

    resumo_fase = {
        "fase": fase_atual,
        "pontos": pontos_fase,
        "maximo": pontos_maximos_fase,
        "nota": nota,
        "moedas": moedas_coletadas,
        "estrelas": estrelas_coletadas,
        "total": pontos_total(),
        "todas": all(f in melhor_nota for f in map.Fases),
    }

    estado_jogo = "FASE_CONCLUIDA"


def avancar_apos_resumo():
    """Sai da tela de resumo e vai para a escolha de fase."""
    global estado_jogo

    estado_jogo = "SELECAO_FASE"


atualizar_posicao_portal()
preparar_mundo()


while rodando:

    def coletar_itens():
        global moedas_coletadas, estrelas_coletadas, pontos_fase

        rect_jogador = jogador.obter_rect()
        coletou = False

        for linha in range(len(map.MAPA_ATUAL)):
            for coluna in range(len(map.MAPA_ATUAL[linha])):
                tipo = map.MAPA_ATUAL[linha][coluna]

                if tipo == 4 or tipo == 7:
                    rect_item = pygame.Rect(
                        coluna * map.TAMANHO_BLOCO,
                        linha * map.TAMANHO_BLOCO,
                        map.TAMANHO_BLOCO,
                        map.TAMANHO_BLOCO
                    )

                    if rect_jogador.colliderect(rect_item):
                        if tipo == 4:
                            moedas_coletadas += 1
                            pontos_fase += PONTOS_MOEDA
                        elif tipo == 7:
                            estrelas_coletadas += 1
                            pontos_fase += PONTOS_ESTRELA
                        map.MAPA_ATUAL[linha][coluna] = 0
                        coletou = True
        if coletou:
            map.desenhar_mapa(MAPA_PRONTO)

    RELOGIO.tick(60)

    tempo_animacao += 0.05

    posicao_mouse = pygame.mouse.get_pos()
    

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        elif (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):


            if estado_jogo == "MENU":

                if botao_jogar.collidepoint(
                    posicao_mouse
                ):

                    estado_jogo = "SELECAO_FASE"

                elif botao_creditos.collidepoint(
                    posicao_mouse
                ):

                    estado_jogo = "CREDITOS"

                elif botao_sair.collidepoint(
                    posicao_mouse
                ):

                    rodando = False


            elif estado_jogo == "SELECAO_FASE":

                for numero, ret in RECTS_FASES.items():

                    if ret.collidepoint(posicao_mouse):

                        if fase_liberada(numero):

                            iniciar_fase(numero)

                            estado_jogo = "JOGANDO"

                        else:

                            avisar_fase_bloqueada(numero)

                        break

            elif estado_jogo == "FASE_CONCLUIDA":

                if botao_continuar.collidepoint(
                    posicao_mouse
                ):

                    avancar_apos_resumo()

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

            if (
                estado_jogo == "FASE_CONCLUIDA"
                and evento.key in (pygame.K_RETURN, pygame.K_SPACE)
            ):

                avancar_apos_resumo()

            elif evento.key == pygame.K_ESCAPE:

                if estado_jogo in (
                    "JOGANDO",
                    "CREDITOS",
                    "GAME_OVER",
                    "FASE_CONCLUIDA",
                    "SELECAO_FASE"
                ):

                    estado_jogo = "MENU"


    TELA.fill(COR_FUNDO)


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

   

    elif estado_jogo == "JOGANDO":

        jogador.mover(
            LARGURA_MUNDO,
            ALTURA_MUNDO,
            lista_paredes_do_seu_mapa,
            gerenciador_efeitos,
        )
        coletar_itens()

        for inimigo in lista_inimigos:

            inimigo.atualizar_ia(
                LARGURA_MUNDO,
                ALTURA_MUNDO,
                lista_paredes_do_seu_mapa,
                jogador
            )

            if inimigo.checar_colisao(
                jogador
            ):

                estado_jogo = "GAME_OVER"

       

        rect_jogador = jogador.obter_rect()

        if rect_jogador.colliderect(
            rect_portal
        ):

            concluir_fase()

        
        MUNDO.blit(MAPA_PRONTO, (0, 0))


        try:

            gerenciador_efeitos.atualizar_e_desenhar(
                MUNDO
            )

        except TypeError:

            gerenciador_efeitos.atualizar_e_desenhar(
                MUNDO,
                1 / 60
            )


        for inimigo in lista_inimigos:

            inimigo.desenhar(MUNDO)


        atualizar_camera()

        cam_x, cam_y = int(camera_x), int(camera_y)

        TELA.blit(
            MUNDO,
            (0, 0),
            (cam_x, cam_y, LARGURA, ALTURA)
        )


        centro_jogador = jogador.obter_rect().center

        map.aplicar_iluminacao_pro(
            TELA,
            (centro_jogador[0] - cam_x, centro_jogador[1] - cam_y)
        )

        # desenha o jogador na posição da tela (posição no mundo - câmera)
        pos_mundo = (jogador.x, jogador.y)
        jogador.x -= cam_x
        jogador.y -= cam_y
        jogador.desenhar(TELA)
        jogador.x, jogador.y = pos_mundo

        desenhar_hud_jogo()

        desenhar_texto(
            "Pressione ESC para ejetar",
            FONTE_PEQUENA,
            COR_TEXTO,
            LARGURA // 2,
            ALTURA - 25
        )

 

    elif estado_jogo == "SELECAO_FASE":

        desenhar_selecao_fase(posicao_mouse)

    elif estado_jogo == "FASE_CONCLUIDA":

        desenhar_linhas_tecnologicas()

        moldura_resumo = pygame.Rect(
            LARGURA // 2 - 280,
            100,
            560,
            400
        )

        pygame.draw.rect(
            TELA,
            COR_ROXO_ESCURO,
            moldura_resumo,
            border_radius=8
        )

        pygame.draw.rect(
            TELA,
            COR_ROXO_NEON,
            moldura_resumo,
            width=2,
            border_radius=8
        )

        if resumo_fase["todas"]:
            titulo_resumo = "TODAS AS FASES CONCLUÍDAS"
        else:
            titulo_resumo = f"FASE {resumo_fase['fase']} CONCLUÍDA"

        desenhar_texto(
            titulo_resumo,
            FONTE_MENU,
            COR_ROXO_NEON,
            LARGURA // 2,
            150
        )

        pygame.draw.line(
            TELA,
            COR_ROXO_HOVER,
            (LARGURA // 2 - 200, 185),
            (LARGURA // 2 + 200, 185),
            1
        )

        for i in range(3):
            desenhar_estrela_nota(
                LARGURA // 2 + (i - 1) * 70,
                232,
                26,
                i < resumo_fase["nota"]
            )

        desenhar_texto(
            f"MOEDAS: {resumo_fase['moedas']}  (+{resumo_fase['moedas'] * PONTOS_MOEDA})",
            FONTE_PEQUENA,
            (255, 215, 40),
            LARGURA // 2,
            285
        )

        desenhar_texto(
            f"ESTRELAS: {resumo_fase['estrelas']}  (+{resumo_fase['estrelas'] * PONTOS_ESTRELA})",
            FONTE_PEQUENA,
            (255, 255, 120),
            LARGURA // 2,
            310
        )

        desenhar_texto(
            f"PONTOS DA FASE: {resumo_fase['pontos']} / {resumo_fase['maximo']}",
            FONTE_MENU,
            COR_TEXTO,
            LARGURA // 2,
            350
        )

        desenhar_texto(
            f"PONTUAÇÃO TOTAL: {resumo_fase['total']}",
            FONTE_MENU,
            (0, 255, 150),
            LARGURA // 2,
            388
        )

        desenhar_botao_profissional(
            botao_continuar,
            "[ ESCOLHER FASE ]",
            posicao_mouse
        )

 

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
        ) 

        desenhar_texto(
            "Pressione ESC para retornar ao painel",
            FONTE_PEQUENA,
            (alfa, alfa, 255),
            LARGURA // 2,
            440
        )

   

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
            COR_VERMELHO_ESCURO,
            moldura_game_over,
            border_radius=10
        )

        pygame.draw.rect(
            TELA,
            COR_VERMELHO_NEON,
            moldura_game_over,
            width=2,
            border_radius=10
        )

        desenhar_texto(
            "GAME OVER",
            FONTE_TITULO,
            (80, 10, 20),
            LARGURA // 2 + 5,
            150
        )

        desenhar_texto(
            "GAME OVER",
            FONTE_TITULO,
            (255, 30, 50),
            LARGURA // 2,
            145
        )

        pygame.draw.line(
            TELA,
            COR_VERMELHO_NEON,
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
            235
        )

        desenhar_texto(
            "O NÚCLEO FOI COMPROMETIDO",
            FONTE_PEQUENA,
            (255, 120, 120),
            LARGURA // 2,
            258
        )

        desenhar_texto(
            f"FASE {fase_atual}",
            FONTE_MENU,
            COR_VERMELHO_NEON,
            LARGURA // 2,
            285
        )

        desenhar_texto(
            f"PONTOS DA FASE: {pontos_fase}   TOTAL: {pontos_total()}",
            FONTE_PEQUENA,
            (255, 215, 40),
            LARGURA // 2,
            312
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

 

    pygame.display.flip()




pygame.quit()
sys.exit()


pygame.quit()
sys.exit()
