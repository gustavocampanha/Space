# Importe as bibliotecas necessárias
import json
import os
import pygame
import sys

import gaming_elements as ge
import interface as it
import setup as st

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

# Crie a tela
screen = pygame.display.set_mode((st.WIDTH, st.HEIGHT), pygame.FULLSCREEN)

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Space Oddity")

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

# Define a classe principal do jogo, responsável pelas telas e ações da aplicação
class Game():
    
    # Define o método construtor da classe
    def __init__(self):

        self.in_menu = True
        self.game_is_running = False
        self.pause = False
        self.mainloop("menu")

    # Define o método que controla o loop principal do jogo
    def mainloop(self, scene):
        self.scene = scene

        while scene != "quit":
            if scene == "menu":
                scene = self.menu()
            elif scene == "game":
                scene =  self.run_game()

    def menu(self):

        # Define referências de posições para os botões, ao centro da tela
        x_centered = st.WIDTH / 2
        y_centered = st.HEIGHT / 2

        # Instancia os botões do menu
        play_button = it.Button(text="PLAY", x=x_centered, y=y_centered-60, width=200, height=25)
        scores_button = it.Button(text="SCORES", x=x_centered, y=y_centered-30, width=200, height=25)
        intructions_button = it.Button(text="INSTRUCTIONS", x=x_centered, y=y_centered, width=200, height=25)
        exit_button = it.Button(text="EXIT", x=x_centered, y=y_centered+30, width=200, height=25)
        back_button = it.Button(text="BACK TO GAME", x=x_centered, y=y_centered+60, width=200, height=25)

        # # Lê os dados dos high scores a partir do arquivo ".save/scores.txt"
        # scores_filepath = os.path.join(st.save_folder, "scores.txt")
        # try:
        #     with open(scores_filepath, "r") as file:
        #         if file.read() != "":
        #             scores_data = json.load(file)
        #         else:
        #             scores_data = {}
        # except FileNotFoundError:
        #     scores_data = {"scores": []} # TODO: Conferir qual seria a fórmula de um arquivo vazio
        # sorted_scores = sorted(scores_data.items(), key=lambda x: x[1]["points"], reverse=True)

        # Inicia um loop para o menu
        while self.in_menu:
            # fnc()
            
            # Carrega a imagem de fundo do menu
            # screen.blit(menuBg, (0, 0))

            screen.fill(st.WHITE)

            # Desenha os botões na tela
            play_button.draw(screen, (0,0,0))
            scores_button.draw(screen, (0,0,0))
            intructions_button.draw(screen, (0,0,0))
            exit_button.draw(screen, (0,0,0))

            # Caso o usuário estava jogando, desenha o botão de voltar ao jogo
            if self.game_is_running:
                back_button.draw(screen, (0,0,0))

            # Verifica a ocorrência de eventos
            for event in pygame.event.get():
                # Recolhe a posição atual do mouse
                pos = pygame.mouse.get_pos()

                # Caso o usuário feche a janela
                if event.type == pygame.QUIT:
                    self.in_menu = False
                    self.quit_game()

                # Caso o usuário clique com o botão esquerdo do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Caso o usuário clique no botão de play
                    if play_button.is_over(pos):
                        return "game"
        
                    # Caso o usuário clique no botão de scores
                    elif scores_button.is_over(pos):
                        # changescn("scores")
                        print("scores")

                    # Caso o usuário clique no botão de instruções
                    elif intructions_button.is_over(pos):
                        # changescn("instructions")
                        print("instructions")
                    
                    # Caso o usuário clique no botão de sair
                    elif exit_button.is_over(pos):
                        self.in_menu = False
                        self.quit_game()
                        
                    # Caso o usuário clique no botão de voltar para o jogo (caso esteja jogando)
                    elif back_button.is_over(pos):
                        # changescn("mainLoop")
                        print("mainLoop")

                    else:
                        pass
                        
            # Atualiza os conteúdos da tela
            pygame.display.flip()

    # Crie um método para o encerramento do jogo
    def quit_game(self):
        """Encerra o jogo e o executável.
        

        Returns
        -------
        None.

        """
        pygame.quit()
        sys.exit()

##########################

# font_name = pygame.font.match_font("arial")

# draw_text(surface, text, size, x, y, color) -> GAME
# quit_game() -> GAME
# spawn_asteroids(asteroids_group,all_sprites_group) -> GAME
# spawn_enemy_ships(enemy_ships_group,all_sprites_group) -> GAME
# player_dies -> GAME