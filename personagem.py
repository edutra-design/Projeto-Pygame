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

        self.sprite = pygame.image.load(
            "assets/Mad_Mask.webp"
        ).convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite,
            (tamanho, tamanho)
        )

    def mover(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w]:
            self.y -= self.velocidade

        if teclas[pygame.K_s]:
            self.y += self.velocidade

        if teclas[pygame.K_a]:
            self.x -= self.velocidade

        if teclas[pygame.K_d]:
            self.x += self.velocidade

    def desenhar(self, tela):

        self.mover()  # movimenta antes de desenhar

        tela.blit(
            self.sprite,
            (self.x, self.y)
        )
