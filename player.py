import pygame
from pygame.locals import *
#from main import *

speed = 400
scroll = 0

class Player():

    def __init__(self, x: int, y: int, dx=0, dy=0) -> None:
        img = pygame.image.load('image/Player1.png')
        self.image = pygame.transform.scale(img, (48, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.onGround = False

    def move(self, key, world, screen, delta_time):
        self.dx = 0
        self.dy = 0

        if (key[K_w] or key[K_SPACE]) and self.jumped == False and self.onGround == True:
            self.vel_y = -screen.get_width() / 30
            self.jumped = True
            self.onGround = False
        if (key[K_w] or key[K_SPACE]) == False:     
            self.jumped = False
        if key[K_a] and scroll >= 0:
            self.dx -= speed * delta_time
            #scroll -= 5
        if key[K_s]:
            self.dy += speed * delta_time
        if key[K_d] and scroll < 3000:
            self.dx += speed * delta_time
            #scroll += 5

    def move_left(self, delta_time, world):
        self.dx -= speed * delta_time
        #self.collisiontest(world)

    def move_right(self, delta_time, world):
        self.dx += speed * delta_time  
        #self.collisiontest(world)
 
    def jump(self, screen, world):
        self.vel_y = -screen.get_width() / 30
        self.jumped = True
        self.onGround = False
        self.collisiontest(world)
        
    def move_down(self, world, delta_time):
        self.dy += speed * delta_time
        self.collisiontest(world)
        #print(self.dy)

        #add gravity
        

        #check for collison
    def collisiontest(self, world):
        collision = False
        self.onGround = False
        for tile in world.tile_list:
            #check in x
            if tile[1].colliderect(self.rect.x +self.dx, self.rect.y, self.width, self.height):
                if self.dx > 0:  # Moving right
                    self.dx = tile[1].left - self.rect.right
                elif self.dx < 0:  # Moving left
                    self.dx = tile[1].right - self.rect.left
                collision = True
            #check in y
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
            #check if below block
                if self.vel_y < 0:
                    self.dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.onGround = True
                collision = True
        return collision
        
    def update(self, world, screen):
        #update player position
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.dx = 0

        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.dy = 0

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)