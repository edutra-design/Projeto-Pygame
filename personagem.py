import pygame
import os

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
        if self.sprite is not None:
            tela.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(tela, self.cor, self.obter_rect())

        

class Jogador(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (0, 255, 255)) # Ciano Neon
        self.velocidade = 12.0
        self.direcao_x = 0
        self.direcao_y = 0
        self.direcao_visual = "baixo"
        self.buffer_x = 0
        self.buffer_y = 0
        self.tamanho_bloco = 50 # Tamanho da grade do mapa para alinhar
        
    
        pasta_assets = os.path.join(
        os.path.dirname(__file__), 
        "assets",
        "personagem"
        )

        self.animacoes = {}
        self.frame_atual = 0
        self.intervalo_animacao = 120
        self.ultimo_frame = pygame.time.get_ticks()
        self.invulneravel_ate = 0

        try:
            caminho_idle = os.path.join(
                pasta_assets, 
                "robo_idle.png"
                )
            imagem_idle = pygame.image.load(
                caminho_idle).convert_alpha()
            self.sprite_original = pygame.transform.scale(
                imagem_idle,
                (tamanho, tamanho)
            )

            self.sprite = self.sprite_original

            for direcao in ["baixo", "cima", "esquerda", "direita"]:
                quadros = []

                for numero in range(1, 5):
                    caminho = os.path.join(
                        pasta_assets,
                        f"{direcao}_{numero}.png"
                    )

                    imagem = pygame.image.load(
                        caminho
                    ).convert_alpha()

                    imagem = pygame.transform.scale(
                        imagem,
                        (tamanho, tamanho)
                    )

                    quadros.append(imagem)

                self.animacoes[direcao] = quadros

            print("Todas as animações foram carregadas!")

        except Exception as erro:
            print("Erro ao carregar sprites:", erro)
            self.sprite_original = None
            self.sprite = None
            self.animacoes = {}


    def mover(self, largura_tela: int, altura_tela: int, lista_paredes: list, gerenciador_efeitos):
        """Movimentação fluida com alinhamento inteligente para não travar nas quinas."""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_d]:
            print("Tecla D pressionada")
        
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

        # Atualiza a direção visual do personagem
        if self.direcao_x == -1:
            self.direcao_visual = "esquerda"
        elif self.direcao_x == 1:
            self.direcao_visual = "direita"
        elif self.direcao_y == -1:
            self.direcao_visual = "cima"
        elif self.direcao_y == 1:
            self.direcao_visual = "baixo"

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
    
    def desenhar(self, tela):
        em_movimento = (
            self.direcao_x != 0 or self.direcao_y != 0
        )

        if em_movimento and self.animacoes:
            quadros = self.animacoes.get(
                self.direcao_visual, []
            )

            if quadros:
                agora = pygame.time.get_ticks()

                if agora - self.ultimo_frame >= self.intervalo_animacao:
                    self.frame_atual = (
                        self.frame_atual + 1
                    ) % len(quadros)

                    self.ultimo_frame = agora

                imagem = quadros[self.frame_atual]
            else:
                imagem = self.sprite_original
        else:
            imagem = self.sprite_original
            self.frame_atual = 0

        agora = pygame.time.get_ticks()

        if agora < self.invulneravel_ate:

            # Pisca a cada 100 milissegundos
            if (agora // 100) % 2 == 0:
                if imagem is not None:
                    tela.blit(imagem, (int(self.x), int(self.y)))
                else:
                    pygame.draw.rect(tela, self.cor, self.obter_rect())

        else:
            if imagem is not None:
                tela.blit(imagem, (int(self.x), int(self.y)))
            else:
                pygame.draw.rect(tela, self.cor, self.obter_rect())

