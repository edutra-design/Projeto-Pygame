# efeitos.py
import pygame
import random

class EfeitoRastro:
    """Gerenciador avançado de efeitos visuais neon com gradiente e física de partículas."""
    def __init__(self):
        self.rastros = []
        self.particulas = []

    def adicionar_rastro(self, x: float, y: float, tamanho: int, cor_base: tuple):
        """Registra a posição da entidade para criar a esteira de luz degradê."""
        self.rastros.append({
            'pos_x': float(x),
            'pos_y': float(y),
            'alfa': 180,           # Opacidade inicial alta para dar brilho
            'tamanho_original': tamanho,
            'tamanho_atual': float(tamanho),
            'cor_base': cor_base
        })
        
        # 50% de chance de soltar faíscas de plasma com variação de cor neon
        if random.random() < 0.5:
            # Mistura um tom de roxo/rosa neon nas faíscas azuis para dar efeito de energia
            cor_faisca = random.choice([cor_base, (255, 0, 128), (180, 50, 255)])
            self.adicionar_faisca(x + tamanho//2, y + tamanho//2, cor_faisca)

    def adicionar_faisca(self, x_centro: float, y_centro: float, cor: tuple):
        """Cria pequenas partículas com direções explosivas aleatórias."""
        for _ in range(random.randint(3, 5)):
            self.particulas.append({
                'x': float(x_centro),
                'y': float(y_centro),
                'vel_x': random.uniform(-4.0, 4.0),
                'vel_y': random.uniform(-4.0, 4.0),
                'atrito': 0.92,     # Faz a partícula frear gradativamente no ar
                'tamanho': random.uniform(3.0, 7.0),
                'alfa': 255,
                'cor': cor
            })

    def atualizar_e_desenhar(self, tela: pygame.Surface):
        """Atualiza e renderiza os efeitos com fusão de cores e redução de escala."""
        
        # --- 1. PROCESSAR RASTRO PRINCIPAL (GRADIENTE E ENCOLHIMENTO) ---
        for rastro in self.rastros[:]:
            rastro['alfa'] -= 12  # Velocidade do fade-out
            
            if rastro['alfa'] <= 0:
                self.rastros.remove(rastro)
                continue

            # Evolução 1: Encolhe o rastro baseado no tempo de vida (alfa)
            fator_vida = rastro['alfa'] / 180.0
            rastro['tamanho_atual'] = rastro['tamanho_original'] * (0.3 + 0.7 * fator_vida)

            # Evolução 2: Gradiente dinâmico (Interpola do Ciano para o Roxo/Preto)
            r = int(rastro['cor_base'][0] * fator_vida + 50 * (1 - fator_vida))
            g = int(rastro['cor_base'][1] * fator_vida + 0 * (1 - fator_vida))
            b = int(rastro['cor_base'][2] * fator_vida + 150 * (1 - fator_vida))
            cor_gradiente = (max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255)))

            # Cria superfície e centraliza o desenho para o encolhimento não deslocar o rastro
            tam = int(rastro['tamanho_atual'])
            if tam > 1:
                surf_rastro = pygame.Surface((tam, tam), pygame.SRCALPHA)
                surf_rastro.fill((*cor_gradiente, rastro['alfa']))
                
                # Ajusta a posição para o quadrado encolher focado no centro original
                offset = (rastro['tamanho_original'] - tam) // 2
                tela.blit(surf_rastro, (int(rastro['pos_x'] + offset), int(rastro['pos_y'] + offset)))

        # --- 2. PROCESSAR FAÍSCAS (FÍSICA DE ARRASTO) ---
        for p in self.particulas[:]:
            p['alfa'] -= 15  # Faíscas somem mais rápido
            
            if p['alfa'] <= 0:
                self.particulas.remove(p)
                continue

            # Aplica atrito nas velocidades (Evolução 3)
            p['vel_x'] *= p['atrito']
            p['vel_y'] *= p['atrito']
            
            # Atualiza posição espacial
            p['x'] += p['vel_x']
            p['y'] += p['vel_y']
            
            # Encolhe a faísca levemente
            p['tamanho'] *= 0.95

            tam_p = int(p['tamanho'])
            if tam_p > 1:
                surf_particula = pygame.Surface((tam_p, tam_p), pygame.SRCALPHA)
                surf_particula.fill((*p['cor'], p['alfa']))
                tela.blit(surf_particula, (int(p['x']), int(p['y'])))
