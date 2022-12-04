# Importe as bibliotecas necessárias
import json
import math
import os
import pygame
import random
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

    # Crie um st.background
    st.background = pygame.image.load(os.path.join(st.img_folder, "space.jpg"))

    # Armazene a altura desse st.background
    st.background_height = st.background.get_height()

    # Som de st.background
    pygame.mixer.music.load(os.path.join(st.sound_folder, "som1.mp3"))
    pygame.mixer.music.set_volume(0.5)

    # Crie um grupo para todos os sprites
    st.all_sprites = pygame.sprite.Group()

    # Crie um grupo para os asteroides
    st.asteroids = pygame.sprite.Group()

    # Crie um grupo para as naves inimigas
    st.enemy_ships = pygame.sprite.Group()

    # Crie um grupo para as balas
    st.bullets = pygame.sprite.Group()

    # Crie um grupo para as balas dos inimigos
    st.enemies_bullets = pygame.sprite.Group()

    # Crie um grupo para os bônus
    st.powers = pygame.sprite.Group()
    
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

    # Crie um método para o menu principal
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

    def run_game(self):
        
        #Crie uma variável para o deslizamento da tela
        scrolling = 0
        
        #Crie uma variável para a quantidade de painés necessários no deslizamento da tela
        panels = math.ceil(st.HEIGHT/st.background_height)+2
        
        # Atribui a classe player a uma variável
        player = ge.Player()
        player.hitbox = ge.Hitbox(player)
        
        # Adiciona player aos grupo de sprites
        st.all_sprites.add(player, player.hitbox)
        
        # testButton = ge.Button(color=ge.WHITE, x=200, y=200, width=200, height=200, size=20, text="ABCASKLDASKLDNASD")
        
        #Cria uma marcação de tempo inicial para spawning
        start_asteroids = pygame.time.get_ticks()
        start_enemies_ships = pygame.time.get_ticks()
        
        #Reproduza a música de fundo infinitamente
        pygame.mixer.music.play(loops=-1)
        
        #Estabeleça o nível antes do jogo iniciar
        level = 1
        
        start_level_time = pygame.time.get_ticks()
        
        # Loop para o jogo
        running = True
        
        while running:
            
            # Faça o jogo funcionar com a quantidade de frames por segundo estabelecidas
            clock.tick(st.FPS)
            
            #Recebe a quantidade de tempo decorrida desde o início do jogo
            level_delay = pygame.time.get_ticks()
            
            #Adicione um nível de 5 em 5 segundos
            if level_delay - start_level_time   > 5000:
                start_level_time = pygame.time.get_ticks()
                level += 1
            
            
            # Faça o jogo reagir a eventos externos
            for event in pygame.event.get():
                # Permita que o usuário saia do jogo
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # running = False
                        # mso.quit_game()
                        self.pause = self.paused()

            # Atualiza os sprites
            st.all_sprites.update()
            
            
            # Gera bônus aleatoriamente na tela
            if random.random() < 0.005:
                power = ge.Power()
                st.powers.add(power)
                st.all_sprites.add(power)

                
            #Spawna asteroides em intervalos de 3 ou menos segundos (dependendo do nível)
            now = pygame.time.get_ticks()
            if now - start_asteroids > (3000 - 10*level) :
                start_asteroids = now
                self.spawn_asteroids(st.asteroids,st.all_sprites)
        
            #spawna naves inimigas em intervalos de 4 ou menos segundos
            if now - start_enemies_ships > (4000 - 5*level):
                start_enemies_ships = now
                self.spawn_enemy_ships(st.enemy_ships,st.all_sprites)

            #Cria casos de colisão entre balas do jogador e asteroides
            bullet_hits_asteroid = pygame.sprite.groupcollide(st.asteroids, st.bullets, True, True)
            for hitted_asteroid in bullet_hits_asteroid:
                asteroid_score = hitted_asteroid.get_score()
                player_old_score = player.get_score()
                player.set_score(player_old_score+asteroid_score) 
                
                #Exibe explosão
                explosion = ge.Explosion(hitted_asteroid.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                # Adiciona um novo asteroide à tela
                new_asteroid = ge.Asteroid()
                st.all_sprites.add(new_asteroid)
                st.asteroids.add(new_asteroid)
                
            #Cria casos de colisão entre balas do jogador e naves inimigas    
            bullet_hits_enemy_ship = pygame.sprite.groupcollide(st.enemy_ships,st.bullets, True, True)
            for hitted_enemy_ship in bullet_hits_enemy_ship:
                enemy_score = hitted_enemy_ship.get_score()
                player_old_score = player.get_score()
                player.set_score(player_old_score+enemy_score) 
                
                #Exibe explosão
                explosion = ge.Explosion(hitted_enemy_ship.rect.center,"small")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
            #Cria casos de colisão entre jogador e asteroides    
            asteroid_hits_player = pygame.sprite.spritecollide(
                player.hitbox, st.asteroids, True, pygame.sprite.collide_circle)
            if asteroid_hits_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.get_life()
                damage = 1
                player.set_life(life - damage)
                if player.get_life() <= 0:
                    running =  self.player_dies(running) 
                
            #Cria casos de colisão entre balas do inimigo e o jogador    
            enemy_shoots_player = pygame.sprite.spritecollide(
                player.hitbox, st.enemies_bullets, True, pygame.sprite.collide_circle)
            if enemy_shoots_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.get_life()
                damage = 1
                player.set_life(life - damage)
                if player.get_life() <= 0:
                    running = self.player_dies(running)  
                
            #Cria casos de colisão entre nave inimiga e o jogador    
            enemy_hits_player = pygame.sprite.spritecollide(
                player.hitbox, st.enemy_ships, False, pygame.sprite.collide_circle)
            if enemy_hits_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.get_life()
                damage = 1
                player.set_life(life - damage)
                if player.get_life() <= 0:
                    running =  self.player_dies(running) 
                
            
            #Cria casos de colisão entre bônus e o jogador
            player_hits_bonus = pygame.sprite.spritecollide(player.hitbox, st.powers, True, pygame.sprite.collide_circle)
            
            for hitted_bonus in player_hits_bonus:
                #Caso seja um escudo, adicione vidas ao a jogador
                if hitted_bonus.type == "shield":
                    initial_lifes = player.get_life()
                    player.set_life(initial_lifes + 1)
                #Caso seja uma arma, adicione uma arma mais poderosa ao jogador
                if hitted_bonus.type == "gun":
                    player.gain_powerup()
               

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(True)
            elif not keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(False)


            # Defina a imagem de fundo da tela
            screen.fill((0, 0, 0))

            #Mova o st.background
            for i in range(panels):
                screen.blit(st.background,(0,i*st.background_height+scrolling-st.background_height))
            
            scrolling += 5
            
            if abs(scrolling)>st.background_height:
                scrolling = 0
            

            # Desenha os sprites na tela
            st.all_sprites.draw(screen)

            # Insere o score na tela

            #Adiciona a pontuação no topo da tela
            self.draw_text(screen, f"Score: {str(player.get_score())}", 40, st.WIDTH/2, 10,(255,255,255))
            
            #Adiciona os escudos no cando superior direito da tela
            self.draw_text(screen, f"Shields: {str(player.get_life()-1)}", 20, st.WIDTH * (7/8), 10,(255,255,255))
            
            # Atualize as imagens dos objetos quando ocorrerem mudanças
            pygame.display.flip()
            
            # Atualiza o jogo
            pygame.display.update()
        
        self.quit_game()


    def paused(self):
        self.pause = True

        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    
            screen.fill(st.WHITE)

            pygame.display.update()
            clock.tick(st.FPS)

    def game_over(self, score):
        self.over = True

        # Define referências de posições para os botões, ao centro da tela
        x_centered = st.WIDTH / 2
        y_centered = st.HEIGHT / 2

        player_name_box = it.InputTextBox(x_centered, y_centered, 200, max_input_length=20)
        ok_button = it.Button(text="Salvar score", x=x_centered, y=y_centered+50, width=200, height=25)

        while self.over:

            screen.fill(st.WHITE)

            # Imprime uma mensagem de "Game Over" na tela
            self.draw_text(screen, "GAME OVER", 100, x_centered, y_centered - 250, st.BLACK)
            # Imprime a pontuação do jogador na tela
            self.draw_text(screen, f"Score: {str(score)}", 50, x_centered, y_centered - 100, st.BLACK)

            # Imprime um rótulo para a caixa de nome do usuário
            self.draw_text(screen, "Digite seu nome:", 30, x_centered, y_centered - 50, st.BLACK)

            player_name_box.update()
            player_name_box.draw(screen)

            ok_button.draw(screen, (0,0,0))

            for event in pygame.event.get():

                player_name_box.handle_event(event)

                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_RETURN:
                        self.over = False
                        return False

            pygame.display.update()
            clock.tick(st.FPS)

    # Crie uma função para a dispersão de asteroides
    def spawn_asteroids(self, asteroids_group,all_sprites_group):
        """Recebe um grupo para os sprites de asteroides e um para todos os sprites 
        e adiciona asteroides a esses grupos.  
        

        Parameters
        ----------
        asteroids_group : pygame.sprite.Group()
            Grupo com os sprites de asteroides.
        all_sprites_group : pygame.sprite.Group()
            Grupo com todos os sprites .

        Returns
        -------
        None.

        """
        asteroid = ge.Asteroid()
        asteroids_group.add(asteroid)
        all_sprites_group.add(asteroid)

    #Crie uma função para dispersão de naves inimigas    
    def spawn_enemy_ships(self, enemy_ships_group,all_sprites_group):
        """Recebe um grupo para os sprites de naves inimigas e um para todos os sprites 
        e adiciona naves inimigas a esses grupos.  
        

        Parameters
        ----------
        enemy_ships_group : pygame.sprite.Group()
            Grupo com os sprites de naves inimigas.
        all_sprites_group : pygame.sprite.Group()
            Grupo com todos os sprites .

        Returns
        -------
        None.

        """
        
        enemy = ge.Enemy_ship()
        enemy.enemy_shoots()
        enemy_ships_group.add(enemy)
        all_sprites_group.add(enemy)
        enemy.update()

    #Crie uma função para a morte do jogador
    def player_dies(self, loop):
        """Recebe o loop do jogo e o encerra.
        

        Parameters
        ----------
        loop : boll
            Loop do jogo.

        Returns
        -------
        loop : boll
            Loop do jogo, agora sendo "Falso".

        """
        loop = False
        return loop

    # Crie um método para o encerramento do jogo
    def quit_game(self):
        """Encerra o jogo e o executável.
        

        Returns
        -------
        None.

        """
        pygame.quit()
        sys.exit()


    #Inicia o pygame
    # pygame.init()

    # font_name =pygame.font.SysFont("arcade", 20)
    # font_name = pygame.font.Font("./src/fonts/DigitalDisco.ttf", 20)

    # Crie uma função para exibição de texto
    def draw_text(self, surface, text, size, x, y, color):
        """Exibe um texto em uma superfície, o conteúdo do texto, tamanho, cor, posição e 
        a superfície são dados como parâmetro.
        

        Parameters
        ----------
        surface : pygame.sprite.Sprite
            Superfície onde será exibido o texto.
        text : str
            Conteúdo do texto.
        size : int
            Tamanho do texto.
        x : int
            Posição do texto no eixo x.
        y : int
            Posição do texto no eixo y.
        color : tuple
            Cor do texto.

        Returns
        -------
        None.

        """
        
        # Crie uma variável para a fonte utilizada
        font_name = pygame.font.match_font("arial")

        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

##########################

# font_name = pygame.font.match_font("arial")

# draw_text(surface, text, size, x, y, color) -> GAME
# quit_game() -> GAME
# spawn_asteroids(asteroids_group,all_sprites_group) -> GAME
# spawn_enemy_ships(enemy_ships_group,all_sprites_group) -> GAME
# player_dies -> GAME