import pygame
from pygame.locals import *
pygame.init()
main_menu = True
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

#Grafiken
background_imgs = []
for i in range (1,6):
    background_img = pygame.image.load(f'image/plx-{i}.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    background_imgs.append(background_img)
background_width = background_imgs[0].get_width()

scroll = 0


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

class Player():
    def __init__(self, x: int, y: int) -> None:
        img = pygame.image.load('image/Player1.png')
        self.image = pygame.transform.scale(img, (48, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.onGround = False

    def update(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if (keys[K_w] or keys[K_SPACE]) and self.jumped == False and self.onGround == True:
            self.vel_y = -screen_width / 30
            self.jumped = True
            self.onGround = False
        if (keys[K_w] or keys[K_SPACE]) == False:     
            self.jumped = False
        if keys[K_a] and scroll >= 0:
            dx -= speed * delta_time
        if keys[K_s]:
            dy += speed * delta_time
        if keys[K_d] and scroll < 3000:
            dx += speed * delta_time


        #add gravity
        self.vel_y += 5
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collison
        for tile in world.tile_list:
            #check in x
            if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
                if dx > 0:  # Moving right
                    dx = tile[1].left - self.rect.right
                elif dx < 0:  # Moving left
                    dx = tile[1].right - self.rect.left
            #check in y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below block
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.onGround = True

        #update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        

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
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Button():
	def __init__(self, image, x_pos, y_pos, text_input):
		self.image = image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_input = text_input
		self.text = font.render(self.text_input, True, "white")
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self):
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = font.render(self.text_input, True, "white")
		else:
			self.text = font.render(self.text_input, True, "#0a4635")   

def draw_background():
    for x in range(5):
        bg_speed = 0.2
        for i in background_imgs:
            screen.blit(i, ((x*background_width) - scroll * bg_speed, 0))
            bg_speed += 0.1

player = Player(100, screen_height-128)
world = World(world_data)


#screen.blit(background_img, (0,0))
pygame.display.update()

while main_menu:
    draw_background()
    mouse_pos = pygame.mouse.get_pos()

    menu_text = font2.render("Julia's game", True, white)
    menu_rect = menu_text.get_rect(center=(640, 100))

    play_button = Button(pygame.image.load("image/main_button.png"), 640, 330, "PLAY")
    quit_button = Button(pygame.image.load("image/main_button.png"), 640, 380, "QUIT")

    for button in [play_button, quit_button]:
        button.changeColor(mouse_pos)
        button.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.checkForInput(mouse_pos):
                main_menu = False
                play = True
            if quit_button.checkForInput(mouse_pos):
                main_menu = False

    screen.blit(menu_text, menu_rect)

    pygame.display.flip()



while play:
    delta_time = clock.tick(FPS) / 1000

   # old_player_rect = player.copy()
    
    #Eventhandler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused


    #FPS-Counter
    fps_timer += delta_time
    if fps_timer >= 1.0:  # Aktualisiere die FPS-Anzeige jede Sekunde
        curr_fps = clock.get_fps()
        fps_timer = 0
    fps_text = font.render(f"FPS: {int(curr_fps)}", True, white)

    # screen.blit(background_img, old_player_rect, old_player_rect)dw
    # fps_rect = pygame.Rect(10, 10, fps_text.get_width(), fps_text.get_height())
    # screen.blit(background_img, fps_rect, fps_rect) 
    # world.draw()
    # player.update()
    # screen.blit(fps_text, (10, 10))
    # pygame.display.update([old_player_rect, player, pygame.Rect(10, 10, fps_text.get_width(), fps_text.get_height())])

    if not paused:
        #screen.blit(background_img, (0, 0))  # Hintergrund zeichnen
        draw_background()
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and scroll > -5:
            scroll -= 5
        if key[pygame.K_d] and scroll < 3000:
            scroll += 5
        world.draw()  # Welt zeichnen
        player.update()
        screen.blit(fps_text, (10, 10))  # FPS-Anzeige zeichnen

    if paused:
        screen.blit(pause_text, (530, 200))
        #screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
pygame.quit()