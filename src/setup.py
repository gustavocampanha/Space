import os
import pygame

# Defina os caminhos para as pastas necessárias
source_folder = os.path.dirname(__file__)
img_folder = os.path.join(source_folder, "img")
sound_folder = os.path.join(source_folder, "sounds")
font_folder = os.path.join(source_folder, "fonts")
save_folder = os.path.join(source_folder, "save")

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

# Dimensões da tela
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h

# Frames por segundo
FPS = 30