import math
import pygame

TAMANHO_BLOCO = 50

_FASES_ASCII = {
    1: [
        "#####################",
        "#S..###########....*#",
        "#.#.###########.###.#",
        "#.#.............###.#",
        "#.#########.###.###.#",
        "#.#########.###.###.#",
        "#.#########.###.###.#",
        "#.#####.....###.###.#",
        "#.#####.#.#####.###.#",
        "#.#####P#...........#",
        "#.#################.#",
        "#.#####.........###.#",
        "#.#####.#######.###.#",
        "#*......#######*....#",
        "#####################",
    ],
    2: [
        "#########################",
        "#S....#.............#####",
        "#.#.#.#.###.###.###.#####",
        "#.#.#.......###.###.#####",
        "#.#.#.#####.###.###.#####",
        "#...............###.#####",
        "#.#.#####.#####.###.#####",
        "#.#....*#.#####.###.....#",
        "#.#.###.#.#####.###.###.#",
        "#.#.###.#.#####.###.###.#",
        "#.#.###.#.#####.###.###.#",
        "#.........#*........#..P#",
        "###.###.#.###.#.###.#.#.#",
        "#...###...........#...#.#",
        "#.#####.#.#.#.#.#.#####.#",
        "#+.....*....#...........#",
        "#########################",
    ],
    3: [
        "###############################",
        "#S..............#.......#*#...#",
        "#.#############.#.#.#.#.#.#.#.#",
        "#.....#########.#.#.#.#.#.#.#.#",
        "#.###.#########.#.#.#.#.#.#.#.#",
        "#.###.............#...........#",
        "#.###.#######.#.#.#.#.###.###.#",
        "#...............#.#.........#.#",
        "#.###.#.#####.#.#.#.#.###.#.#.#",
        "#.........#+..#.#.#.........#.#",
        "#.###.#.#.#.#.#.#.###.###.#.#.#",
        "#.###.#.#.#.#.#.#.#...#...#...#",
        "#.###.#.#.#.#.#.#.#.#.#.#.#####",
        "#.....#.#...........#...#.#P..#",
        "#####.#.###.#.###.#####.#.#.#.#",
        "#.....#.......#.......#.#.....#",
        "#.###.#.#.#.#.#.#####.#.###.#.#",
        "#.#.........#...#####...#.....#",
        "#.#.###.#.#.#########.###.#.#.#",
        "#.......#...#*.......*....#...#",
        "###############################",
    ],
    4: [
        "#####################################",
        "#S......#...#####.................#*#",
        "#######.#.#.#####.###.#######.#.#.#.#",
        "#.....#...............#....##.#.#.#.#",
        "#.#.#.###.#######.###.#.##....#.#.#.#",
        "#.#.......#.....#.###.#.....#.......#",
        "#.###.#.###.#.#.#.###.#.#..##.#.###.#",
        "#...........#.....#.............###.#",
        "#####.#.#.#.#.#####.###.#.###.#####.#",
        "#.......#.................###.#####.#",
        "#.#####.#.###.###.#######.###.#####.#",
        "#.#*#.........###.###*###.#...#...#.#",
        "#.#.#.#.#####.###.###.###.#.#.#.#.#.#",
        "#.#...............###.###.#.#.#.#...#",
        "#.#.#.#######.###.###.###.#.#.#.#####",
        "#.#.#.#######.###.###...#.#...#.....#",
        "#.#.#.#######.###.###.#.#.#####.###.#",
        "#.....................#.............#",
        "#.#.#.###.###########.#.#.#########.#",
        "#.#.....#.......#####.#.#.#######...#",
        "#.#.###.#####.#.#####.#.#.#######.###",
        "#............+#.......#..........P..#",
        "#####################################",
    ],
    5: [
        "###########################################",
        "#S......#*#.......#...............#.......#",
        "#####.#.#.#.#####.#.###########.#.#.#####.#",
        "#.....#.#.........#.............#.#.#####.#",
        "#.###.#.###.#.###.###.#####.###.#.#.#####.#",
        "#.#.#.......#.......................#...#.#",
        "#.#.#.###.###.###.#.#.#####.###.#.#.###.#.#",
        "#.#.#.#.......###.#.#.#####.............#.#",
        "#.#.#.#.#.#######.#.#.#####.###.#.#####.#.#",
        "#...................#.....#.#.............#",
        "#.#.#####.#######.###.#.#.#.#.#########.###",
        "#.#...#...............#...........#...#...#",
        "#.###.#.#.#####.#####.#######.#.#.#.#.#.#.#",
        "#.###.#.#.................#...........#...#",
        "#.###.#.#.#####.#######.#.#.###.#.#.#####.#",
        "#.....#.................#.....#.........#.#",
        "#####.#.#.#####.#.#.#########.#.#.###.#.#.#",
        "#........+....#.............#.#P....#.#.#.#",
        "#.###.#.#####.#.#.#.#.#####.#.#.#.#.#.#.#.#",
        "#.#.......#*......#.#.#####.#.#.#.#.#.....#",
        "#.#.#.#.#.#######.#.#.#####.#.#.#.#.#.#####",
        "#.#.....#.......#...#.#####.....#.#.#.#...#",
        "#.#.#.###.###.#.#####.#####.#.###.#.#.#.#.#",
        "#.......#.....#.#####.....#.......#.....#.#",
        "#.#.###.#######.#####.###.#.#######.#####.#",
        "#*#.......................#...............#",
        "###########################################",
    ],
}

