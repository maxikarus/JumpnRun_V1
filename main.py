import pygame
from pygame.locals import *
pygame.init()

# Farben und Schriftart
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)  # Standard-Schriftart, Größe 36

#halloooooo

#Fenster 
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Julia und Max')

# Spielgeschwindigkeit
clock = pygame.time.Clock()
FPS = 120

#FPS-Anzeige
fps_timer = 0
curr_fps = 0

#Grafiken
player_img = pygame.image.load('image/Player1.png')
player_img = pygame.transform.scale(player_img, (100, 100))  # Breite und Höhe anpassen
background_img = pygame.image.load('image/background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

#Player
player = pygame.Rect((300, 250, 100, 100))
delta_time = 0
speed = 400

screen.blit(background_img, (0,0))
pygame.display.update()

run = True
while run:
    delta_time = clock.tick(FPS) / 1000

    #Steuerung
    old_player_rect = player.copy()
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player.move_ip(0, -speed * delta_time)
    if keys[K_a]:
        player.move_ip(-speed * delta_time, 0)
    if keys[K_s]:
        player.move_ip(0, speed * delta_time)
    if keys[K_d]:
        player.move_ip(speed * delta_time, 0)

    #Eventhandler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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
            player.move(key, world, screen, delta_time)
            if (key[K_w] or key[K_SPACE]):
                player.move(key, world, screen, delta_time)
            if key[pygame.K_a] and scroll > -5:
                scroll -= 5
                #player.move(key, world, screen, delta_time)
            if key[pygame.K_d] and scroll < 3000:
                scroll += 5
                #player.move(key, world, screen, delta_time)
            if key[pygame.K_s]:
                player.move(key, world, screen, delta_time)
            world.draw()  # Welt zeichnen
            player.update(screen)
            screen.blit(fps_text, (10, 10))  # FPS-Anzeige zeichnen

        if paused:
            screen.blit(pause_text, (530, 200))
            #screen.blit(fps_text, (10, 10))
    
        pygame.display.flip()
    
pygame.quit()

#tetststetetete