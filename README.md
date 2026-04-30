Alunas: Ana Câdida de Azevedo Santos, Emilly Vitória Dutra Batista e Júlia Dutra Fernandes.

1-
Título do jogo: Core-sync,( protocolo de sobrecarga.)
Um jogo onde o objetivo é ajudar um robô a fugir de uma exploxão nuclear.
O nosso jogo é um jogo de arcade 2D em um ritmo rápido, estilo pixel art focado em labirintos verticais e infinitos.
O jogo acontecerá em labirintos(corredores de um laboratorio), onde o jogador deve chegar ao final para avançar de fase.
Nossa ideial surgiu por meio de uma história criada por nós mesmas, que é a seguinte: 
Um robô estava trabalhando em um laboratorio nuclear, até que aconteceu uma explosão em umas da usinas e espalhou plasma para todas as direções, e é ai que o jogador entra, com o objetivo de ajudar o robô a fugir do laboratorio e do plasma que sai da usinas nucleares e persegue o robô.

2-
Para passar de nível e vencer o jogo, o jogador tem que chegar ao final do labirinto,desviando do plasma, e coletando itens. 

3. Personagem Principal
O personagem principal é um robô de energia neon.
Ele não anda livremente, ao apertar uma direção, ele desliza automaticamente até bater em uma parede ou obstáculo
Os atributos dos personagem são:
Vida
Velocidade
Pontuação
Escudo (temporário)
Ímã de coleta (temporário)
rastro visual (ghost effect)
e um brilho circular em volta do personagem

4. Inimigos e Obstáculos
Os Obstáculos:
Espinhos,Paredes,Áreas proibidas
Os Inimigos:
Onda de plasma (principal ameaça)
Comportamentos:
Paredes:Bloqueiam movimento
Espinhos:Dano ao tocar
Plasma:Sobe continuamente pelo mapa
Ao colidir:
* parede → gera partículas
* espinho → perde vida
* plasma → morte imediata ou dano crítico
  
 5. Cenário (Mapa)
O jogo acontece em labirintos q vc passa por fase.
 Elementos do mapa:
Paredes
Corredores
Espinhos
Moedas
Pontos
Power-ups
O mapa é construído com pedaços pré-fabricados conectados automaticamente.
Isso garante:
caminhos válidos
variedade

6. Sistema de Pontuação
O jogador acumula pontos ao:
Coletar pontos básicos
Coletar moedas
Sobreviver mais tempo
Subir mais alto no mapa
Os pontos tem Valores:
Ponto comum = 5 pontos
Moeda = 10 pontos
Sobrevivência = bônus progressivo

7. Sistema de Vida
Vida inicial:3 vidas
Perda de vida:
 Encostar em espinhos
 Ser atingido por perigos
Fim do jogo:Quando as vidas chegam a zero.

8. Controles
Teclas:
*W ou seta para cima*
→ subir
*A ou seta para esquerda*
→ esquerda
*S ou seta para baixo*
→ descer
*D ou seta para direita*
→ direita
*ESC*
→ sair do jogo

9. Fluxo do Jogo
1. Tela inicial
2. Início da partida
3. Geração do mapa
4. Movimentação e coleta
5. Plasma sobe continuamente
6. Dificuldade aumenta com o passar de fases
7. Game Over
 Vitória:
O jogo é por fases, então a meta é passar delas e ir aumentando a dificuldade.
 Derrota:
vidas zeradas
plasma alcança o jogador
 
 10. Regras do Jogo
O jogador só para ao colidir
Não pode atravessar paredes
Espinhos causam dano
Plasma sobe sem parar
Itens só podem ser coletados por contato
Movimento segue uma grade lógica

11. Estrutura do Projeto
```text
Core-sync/
│── main.py
│── player.py
│── enemy.py
│── map.py
│── items.py
│── effects.py
│── settings.py
│── assets/
│   ├── sprites/
│   ├── sounds/
│   └── particles/
│── README.md
```
 Responsabilidades:
*main.py*
→ execução principal
*player.py*
→ lógica do jogador
*enemy.py*
→ plasma e obstáculos
*map.py*
→ geração do mapa
*items.py*
→ moedas e power-ups
*effects.py*
→ partículas e efeitos visuais
*settings.py*
→ configurações gerais

12. Funcionalidades Mínimas
Versão inicial obrigatória:
Movimento deslizante
Sistema de colisão
Mapa funcional
Coleta de pontos
Sistema de vidas
Sistema de score
Plasma subindo
Game over

13. Melhorias Futuras
Possíveis melhorias:
* Novos power-ups
* Novos tipos de obstáculos
* Skins para personagem
* Sons dinâmicos
* Efeitos visuais avançados
* Modo desafio
Requisitos Funcionais
* Movimento deslizante automático
* Colisão com paredes
* Partículas ao impacto
* Sistema de pontos e moedas
* Plasma subindo continuamente
* Itens temporários
Requisitos Não Funcionais
* Movimento em grade lógica
* Geração procedural com blocos
* Alto contraste visual
* Buffer de input para fluidez
* Performance estável
Diferenciais Técnicos
* Ghost effect durante movimento
* Colisão precisa com pygame.mask
* Sistema de iluminação local
* Partículas de impacto
* Visual neon minimalista

