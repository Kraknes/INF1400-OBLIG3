import pygame
import random
import math
import config

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = random.uniform(0, config.SCREEN_X-self.size)
        self.rect.y = random.uniform(0, config.SCREEN_Y-self.size)
        
        
class Player_Object(Sprite):
    def __init__(self):
        self.size = 10
        self.colour = config.BLUE
        self.speed_y = 0
        self.speed_x = 0
        self.acc = 0
        super().__init__()
        
    def gravity(self):
        if self.speed_y < 5:
            self.speed_y += config.GRAVITY
        
    def acceleration(self):
        self.speed_y -= config.ACCELERATE
        
    def update(self):
        self.gravity()
        self.rect.y += self.speed_y
        
def create_objects(): 
    sprite_group = pygame.sprite.Group()
    sprite_group.add(Player_Object())
    return sprite_group
 
def update_screen(group):
    player_group  = group.sprites()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_SPACE]: 
        player_group[0].acceleration()


            
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                config.DONE = True
                
    screen.fill(config.BLACK)
    group.update()
    group.draw(screen)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(config.FPS)


pygame.init()
screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y))
pygame.display.set_caption("Erling's Mayhamorama")
clock = pygame.time.Clock()

sprite_group = create_objects()

if __name__ == "__main__":
    while not config.DONE:
        update_screen(sprite_group)