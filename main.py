import pygame
from pygame.locals import *
from buttons import *
from player import *

pygame.init()
loop = True
main_menu = True
option_menu = False
play = False
paused = False

# Farben und Schriftart
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)  # Standard-Schriftart, Größe 36
font2 = pygame.font.Font(None, 100)  # Standard-Schriftart, Größe 100

pause_text = font2.render("Pause", True, "white")

#Fenster 
screen_width = 1280 #20 tiles
screen_height = 704 #11 tiles
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Julia und Max')

# Spielgeschwindigkeit
clock = pygame.time.Clock()
FPS = 120

#FPS-Anzeige
fps_timer = 0
curr_fps = 0
delta_time = 0
speed = 400
camera_offset = [0, 0]

#Grafiken
background_imgs = []
for i in range (1,6):
    background_img = pygame.image.load(f'image/plx-{i}.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    background_imgs.append(background_img)
background_width = background_imgs[0].get_width()

#background_img = pygame.image.load('image/background.png')

#World
tile_size = screen_width / 20
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
        
class World():
    def __init__(self, data) -> None:
        self.tile_list = []
        self.tile_size = tile_size
        
        #load images
        grass_img = pygame.image.load('image/grass_block.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1
    
    def draw(self) -> None:
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - camera_offset[0], tile[1].y))
            pygame.draw.rect(screen, (255, 255, 255), 
                             (tile[1].x - camera_offset[0], tile[1].y - camera_offset[1],
                             tile[1].width, tile[1].height), 2)

def draw_background():
    num_tiles = int(screen_width / background_width) + 2
    bg_speed = 30
    for i, img in enumerate(background_imgs):
        speed = 0.1 + i/bg_speed
        offset_x = int(camera_offset[0] * speed) % int(background_width)
        for y in range(-1, num_tiles):
            screen.blit(img, (int(y * background_width - offset_x), 0))

player = Player(100, screen_height-128)
world = World(world_data)
world_width = len(world_data[0])
world_height = len(world_data)


#screen.blit(background_img, (0,0))
pygame.display.update()
while loop:
    while main_menu:
        draw_background()
        mouse_pos = pygame.mouse.get_pos()

        menu_text = font2.render("Julia's game", True, white)
        menu_rect = menu_text.get_rect(center=(screen_width/2, (screen_height/10)*1))

        play_button = Button(pygame.image.load("image/main_button.png"), screen_width/2, (screen_height/10)*4, "PLAY", font)
        option_button = Button(pygame.image.load("image/main_button.png"), screen_width/2, (screen_height/10)*5, "OPTIONS", font)
        quit_button = Button(pygame.image.load("image/main_button.png"), screen_width/2, (screen_height/10)*6, "QUIT", font)

        for button in [play_button, option_button, quit_button]:
            button.changeColor(mouse_pos, font)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    main_menu = False
                    play = True
                if option_button.checkForInput(mouse_pos):
                    main_menu = False
                    play = False
                    option_menu = True
                if quit_button.checkForInput(mouse_pos):
                    main_menu = False
                    loop = False

        screen.blit(menu_text, menu_rect)

        pygame.display.flip()

    while option_menu:
        draw_background()

        mouse_pos = pygame.mouse.get_pos()

        menu_text = font2.render("Julia's game", True, white)
        menu_rect = menu_text.get_rect(center=(screen_width/2, (screen_height/10)*1))

        menu_button = Button(pygame.image.load("image/main_button.png"), screen_width/2, (screen_height/10)*7, "MENU", font)
        quit_button = Button(pygame.image.load("image/main_button.png"), screen_width/2, (screen_height/10)*8, "QUIT", font)

        for button in [menu_button, quit_button]:
            button.changeColor(mouse_pos, font)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mouse_pos):
                    main_menu = True
                    play = False
                    option_menu = False
                if quit_button.checkForInput(mouse_pos):
                    loop = False
                    main_menu = False
                    option_menu = False
    
        pygame.display.flip()

    while play:
        delta_time = clock.tick(FPS) / 1000
        # Kamera folgt dem Spieler (zentriert ihn)
        camera_offset[0] += (player.rect.x - screen_width / 2 - camera_offset[0]) / 20
        camera_offset[1] = 0
        # Begrenze die Kamera auf die Weltgrenzen
        #camera_offset[0] = max(0, min(camera_offset[0], world_width * tile_size - screen_width))
        #camera_offset[1] = max(0, min(camera_offset[1], screen_height - player.height))
    
        #Eventhandler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused


        #FPS-Counter
        fps_timer += delta_time
        if fps_timer >= 1.0:  # Aktualisiere die FPS-Anzeige jede Sekunde
            curr_fps = clock.get_fps()
            fps_timer = 0
        fps_text = font.render(f"FPS: {int(curr_fps)}", True, white)

        if not paused:
            #screen.blit(background_img, (0, 0))  # Hintergrund zeichnen
            draw_background()
            key = pygame.key.get_pressed()
            player.dx = 0
            player.dy = 0
            if ((key[K_w] or key[K_SPACE]) and player.jumped == False and player.onGround == True):
                #print("jump")
                player.jump(screen, world)
            elif (key[K_w] or key[K_SPACE]) == False:     
                player.jumped = False
            if key[pygame.K_a] and scroll > -1:
                player.move_left(delta_time, world)
                if(player.collisiontest(world)==False):
                    scroll -= 5
            elif key[pygame.K_d] and scroll < 3000:
                player.move_right(delta_time, world)
                if(player.collisiontest(world)==False):
                    scroll += 5
            elif key[pygame.K_s]:
                player.move_down(world, delta_time)
            world.draw()  # Welt zeichnen
            player.update(world, screen, camera_offset)  # Spieler aktualisieren
            screen.blit(fps_text, (10, 10))  # FPS-Anzeige zeichnen

        if paused:
            screen.blit(pause_text, (530, 200))
            #screen.blit(fps_text, (10, 10))
    
        pygame.display.flip()
    
pygame.quit()