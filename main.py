import pygame
from sys import exit

from modules import mapAndEnemies
from modules import levels
from modules import functions
from modules import menu
from modules import playerClass
from modules import bullet

# initialization
pygame.init()
screen = pygame.display.set_mode((1100, 600), flags=pygame.RESIZABLE)
pygame.display.set_caption("MarHess")
clock = pygame.time.Clock()

# (GAMES STATES: -2: init/intro; -1: menu;   0: game over;    1: game active)
game_state = -2

# text for the title
title_text = functions.title_text()
# text for the game over
game_over_text = functions.gameOver_text()

# player initialization
player = pygame.sprite.GroupSingle()

# moving map, this coordinate will synchronize every element on the same shift
x_map = 0

level = 0 # choosing the intro level and importing what's needed for this one
map_group, enemy_group, background_group, end_point = levels.import_level(level)
# level already finished (achieved_level[0] is intro)
achieved_level = [0,0,0,0]

# importing the sky image
sky_surface = pygame.transform.scale(pygame.image.load('graphics/sky.png').convert(), (1100, 600))

# menu
button_group, deco_menu = menu.Menu()




while True:
    # events loop
    keych = 0 # 2 if c and h are pressed -> cheat mode
    for event in pygame.event.get():
        # close window when asked
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #actions if a party is playing, for timers
        if game_state == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_c:
                    keych +=1 # if c is pressed
                if event.key == pygame.K_h:
                    keych+=1 # if h pressed
                if keych ==2:
                    player.sprite.cheat() # consequently if c and h are pressed
            # if the mouse is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # a mouse button is pressed
                if event.button == 1:
                    # it's the left one, we lunch a bullet !!
                    # bullets_group.add(bullet.Bullet(player.sprite, x_map))
                    pos = event.pos
                    theta = bullet.get_angle(pos, player.sprite.rect.center)
                    if -90 < theta <= 0:
                        projectile = bullet.Bullet(u, theta, screen, player.sprite, x_map)
                        bullet_group.add(projectile)
        # else if space is pressed, actions to start a new party
        elif event.type == pygame.KEYDOWN or game_state == -2:
            # presentation screen
            if game_state==-2:
                screen.fill('#3498db')
                title_text.draw(screen)
                pygame.display.update()
                pygame.time.wait(500)
            # if space key is pressed
            if game_state==-2 or event.key == pygame.K_SPACE:
                # adding a player object in the player group
                player.add(playerClass.Player())
                # creating groups based on the level asked
                map_group, enemy_group, background_group, end_point = levels.import_level(level)
                # puting game state to game active
                game_state = 1
                # initialization of physic and bullet
                radius = 250
                u = 50
                g = 9.8
                bullet_group = pygame.sprite.Group()
                theta = -30
                end = bullet.get_posOnCircumeference(theta, player.sprite.rect.center)
            # if escape key is pressed close the game
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # actions if a party is playing
    if game_state == 1:
        #pygame.mouse.set_visible(False)

        # Putting the sky
        screen.blit(sky_surface, (0, 0))

        # Background
        background_group.draw(screen)
        background_group.update(x_map)

        # Map
        map_group.draw(screen)
        map_group.update(x_map)

        # enemy
        end_point.draw(screen)
        end_point.update(x_map)

        # End Point
        enemy_group.draw(screen)
        enemy_group.update(x_map)

        # player
        player.draw(screen)
        # Updating the player, giving him the collision with the map, he return the shift of the map du to his movement and if he's dead
        collide_map = pygame.sprite.spritecollide(player.sprite, map_group, False)
        x_map, game_state = player.sprite.update(collide_map)
        # updating the collisions of the player with enemys, return if he died
        enemy_collide = pygame.sprite.spritecollide(player.sprite, enemy_group, False)
        if game_state == 1:
            game_state = player.sprite.colliding_enemy(enemy_collide)

        if game_state != 1:
            player.sprite.kill()
            map_group.empty()
            enemy_group.empty()
        elif pygame.sprite.spritecollide(player.sprite,end_point,False):
            player.sprite.kill()
            map_group.empty()
            enemy_group.empty()
            achieved_level[level] = 1
            game_state = -1
            level+=1

        #bullets
        bullet_group.update(x_map)

        #Detection of colision between two ennemies and diseapear both if it's True
        pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)

    elif game_state == 0:
        pygame.mouse.set_visible(True)
        game_over_text.draw(screen)

    elif game_state == -1:
        pygame.mouse.set_visible(True)
        #screen.fill('#1A18B8')  # blue background
        fond = pygame.image.load('graphics/MurBleuBon.jpeg').convert_alpha()
        fond = pygame.transform.scale(fond, (1640*0.671, 1024*0.59  ))
        fond = fond.convert()
        screen.blit(fond, (0, 0))

        deco_menu.draw(screen)
        title_text.draw(screen)
        output = None
        # updating the buttons and taking their outputs
        for button in button_group:
            if output == None or achieved_level[output-1] == 0:
                output = button.update(screen)
        # if a button is clicked, the output will be the level wanted by the player if the previous level is done
        if output != None and achieved_level[output-1] == 1:
            level = output
            # adding a player object in the player group
            player.add(playerClass.Player())
            # creating groups based on the level asked
            map_group, enemy_group, background_group, end_point = levels.import_level(level)
            # putting game state to game active
            game_state = 1



    # update the screen and set 60 frame per seconds
    pygame.display.flip()
    clock.tick(60)