_LEGENDA = {"#": 1, ".": 0, "S": 3, "P": 6, "*": 7, "+": 8, "~": 5}


def _paradas_do_jogador(grade, inicio=(1, 1)):
    """Todas as casas onde o jogador consegue parar deslizando (a partir do início)."""
    vistas = {inicio}
    fila = [inicio]
    while fila:
        linha, col = fila.pop()
        for dl, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            l, c = linha, col
            while grade[l + dl][c + dc] != 1:
                l += dl
                c += dc
            if (l, c) not in vistas:
                vistas.add((l, c))
                fila.append((l, c))
    return vistas


def _converter(linhas):
    grade = [[_LEGENDA[ch] for ch in linha] for linha in linhas]
    # moedas nas casas onde o jogador para (cantos e becos)
    for (l, c) in _paradas_do_jogador(grade):
        if grade[l][c] == 0:
            grade[l][c] = 4
    return grade


# Mantém o mesmo formato de antes: dicionário {numero_da_fase: matriz de ints}
Fases = {numero: _converter(linhas) for numero, linhas in _FASES_ASCII.items()}

# Posições dos inimigos em pixels (coluna*50+5, linha*50+5), longe do início
SPAWNS_INIMIGOS = {
    1: [(355, 405)],
    2: [(655, 605), (955, 755)],
    3: [(405, 455), (1155, 705), (955, 205)],
    4: [(1305, 55), (1055, 955), (1005, 355), (505, 155)],
    5: [(55, 505), (355, 805), (1605, 555), (605, 155), (1805, 1155)],
}

# Velocidades (px por frame). O jogador anda a 12, então sempre dá para fugir.
DIFICULDADE_INIMIGOS = {
    1: {"patrulha": 2.5, "investida": 5.5},
    2: {"patrulha": 2.5, "investida": 6.0},
    3: {"patrulha": 3.0, "investida": 6.5},
    4: {"patrulha": 3.0, "investida": 7.0},
    5: {"patrulha": 3.5, "investida": 7.5},
}

MAPA_ATUAL = Fases[1]
FASE_ATUAL = 1


