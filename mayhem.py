import pygame
import random
import math
import config

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect() 



        
class Player_Object(Sprite):
    def __init__(self, image):
        self.image = image
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (10,10))
        super().__init__()
        self.speed_y = 0
        self.speed_x = 0
        self.acc_y = 0
        self.acc_x = 0
        self.bullet_list = pygame.sprite.Group()
        self.angle = 0
        self.original_image = self.image
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
            self.rect.centery = y + self.speed_y * 20
            self.rect.centerx = x + self.speed_x * 20

        def update(self):
            if self.rect.centerx < 0 or self.rect.centerx > config.SCREEN_X:
                self.kill()
            if self.rect.centery < 0 or self.rect.centery > config.SCREEN_Y:
                self.kill()
            pygame.sprite.spritecollide(self, sprite_group, False)
            self.rect.move_ip(round(self.speed_x * 10),round(self.speed_y * 10))
            
            
            
            
            
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
        self.gravity()
        self.bullet_list.update()
        self.bullet_list.draw(screen)
        self.rect.move_ip(round(self.speed_x),round(self.speed_y))
      
        
    def boundries(self):
        pass
        
def create_objects(): 
    sprite_group = pygame.sprite.Group()
    sprite_group.add(Player_Object(config.T_IMAGE))
    return sprite_group
 
def play_game(group):
    player_group  = group.sprites()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_r]:
        restart_group = create_objects()
        player_group = restart_group.sprites()
    if player_group:
        if player_group[0]:
            if keys[pygame.K_w]: 
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
                
    screen.fill(config.BLACK)
    group.update()
    group.draw(screen)
    pygame.display.update()
    # pygame.display.flip()
    clock.tick(config.FPS)


pygame.init()
screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y))
pygame.display.set_caption("Erling's Mayhamorama")
clock = pygame.time.Clock()


sprite_group = create_objects()

if __name__ == "__main__":
    while not config.DONE:
        play_game(sprite_group)