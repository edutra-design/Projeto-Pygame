import pygame
import random
from personagem import Entidade
import os
#A classe "inimigos" é abstrata da classe "entidade" que serve como modelo para os elementos do jogo
class Inimigo(Entidade):
    def __init__(self, x: float, y: float, tamanho: int):
        super().__init__(x, y, tamanho, (255, 50, 50)) # Vermelho Neon
        self.velocidade_patrulha = 3.0
        self.velocidade_investida = 8.0
        self.estado = "PATRULHA"
        self.direcao_x, self.direcao_y = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        
        caminho_sprite = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "assets",
            "inimigos",
            "sentinela.png"
        )

        self.animacoes = []
        pasta_sprites = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "assets",
            "inimigos"
        )

        for i in range(1,5):
            caminho = os.path.join(pasta_sprites, f"sentinela_{i}.png")
            quadro = pygame.image.load(caminho).convert_alpha()
            quadro = pygame.transform.scale(quadro, (tamanho, tamanho))
            self.animacoes.append(quadro)

        self.frame_atual = 0
        self.intervalo_animacao = 120
        self.ultimo_frame = pygame.time.get_ticks()

        imagem = pygame.image.load(caminho_sprite).convert_alpha()

        self.sprite = pygame.transform.scale(
            imagem,
            (tamanho, tamanho)
        )
        
    def atualizar_ia(self, largura_tela: int, altura_tela: int, lista_paredes: list, jogador: Entidade):
        """Gerencia patrulha e investida rápida se avistar o jogador."""
        if self.estado == "PATRULHA":
            # Visão Horizontal
            if abs(self.y - jogador.y) < self.tamanho // 2:
                dir_x = 1 if jogador.x > self.x else -1
                linha_visao = pygame.Rect(int(self.x), int(self.y), int(jogador.x - self.x), self.tamanho)
                if not any(linha_visao.colliderect(p) for p in lista_paredes):
                    self.estado = "ALERTA"
                    self.direcao_x, self.direcao_y = dir_x, 0
            # Visão Vertical
            elif abs(self.x - jogador.x) < self.tamanho // 2:
                dir_y = 1 if jogador.y > self.y else -1
                linha_visao = pygame.Rect(int(self.x), int(self.y), self.tamanho, int(jogador.y - self.y))
                if not any(linha_visao.colliderect(p) for p in lista_paredes):
                    self.estado = "ALERTA"
                    self.direcao_x, self.direcao_y = 0, dir_y

        vel = self.velocidade_investida if self.estado == "ALERTA" else self.velocidade_patrulha

        pos_antiga_x, pos_antiga_y = self.x, self.y
        self.x += self.direcao_x * vel
        self.y += self.direcao_y * vel
        
        rect_inimigo = self.obter_rect()
        colidiu = False
        
        if self.x < 0 or self.x > largura_tela - self.tamanho or self.y < 0 or self.y > altura_tela - self.tamanho:
            colidiu = True
        elif any(rect_inimigo.colliderect(p) for p in lista_paredes):
            colidiu = True

        if colidiu:
            self.x, self.y = pos_antiga_x, pos_antiga_y
            self.estado = "PATRULHA"
            if self.direcao_x != 0:
                self.direcao_x = 0
                self.direcao_y = random.choice([-1, 1])
            else:
                self.direcao_y = 0
                self.direcao_x = random.choice([-1, 1])
        self.atualizar_animacao()

    def checar_colisao(self, jogador: Entidade) -> bool:
        return self.obter_rect().colliderect(jogador.obter_rect())

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_frame >= self.intervalo_animacao:
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes)
            self.ultimo_frame = agora

        if self.direcao_x < 0:
            self.sprite = pygame.transform.flip(
                self.animacoes[self.frame_atual],
                True,
                False
            )
        else:
            self.sprite = self.animacoes[self.frame_atual]
