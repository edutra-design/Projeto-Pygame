#personagem.py
import pygame

class Entidade:
    """Classe base para as entidades do jogo."""
    def __init__(self, x: float, y: float, tamanho: int, cor: tuple):
        self.x = float(x)
        self.y = float(y)
        self.tamanho = tamanho
        self.cor = cor
        self.sprite = None

    def obter_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.tamanho, self.tamanho)

    def desenhar(self, tela: pygame.Surface):
        if self.sprite:
            tela.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(tela, self.cor, self.obter_rect())


class Jogador(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (0, 255, 255)) # Ciano Neon
        self.velocidade = 12.0
        self.direcao_x = 0
        self.direcao_y = 0
        self.buffer_x = 0
        self.buffer_y = 0
        self.tamanho_bloco = 50 # Tamanho da grade do mapa para alinhar

        try:
            sprite_original = pygame.image.load("assets/Mad_Mask.webp").convert_alpha()
            self.sprite = pygame.transform.scale(sprite_original, (tamanho, tamanho))
        except FileNotFoundError:
            pass

    def mover(self, largura_tela: int, altura_tela: int, lista_paredes: list, gerenciador_efeitos):
        """Movimentação fluida com alinhamento inteligente para não travar nas quinas."""
        teclas = pygame.key.get_pressed()
        
        # Captura os comandos
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:     self.buffer_x, self.buffer_y = -1, 0
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  self.buffer_x, self.buffer_y = 1, 0
        elif teclas[pygame.K_w] or teclas[pygame.K_UP]:     self.buffer_x, self.buffer_y = 0, -1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:   self.buffer_x, self.buffer_y = 0, 1

        # Só aceita novo comando se estiver parado ou prestes a alinhar
        if self.direcao_x == 0 and self.direcao_y == 0:
            if self.buffer_x != 0 or self.buffer_y != 0:
                self.direcao_x = self.buffer_x
                self.direcao_y = self.buffer_y
                self.buffer_x, self.buffer_y = 0, 0

        # Aplica efeito de rastro se estiver em movimento
        if self.direcao_x != 0 or self.direcao_y != 0:
            gerenciador_efeitos.adicionar_rastro(self.x, self.y, self.tamanho, self.cor)

        # --- SISTEMA DE ALINHAMENTO AUTOMÁTICO (ANTI-TRAVAMENTO) ---
        # Se estiver se movendo verticalmente, alinha o X perfeitamente com a grade
        if self.direcao_y != 0:
            centro_bloco_x = (round((self.x - 5) / self.tamanho_bloco) * self.tamanho_bloco) + 5
            if abs(self.x - centro_bloco_x) < self.velocidade:
                self.x = centro_bloco_x
            elif self.x < centro_bloco_x:
                self.x += min(self.velocidade, centro_bloco_x - self.x)
            elif self.x > centro_bloco_x:
                self.x -= min(self.velocidade, self.x - centro_bloco_x)

        # Se estiver se movendo horizontalmente, alinha o Y perfeitamente com a grade
        if self.direcao_x != 0:
            centro_bloco_y = (round((self.y - 5) / self.tamanho_bloco) * self.tamanho_bloco) + 5
            if abs(self.y - centro_bloco_y) < self.velocidade:
                self.y = centro_bloco_y
            elif self.y < centro_bloco_y:
                self.y += min(self.velocidade, centro_bloco_y - self.y)
            elif self.y > centro_bloco_y:
                self.y -= min(self.velocidade, self.y - centro_bloco_y)

        # --- FÍSICA PADRÃO DE COLISÃO ---
        # Colisão no Eixo X
        pos_antiga_x = self.x
        self.x += self.direcao_x * self.velocidade
        rect_jogador = self.obter_rect()
        if self.x < 0 or self.x > largura_tela - self.tamanho or any(rect_jogador.colliderect(p) for p in lista_paredes):
            self.x = pos_antiga_x
            self.direcao_x = 0

        # Colisão no Eixo Y
        pos_antiga_y = self.y
        self.y += self.direcao_y * self.velocidade
        rect_jogador = self.obter_rect()
        if self.y < 0 or self.y > altura_tela - self.tamanho or any(rect_jogador.colliderect(p) for p in lista_paredes):
            self.y = pos_antiga_y
            self.direcao_y = 0
