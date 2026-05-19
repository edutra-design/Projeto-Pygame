import pygame

class Entidade:

    def __init__(self, x, y, tamanho, caminho_imagem):
        self.x = x
        self.y = y
        self.tamanho = tamanho
      try: 
        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(image_original, (self.tamanho, self.tamanho))
except FileNotFoundError:
    print(f"Aviso: Imagem '{caminho_imagem}' não encontrada.")
    self.imagem = pygame.Surface((self.tamanho, self.tamanho))
    self.imagem.fill((255, 0, 255))

class Jogador(Entidade):

    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho, "assets/sprites/nucleos_neon.png")

        self.vel_x = 0
        self.vel_y = 0
        self.velocidade_deslize = 8
        self.deslizando = False
      
    def comando_mover(self, dx, dy):
      if not self.deslizando:
        self.vel_x = dx * self.velocidade_deslize
        self.vel_y = dy * self.velocidade_deslize
        self.deslizando = True

    def update(self, paredes):
      self.x += self.vel_x # Ana: parei aqui
    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            self.cor,
            (self.x, self.y, self.tamanho, self.tamanho)
        )
