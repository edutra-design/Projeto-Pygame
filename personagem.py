import pygame

class Entidade:
    def __init__(self, x, y, tamanho, cor):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.cor = cor


class Jogador(Entidade):
    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho, (0, 255, 255))
        
        self.velocidade = 5
        
        # Carrega e redimensiona o sprite do seu personagem
        self.sprite = pygame.image.load("assets/Mad_Mask.webp").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (tamanho, tamanho))

    def mover(self, largura_tela, altura_tela):
        teclas = pygame.key.get_pressed()
        
        # Variáveis para detectar a direção do movimento
        dx = 0
        dy = 0

        # Aceita tanto as letras (WASD) quanto as setas do teclado
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:   # Esquerda
            dx = -1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  # Direita
            dx = 1
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:     # Cima
            dy = -1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:   # Baixo
            dy = 1

        # Correção da velocidade diagonal (Teorema de Pitágoras)
        if dx != 0 and dy != 0:
            self.x += dx * self.velocidade * 0.7071
            self.y += dy * self.velocidade * 0.7071
        else:
            self.x += dx * self.velocidade
            self.y += dy * self.velocidade

        # --- BARREIRAS DA TELA ---
        if self.x < 0:
            self.x = 0
        elif self.x > largura_tela - self.tamanho:
            self.x = largura_tela - self.tamanho

        if self.y < 0:
            self.y = 0
        elif self.y > altura_tela - self.tamanho:
            self.y = altura_tela - self.tamanho

    def desenhar(self, tela):
        # Apenas desenha o sprite na posição atual
        tela.blit(self.sprite, (self.x, self.y))
