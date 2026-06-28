import pygame

class Entidade:
    """Classe base para todas as entidades móveis do jogo."""
    def __init__(self, x: float, y: float, tamanho: int, cor: tuple):
        self.x = float(x)
        self.y = float(y)
        self.tamanho = tamanho
        self.cor = cor
        self.sprite = None

    def obter_rect(self) -> pygame.Rect:
        """Retorna o retângulo de colisão (hitbox) atual da entidade."""
        return pygame.Rect(int(self.x), int(self.y), self.tamanho, self.tamanho)

    def desenhar(self, tela: pygame.Surface):
        """Renderiza a entidade usando sprite ou fallback para vetor geométrico."""
        if self.sprite:
            tela.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(tela, self.cor, self.obter_rect())


class Jogador(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (0, 255, 255))
        self.velocidade = 600.0  # Pixels por segundo (Independente de FPS)
        
        # Vetores de movimento atual
        self.direcao_x = 0
        self.direcao_y = 0
        
        # Input Buffering: Armazena o próximo comando enquanto desliza
        self.buffer_x = 0
        self.buffer_y = 0
        
        try:
            sprite_original = pygame.image.load("assets/Mad_Mask.webp").convert_alpha()
            self.sprite = pygame.transform.scale(sprite_original, (tamanho, tamanho))
        except FileNotFoundError:
            pass

    def mover(self, largura_tela: int, altura_tela: int, lista_paredes: list, dt: float):
        """Processa a movimentação contínua por deslize com Input Buffering e Delta Time."""
        teclas = pygame.key.get_pressed()
        
        # 1. Captura e armazena inputs no Buffer a qualquer momento do deslize
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.buffer_x, self.buffer_y = -1, 0
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.buffer_x, self.buffer_y = 1, 0
        elif teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.buffer_x, self.buffer_y = 0, -1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.buffer_x, self.buffer_y = 0, 1

        # 2. Se estiver parado, consome o comando armazenado no Buffer
        if self.direcao_x == 0 and self.direcao_y == 0:
            self.direcao_x = self.buffer_x
            self.direcao_y = self.buffer_y
            self.buffer_x, self.buffer_y = 0, 0  # Limpa o buffer após o consumo

        # 3. Cálculo preditivo de movimento usando Delta Time
        passo_x = self.direcao_x * self.velocidade * dt
        passo_y = self.direcao_y * self.velocidade * dt

        # Move e testa colisões no eixo X
        if passo_x != 0:
            self.x += passo_x
            rect_futuro = self.obter_rect()
            
            # Colisão com limites horizontais da tela
            if self.x < 0:
                self.x = 0
                self.direcao_x = 0
            elif self.x > largura_tela - self.tamanho:
                self.x = float(largura_tela - self.tamanho)
                self.direcao_x = 0
                
            # Colisão com objetos do mapa
            for parede in lista_paredes:
                if rect_futuro.colliderect(parede):
                    if passo_x > 0:  # Movendo para a direita
                        self.x = float(parede.left - self.tamanho)
                    else:            # Movendo para a esquerda
                        self.x = float(parede.right)
                    self.direcao_x = 0
                    break

        # Move e testa colisões no eixo Y
        if passo_y != 0:
            self.y += passo_y
            rect_futuro = self.obter_rect()
            
            # Colisão com limites verticais da tela
            if self.y < 0:
                self.y = 0
                self.direcao_y = 0
            elif self.y > altura_tela - self.tamanho:
                self.y = float(altura_tela - self.tamanho)
                self.direcao_y = 0
                
            # Colisão com objetos do mapa
            for parede in lista_paredes:
                if rect_futuro.colliderect(parede):
                    if passo_y > 0:  # Movendo para baixo
                        self.y = float(parede.top - self.tamanho)
                    else:            # Movendo para cima
                        self.y = float(parede.bottom)
                    self.direcao_y = 0
                    break