def carregar_fase(numero_fase=1):
    global MAPA_ATUAL, FASE_ATUAL

    if numero_fase in Fases:
        MAPA_ATUAL = Fases[numero_fase]
        FASE_ATUAL = numero_fase
    else:
        print("Fases concluídas!")
        return None

    paredes = []
    for linha_idx, linha in enumerate(MAPA_ATUAL):
        for col_idx, tipo in enumerate(linha):
            if tipo == 1:
                x = col_idx * TAMANHO_BLOCO
                y = linha_idx * TAMANHO_BLOCO
                paredes.append(pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
    return paredes


# ---------------------------------------------------------------------------
#  VISUAL: cada fase tem um "templo" com uma cor de neon diferente
# ---------------------------------------------------------------------------
TEMAS = {
    1: dict(neon=(190, 70, 255), claro=(240, 190, 255), parede=(24, 12, 46), parede2=(38, 20, 70),
            runa=(78, 42, 124), fundo=(8, 6, 16), piso=(13, 10, 26), piso2=(17, 13, 32), ponto=(36, 28, 62)),
    2: dict(neon=(0, 210, 255), claro=(190, 245, 255), parede=(10, 24, 44), parede2=(16, 38, 68),
            runa=(28, 82, 120), fundo=(5, 9, 16), piso=(8, 15, 26), piso2=(10, 19, 32), ponto=(20, 42, 66)),
    3: dict(neon=(255, 60, 170), claro=(255, 200, 230), parede=(42, 12, 36), parede2=(64, 18, 54),
            runa=(120, 36, 96), fundo=(14, 6, 12), piso=(22, 10, 20), piso2=(28, 12, 25), ponto=(62, 28, 52)),
    4: dict(neon=(100, 130, 255), claro=(200, 215, 255), parede=(16, 18, 52), parede2=(26, 30, 82),
            runa=(48, 56, 132), fundo=(6, 7, 18), piso=(10, 11, 28), piso2=(13, 14, 34), ponto=(30, 34, 70)),
    5: dict(neon=(255, 100, 60), claro=(255, 215, 190), parede=(44, 16, 12), parede2=(68, 24, 16),
            runa=(124, 48, 32), fundo=(14, 6, 5), piso=(22, 10, 9), piso2=(28, 13, 11), ponto=(62, 30, 24)),
}

CORES = {
    "FUNDO": (10, 10, 18),
    "NEON_PRINCIPAL": (180, 50, 255),
    "NEON_TRILHA": (40, 30, 65),
    "MOEDA": (255, 215, 40),
    "AGUA": (0, 180, 255),
    "PORTAL": (0, 255, 150),
    "PAREDE_PREENCHIMENTO": (35, 15, 60),
    "PAREDE_INTERNO": (50, 25, 85)
}

superficie_escuridao = None


def inicializar_iluminacao(largura, altura):
    global superficie_escuridao
    superficie_escuridao = pygame.Surface((largura, altura), pygame.SRCALPHA)


def eh_parede(linha, col):
    if 0 <= linha < len(MAPA_ATUAL) and 0 <= col < len(MAPA_ATUAL[0]):
        return MAPA_ATUAL[linha][col] == 1
    return True


def _misturar(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _ruido(l, c, sal=0):
    """Número pseudo-aleatório fixo (0 a 1) para cada casa: textura sempre igual."""
    n = (l * 73856093) ^ (c * 19349663) ^ (sal * 83492791)
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


RAIO_CANTO = 16     # arredondamento dos cantos externos das paredes
ALCANCE_BRILHO = 9  # quantos pixels o neon "vaza" para dentro do corredor


def _piso(tela, x, y, l, c, tema):
    B = TAMANHO_BLOCO
    cor = _misturar(tema["piso"], tema["piso2"], _ruido(l, c, 1))
    pygame.draw.rect(tela, cor, (x, y, B, B))
    for dx, dy in ((7, 7), (B - 9, 7), (7, B - 9), (B - 9, B - 9)):
        pygame.draw.rect(tela, tema["ponto"], (x + dx, y + dy, 2, 2))


def _runa(tela, x, y, l, c, tema):
    """Entalhes decorativos no miolo das paredes grossas (estilo templo)."""
    cor = tema["runa"]
    cx, cy = x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2
    tipo = int(_ruido(l, c, 4) * 4) % 4
    if tipo == 0:      # quadrados concêntricos
        pygame.draw.rect(tela, cor, (cx - 12, cy - 12, 24, 24), 2)
        pygame.draw.rect(tela, cor, (cx - 5, cy - 5, 10, 10))
    elif tipo == 1:    # cruz com ponto
        pygame.draw.line(tela, cor, (cx - 13, cy), (cx + 13, cy), 2)
        pygame.draw.line(tela, cor, (cx, cy - 13), (cx, cy + 13), 2)
        pygame.draw.circle(tela, cor, (cx, cy), 5)
    elif tipo == 2:    # olho
        pygame.draw.ellipse(tela, cor, (cx - 14, cy - 7, 28, 14), 2)
        pygame.draw.circle(tela, cor, (cx, cy), 4)
    else:              # zigue-zague
        pts = [(cx - 14, cy + 6), (cx - 7, cy - 6), (cx, cy + 6), (cx + 7, cy - 6), (cx + 14, cy + 6)]
        pygame.draw.lines(tela, cor, False, pts, 2)


def _arco(superficie, cor, cx, cy, raio, a0, a1):
    pygame.draw.arc(superficie, cor, (cx - raio, cy - raio, raio * 2, raio * 2), a0, a1, 1)


def _parede(tela, brilho, l, c, tema):
    B = TAMANHO_BLOCO
    r = RAIO_CANTO
    x, y = c * B, l * B
    cima, baixo = eh_parede(l - 1, c), eh_parede(l + 1, c)
    esq, dire = eh_parede(l, c - 1), eh_parede(l, c + 1)

    # cantos externos (convexos) ficam arredondados
    c_te = (not cima) and (not esq)
    c_td = (not cima) and (not dire)
    c_bd = (not baixo) and (not dire)
    c_be = (not baixo) and (not esq)

    base = _misturar(tema["parede"], tema["parede2"], _ruido(l, c, 2) * 0.7)
    pygame.draw.rect(tela, base, (x, y, B, B),
                     border_top_left_radius=r if c_te else 0,
                     border_top_right_radius=r if c_td else 0,
                     border_bottom_right_radius=r if c_bd else 0,
                     border_bottom_left_radius=r if c_be else 0)

    # "lajota" de pedra no meio de cada bloco
    laje = _misturar(base, tema["parede2"], 0.8)
    pygame.draw.rect(tela, laje, (x + 6, y + 6, B - 12, B - 12), border_radius=4)

    if cima and baixo and esq and dire and _ruido(l, c, 3) > 0.78:
        _runa(tela, x, y, l, c, tema)

    # ---- contorno neon só nos lados voltados para o corredor ----
    neon, claro = tema["neon"], tema["claro"]
    rr = r - 1  # raio do traço nos cantos arredondados

    def brilho_cor(k):
        a = int(150 * (1 - k / (ALCANCE_BRILHO + 1)) ** 2)
        return (neon[0], neon[1], neon[2], a)

    if not cima:
        xa = x + (r if c_te else 0)
        xb = x + B - 1 - (r if c_td else 0)
        pygame.draw.line(tela, neon, (xa, y + 1), (xb, y + 1), 3)
        pygame.draw.line(tela, claro, (xa, y + 1), (xb, y + 1), 1)
        for k in range(1, ALCANCE_BRILHO + 1):
            pygame.draw.line(brilho, brilho_cor(k), (xa, y - k), (xb, y - k), 1)
    if not baixo:
        xa = x + (r if c_be else 0)
        xb = x + B - 1 - (r if c_bd else 0)
        pygame.draw.line(tela, neon, (xa, y + B - 2), (xb, y + B - 2), 3)
        pygame.draw.line(tela, claro, (xa, y + B - 2), (xb, y + B - 2), 1)
        for k in range(1, ALCANCE_BRILHO + 1):
            pygame.draw.line(brilho, brilho_cor(k), (xa, y + B - 1 + k), (xb, y + B - 1 + k), 1)
    if not esq:
        ya = y + (r if c_te else 0)
        yb = y + B - 1 - (r if c_be else 0)
        pygame.draw.line(tela, neon, (x + 1, ya), (x + 1, yb), 3)
        pygame.draw.line(tela, claro, (x + 1, ya), (x + 1, yb), 1)
        for k in range(1, ALCANCE_BRILHO + 1):
            pygame.draw.line(brilho, brilho_cor(k), (x - k, ya), (x - k, yb), 1)
    if not dire:
        ya = y + (r if c_td else 0)
        yb = y + B - 1 - (r if c_bd else 0)
        pygame.draw.line(tela, neon, (x + B - 2, ya), (x + B - 2, yb), 3)
        pygame.draw.line(tela, claro, (x + B - 2, ya), (x + B - 2, yb), 1)
        for k in range(1, ALCANCE_BRILHO + 1):
            pygame.draw.line(brilho, brilho_cor(k), (x + B - 1 + k, ya), (x + B - 1 + k, yb), 1)

    # arcos nos cantos arredondados (traço + brilho)
    cantos = (
        (c_te, x + r, y + r, math.pi / 2, math.pi),
        (c_td, x + B - r, y + r, 0, math.pi / 2),
        (c_bd, x + B - r, y + B - r, 3 * math.pi / 2, 2 * math.pi),
        (c_be, x + r, y + B - r, math.pi, 3 * math.pi / 2),
    )
    for ativo, cx, cy, a0, a1 in cantos:
        if not ativo:
            continue
        _arco(tela, neon, cx, cy, rr, a0, a1)
        _arco(tela, neon, cx, cy, rr - 1, a0, a1)
        _arco(tela, neon, cx, cy, rr + 1, a0, a1)
        _arco(tela, claro, cx, cy, rr, a0, a1)
        for k in range(1, ALCANCE_BRILHO + 1):
            _arco(brilho, brilho_cor(k), cx, cy, rr + k, a0, a1)


# ---------------------------------------------------------------------------
#  Itens do mapa (moeda, estrela, coração, portal, início, água)
# ---------------------------------------------------------------------------
def _estrela_pontos(cx, cy, r_ext, r_int):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        raio = r_ext if i % 2 == 0 else r_int
        pts.append((cx + math.cos(ang) * raio, cy + math.sin(ang) * raio))
    return pts


def _halo(brilho, cor, centro, raios_alfas):
    for raio, alfa in raios_alfas:
        pygame.draw.circle(brilho, (cor[0], cor[1], cor[2], alfa), centro, raio)


def _item_halo(brilho, tipo, x, y):
    """Parte do item que brilha (vai na camada translúcida)."""
    B = TAMANHO_BLOCO
    centro = (x + B // 2, y + B // 2)
    if tipo == 4:
        _halo(brilho, CORES["MOEDA"], centro, ((11, 22), (8, 44), (6, 80)))
    elif tipo == 7:
        _halo(brilho, CORES["MOEDA"], centro, ((22, 22), (17, 40), (12, 70)))
    elif tipo == 8:
        _halo(brilho, (255, 60, 140), centro, ((20, 24), (15, 44), (11, 72)))
    elif tipo == 6:
        _halo(brilho, CORES["PORTAL"], centro, ((32, 20), (27, 36), (22, 56), (17, 80)))


def _item(tela, tipo, x, y, tema):
    B = TAMANHO_BLOCO
    cx, cy = x + B // 2, y + B // 2
    if tipo == 4:      # moeda
        pygame.draw.circle(tela, CORES["MOEDA"], (cx, cy), 4)
        pygame.draw.circle(tela, (255, 250, 190), (cx - 1, cy - 1), 2)
    elif tipo == 7:    # estrela
        pygame.draw.polygon(tela, CORES["MOEDA"], _estrela_pontos(cx, cy, 14, 6))
        pygame.draw.polygon(tela, (255, 250, 200), _estrela_pontos(cx, cy, 8, 3.5))
    elif tipo == 8:    # coração
        rosa = (255, 60, 140)
        pygame.draw.circle(tela, rosa, (cx - 5, cy - 3), 6)
        pygame.draw.circle(tela, rosa, (cx + 5, cy - 3), 6)
        pygame.draw.polygon(tela, rosa, [(cx - 10, cy - 1), (cx + 10, cy - 1), (cx, cy + 11)])
        pygame.draw.circle(tela, (255, 190, 220), (cx - 6, cy - 5), 2)
    elif tipo == 6:    # portal
        verde = CORES["PORTAL"]
        pygame.draw.circle(tela, (6, 30, 26), (cx, cy), 21)
        pygame.draw.circle(tela, verde, (cx, cy), 21, 3)
        pygame.draw.circle(tela, (150, 255, 215), (cx, cy), 14, 1)
        pygame.draw.circle(tela, verde, (cx, cy), 8)
        pygame.draw.circle(tela, (230, 255, 245), (cx, cy), 3)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):   # 4 "dentes" em volta
            pygame.draw.line(tela, verde, (cx + dx * 21, cy + dy * 21), (cx + dx * 25, cy + dy * 25), 3)
    elif tipo == 3:    # marca do ponto de partida
        pygame.draw.circle(tela, tema["neon"], (cx, cy), 17, 1)
        pygame.draw.circle(tela, tema["ponto"], (cx, cy), 12, 1)
        pygame.draw.circle(tela, tema["claro"], (cx, cy), 3)
    elif tipo == 5:    # água
        pygame.draw.rect(tela, (12, 26, 52), (x + 3, y + 3, B - 6, B - 6), border_radius=6)
        pygame.draw.rect(tela, CORES["AGUA"], (x + 3, y + 3, B - 6, B - 6), 1, border_radius=6)
        for oy in (17, 31):
            pygame.draw.line(tela, CORES["AGUA"], (x + 12, y + oy), (x + B - 12, y + oy), 1)


def desenhar_mapa(tela: pygame.Surface):
    """Pré-desenha a fase inteira (chamado 1x por fase): piso, paredes de pedra
    com contorno neon arredondado e brilho, runas, moedas e portal."""
    B = TAMANHO_BLOCO
    tema = TEMAS.get(FASE_ATUAL, TEMAS[1])
    tela.fill(tema["fundo"])
    brilho = pygame.Surface(tela.get_size(), pygame.SRCALPHA)

    # 1) piso em todas as casas (os cantos arredondados das paredes mostram o piso)
    for l, linha in enumerate(MAPA_ATUAL):
        for c, _ in enumerate(linha):
            _piso(tela, c * B, l * B, l, c, tema)

    # 2) paredes (corpo, entalhes, contorno e brilho)
    for l, linha in enumerate(MAPA_ATUAL):
        for c, tipo in enumerate(linha):
            if tipo == 1:
                _parede(tela, brilho, l, c, tema)

    # 3) halos dos itens na camada translúcida
    for l, linha in enumerate(MAPA_ATUAL):
        for c, tipo in enumerate(linha):
            if tipo in (4, 6, 7, 8):
                _item_halo(brilho, tipo, c * B, l * B)

    # 4) junta o brilho e desenha os itens por cima
    tela.blit(brilho, (0, 0))
    for l, linha in enumerate(MAPA_ATUAL):
        for c, tipo in enumerate(linha):
            if tipo in (3, 4, 5, 6, 7, 8):
                _item(tela, tipo, c * B, l * B, tema)


def aplicar_iluminacao_pro(tela: pygame.Surface, centro_jogador: tuple):
    """Escuridão com um círculo de luz suave em volta do jogador.
    Centro totalmente claro, bordas escurecendo aos poucos e o resto do mapa
    ainda levemente visível (antes era quase preto e o centro ficava escuro)."""
    if superficie_escuridao is None:
        return

    alfa_fora = 205        # escuridão longe do jogador (antes 245)
    raio_maximo = 300      # alcance da luz (antes 190)
    passos = 22

    superficie_escuridao.fill((6, 5, 12, alfa_fora))
    for i in range(passos):
        raio = raio_maximo - i * (raio_maximo // passos)
        alfa = int(alfa_fora * (1 - i / (passos - 1)))
        pygame.draw.circle(superficie_escuridao, (6, 5, 12, alfa), centro_jogador, raio)

    tela.blit(superficie_escuridao, (0, 0))
