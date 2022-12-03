# Importe as bibliotecas necessárias
import pygame
import setup as st

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

# Crie a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Space Oddity")

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()