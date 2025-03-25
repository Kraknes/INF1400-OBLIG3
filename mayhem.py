import pygame
import random
import math
import config
import time 


class Sprite(pygame.sprite.Sprite): # Alle objektene henter inn denne for å kunne konstruere Sprites
    def __init__(self):
        super().__init__()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect() 

class Player_Object(Sprite): # Spiller klasse
    def __init__(self, image, player_number):
        self.number = player_number
        self.image = image
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (30,30))
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.original_image = self.image #brukes til rotering av sprite, unngår distortion av sprite bilde
        self.speed_y = 0
        self.speed_x = 0
        self.angle = 0
        self.bullet_list = pygame.sprite.Group()
        self.health = 100
        self.fuel = 100
        self.rect.centerx = float(random.uniform(0, config.SCREEN_X-self.width))
        self.rect.centery = float(random.uniform(0, config.SCREEN_Y-self.height))

    
    class Bullet(Sprite):
        def __init__(self, angle, x, y):
            self.image = pygame.Surface([3, 3])
            self.image.fill(config.WHITE)
            self.angle = angle
            self.speed_y = -math.cos(math.radians(self.angle))
            self.speed_x = math.sin(math.radians(self.angle))  
            super().__init__()
            self.rect.centery = y + self.speed_y * 30
            self.rect.centerx = x + self.speed_x * 30

        def update(self):
            # sletter seg selv når går ut av mappet
            if self.rect.centerx < 0 or self.rect.centerx > config.SCREEN_X:
                self.kill()
            if self.rect.centery < 0 or self.rect.centery > config.SCREEN_Y:
                self.kill()

            # henter sprites som blir truffet av skudd
            hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
            for sprite in hit_list:
                sprite.health -= 10
                print(sprite.health)
                self.kill()
            self.rect.move_ip(round(self.speed_x * 10),round(self.speed_y * 10))
            
    class Explosion(Sprite):
        def __init__(self, x, y, image):
            self.image = image
            self.image = pygame.image.load(self.image).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (30,30))

    def screen_bars_update(self):
        if self.number == 1:

            pygame.draw.rect(screen, config.GREEN, pygame.Rect(30, 60, self.health*3, 30)) # Health bar
            pygame.draw.rect(screen, config.YELLOW, pygame.Rect(30, 100, self.fuel*3, 30)) # Fuel bar
        if self.number == 2:
            pygame.draw.rect(screen, config.GREEN, pygame.Rect(config.SCREEN_X - 330, 60, self.health*3, 30))
            pygame.draw.rect(screen, config.YELLOW, pygame.Rect(config.SCREEN_X - 330, 100, self.fuel*3, 30))
        
            
    def shoot(self):
        bullet = self.Bullet(self.angle, self.rect.centerx, self.rect.centery)
        self.bullet_list.add(bullet)
        

    def rotateObject(self, value):
        self.angle += value
        self.angle = self.angle % 360
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(self.image, self.rect)
        print(self.angle)


    def gravity(self):
        if self.speed_y < 5:
            self.speed_y += config.GRAVITY
        
    def acceleration(self):
        self.speed_y += -math.cos(math.radians(self.angle))
        print("speed_y: " + str(self.speed_y))
        self.speed_x +=  math.sin(math.radians(self.angle))
        print("speed_x: " + str(self.speed_x))
        
    def update(self):
        # self.gravity()
        if self.fuel > 0:
            self.fuel -= 0.1
        self.screen_bars_update()
        self.bullet_list.update()
        self.bullet_list.draw(screen)
        self.rect.move_ip(round(self.speed_x),round(self.speed_y))
        if self.health == 0:
            self.kill()  # Må fikses
            
      
        
    def boundries(self):
        pass
        
def create_objects(): 
    bullet_group = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()
    sprite_group.add(Player_Object(config.T_IMAGE, 1)) # Spiller 1
    sprite_group.add(Player_Object(config.T_IMAGE, 2)) # Spiller 2
    return sprite_group, bullet_group
 
def play_game(group):
    player_group  = group.sprites()
    keys = pygame.key.get_pressed() 
    if player_group:
        if player_group[0]:
            if keys[pygame.K_w]: 
                if player_group[0].fuel != 0:
                    player_group[0].acceleration()
            if keys[pygame.K_d]:
                player_group[0].rotateObject(5)
            if keys[pygame.K_a]:
                player_group[0].rotateObject(-5)
            if keys[pygame.K_SPACE]:
                player_group[0].shoot()


            
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                config.DONE = True
            if event.key == pygame.K_r:
                pygame.sprite.Group.empty(group)
                group.add(Player_Object(config.T_IMAGE,1))
                group.add(Player_Object(config.T_IMAGE,2))
                
    screen.fill(config.BLACK)
    group.update()
    group.draw(screen)
    pygame.display.update()
    # pygame.display.flip()
    clock.tick(config.FPS)


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y))
pygame.display.set_caption("Erling's Mayhamorama")
clock = pygame.time.Clock()


sprite_group, bullet_group = create_objects()

if __name__ == "__main__":
    while not config.DONE:
        play_game(sprite_group)