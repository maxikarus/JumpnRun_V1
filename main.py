import pygame
from pygame.locals import *
pygame.init()

# Farben und Schriftart
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)  # Standard-Schriftart, Größe 36

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

#Grafiken
background_img = pygame.image.load('image/background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Player():
    def __init__(self, x: int, y: int) -> None:
        img = pygame.image.load('image/Player1.png')
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if (keys[K_w] or keys[K_SPACE]) and self.jumped == False:
            self.vel_y = -screen_width / 30
            self.jumped = True
        if keys[K_w] or keys[K_SPACE] == False:     
            self.jumped = False
        if keys[K_a]:
            dx -= speed * delta_time
        if keys[K_s]:
            dy += speed * delta_time
        if keys[K_d]:
            dx += speed * delta_time


        #add gravity
        self.vel_y += 5
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        #check for collison

        #update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)
        

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
            screen.blit(tile[0], tile[1])

player = Player(100, screen_height-128)
world = World(world_data)

screen.blit(background_img, (0,0))
pygame.display.update()

run = True
while run:
    delta_time = clock.tick(FPS) / 1000

   # old_player_rect = player.copy()
    
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

    # screen.blit(background_img, old_player_rect, old_player_rect)
    # fps_rect = pygame.Rect(10, 10, fps_text.get_width(), fps_text.get_height())
    # screen.blit(background_img, fps_rect, fps_rect) 
    # world.draw()
    # player.update()
    # screen.blit(fps_text, (10, 10))
    # pygame.display.update([old_player_rect, player, pygame.Rect(10, 10, fps_text.get_width(), fps_text.get_height())])

    screen.blit(background_img, (0, 0))  # Hintergrund zeichnen
    world.draw()  # Welt zeichnen
    player.update()
    screen.blit(fps_text, (10, 10))  # FPS-Anzeige zeichnen
    pygame.display.flip()
pygame.quit()