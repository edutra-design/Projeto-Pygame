
import numpy as np
import os
import wave

# Configurações
TAXA_AMOSTRAGEM = 44100
VOLUME = 0.5

# Localização da pasta audio
PASTA_AUDIO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "audio"
)

os.makedirs(PASTA_AUDIO, exist_ok=True)


def criar_som(nome, frequencias, duracao_nota):
    partes = []

    for frequencia in frequencias:
        tempo = np.linspace(
            0,
            duracao_nota,
            int(TAXA_AMOSTRAGEM * duracao_nota),
            endpoint=False
        )

        onda = np.sin(2 * np.pi * frequencia * tempo)

        # Evita cortes bruscos no som
        envelope = np.linspace(0, 1, len(onda))
        envelope *= np.linspace(1, 0, len(onda))

        onda *= envelope * VOLUME
        partes.append(onda)

    audio = np.concatenate(partes)

    audio = np.int16(audio * 32767)

    caminho = os.path.join(PASTA_AUDIO, nome)

    with wave.open(caminho, "wb") as ficheiro:
        ficheiro.setnchannels(1)
        ficheiro.setsampwidth(2)
        ficheiro.setframerate(TAXA_AMOSTRAGEM)
        ficheiro.writeframes(audio.tobytes())

    print("Criado:", nome)


# Efeitos sonoros do Core-sync
criar_som("moeda.wav", [900, 1300], 0.09)

criar_som("estrela.wav", [700, 1100, 1600], 0.12)

criar_som("dano.wav", [220, 140], 0.15)

criar_som("game_over.wav", [500, 350, 220], 0.25)

print("\nTodos os sons foram criados!")


def criar_musica():
    duracao_nota = 0.14
    notas = [440, 523, 659, 784, 659, 523, 880, 784,
             659, 784, 988, 880, 784, 659, 523, 440]

    partes = []

    for frequencia in notas:
        tempo = np.linspace(
            0,
            duracao_nota,
            int(TAXA_AMOSTRAGEM * duracao_nota),
            endpoint=False
        )

        # Som eletrónico 8-bit
        onda = np.sign(np.sin(2 * np.pi * frequencia * tempo))

        # Volume diminui no final de cada nota
        envelope = np.linspace(1, 0.2, len(onda))
        onda *= envelope * 0.18

        partes.append(onda)

    audio = np.concatenate(partes)

    # Converter para formato WAV
    audio = np.int16(audio * 32767)

    caminho = os.path.join(PASTA_AUDIO, "musica_fundo.wav")

    with wave.open(caminho, "wb") as ficheiro:
        ficheiro.setnchannels(1)
        ficheiro.setsampwidth(2)
        ficheiro.setframerate(TAXA_AMOSTRAGEM)
        ficheiro.writeframes(audio.tobytes())

    print("Música de fundo criada!")


def criar_musica_menu():
    duracao_nota = 0.45

    # Melodia calma, futurista e misteriosa
    notas = [
        440, 523, 659, 523,
        392, 494, 587, 494,
        440, 523, 659, 784,
        659, 523, 440, 392
    ]

    partes = []

    for frequencia in notas:
        tempo = np.linspace(
            0,
            duracao_nota,
            int(TAXA_AMOSTRAGEM * duracao_nota),
            endpoint=False
        )

        # Som suave com uma onda sinusoidal
        onda = np.sin(2 * np.pi * frequencia * tempo)

        envelope = np.linspace(0, 1, len(onda))
        envelope *= np.linspace(1, 0.3, len(onda))

        onda *= envelope * 0.12
        partes.append(onda)

    audio = np.concatenate(partes)
    audio = np.int16(audio * 32767)

    caminho = os.path.join(PASTA_AUDIO, "musica_menu.wav")

    with wave.open(caminho, "wb") as ficheiro:
        ficheiro.setnchannels(1)
        ficheiro.setsampwidth(2)
        ficheiro.setframerate(TAXA_AMOSTRAGEM)
        ficheiro.writeframes(audio.tobytes())

    print("Música do menu criada!")


criar_musica()

criar_som("clique.wav", [800, 1200], 0.06)
criar_som("vitoria.wav", [523, 659, 784, 1047], 0.20)

criar_musica_menu()