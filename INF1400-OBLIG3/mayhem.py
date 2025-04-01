import pygame
import random
import math
import config
import text_file
import pg_init
import time 

# lag bensinkanne for fuel påfyll, eller landingsplatform
# lag tekst for spiller, liv og fuel - OK
# lag objekt som man kan kræsje i - OK
# lag vegger 
# hvis en spiller kræsjer, mister man poeng - OK

# Må ha minimum to filer - OK
# Må ha timing for andre datamaskiner - OK
# Dette må være med
    # The game shall be started using Python’s if name == ’ main ’:
    # idiom. Inside the if test, a single line shall instantiate the game ob-
    #ject. All other code, except the configuration constants, shall be inside
    #classes. This will simplify profiling and documentation generation
# Alle klasser skal arve pygame.sprite.Sprite. Alle objektene skal bli grupert med pygame.spirte.Group - OK
# Alle klassene skal oppdateres med Group.update OG Group.draw(?) - OK
# alle modulene, klassene og metodene skal ha docstrings. Masse text i obligfilen, les den
# I raport, diskutert design patterns.
# Profiler med cProfiler. Ta en screenshot av test og ha det i rapport, diskuter den. 

class Sprite(pygame.sprite.Sprite): # Alle objektene henter inn denne for å kunne konstruere Sprites
    def __init__(self, image, image_size):
        super().__init__()
        self.image = image
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (image_size,image_size))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect() 
        
class Obstacle(Sprite):
    def __init__(self, image, image_size):
        super().__init__(image, image_size)
        self.original_image = self.image
        self.rect.centerx = float(random.uniform(400, config.SCREEN_X-400))
        self.rect.centery = float(random.uniform(400, config.SCREEN_Y-400))
        self.start_y = self.rect.centery
        self.angle = 0
        
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(self.image, self.rect)
        
    def update(self):
        self.angle += 1
        self.rotate()
        
class Fuel(Sprite):
    def __init__(self, image, image_size):
        super().__init__(image, image_size)
        self.original_image = self.image
        self.rect.centerx = float(random.uniform(400, config.SCREEN_X-400))
        self.rect.centery = float(random.uniform(400, config.SCREEN_Y-400))

class Player_Object(Sprite): # Spiller klasse
    def __init__(self, player_number, image, image_size):
        super().__init__(image, image_size)
        self.number = player_number
        self.original_image = self.image # Brukes til rotering av sprite, unngår distortion av sprite bilde
        self.score = 0
        self.resetAll()

    def resetAll(self):  
        if self.number == 1: # Start lokasjon på skjerm
            self.rect.centerx = 300
            self.rect.centery = config.SCREEN_Y / 2
        else: 
            self.rect.centerx = config.SCREEN_X - 300
            self.rect.centery = config.SCREEN_Y / 2
        self.speed_x = 0
        self.speed_y = 0
        self.angle = 0
        self.fuel = 100
        self.health = 100
            
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, angle, x, y):
            super().__init__()
            self.image = pygame.Surface([3, 3])
            self.image.fill(config.WHITE)
            self.rect = self.image.get_rect()
            self.angle = angle
            self.speed_y = -math.cos(math.radians(self.angle))
            self.speed_x = math.sin(math.radians(self.angle))  
            self.rect.centery = y + self.speed_y * 40
            self.rect.centerx = x + self.speed_x * 40
            
        def hitPlayer(self, group):
            hit_list = pygame.sprite.spritecollide(self, group, False)
            for sprite in hit_list:
                if isinstance(sprite, Player_Object):
                    sprite.health -= 10
                self.kill()
    
        def outOfBounds(self):
            if self.rect.centerx < 0 or self.rect.centerx > config.SCREEN_X:
                self.kill()
            if self.rect.centery < 0 or self.rect.centery > config.SCREEN_Y:
                self.kill()    

        def update(self, group):
            # sletter seg selv når går ut av mappet
            self.outOfBounds()
            # henter sprites som blir truffet av skudd
            self.hitPlayer(group)
            self.rect.move_ip(round(self.speed_x * 10),round(self.speed_y * 10))

    def screen_bars_update(self): ## Dette kan gå inni text_file
        text_file.showTextAndBar(self.number, self.score, self.health, self.fuel)
            
    def shoot(self):
        bullet = self.Bullet(self.angle, self.rect.centerx, self.rect.centery)
        return bullet # returneres for class Game controll
        

    def rotateObject(self, value):
        self.angle += value
        self.angle = self.angle % 360
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(self.image, self.rect)


    def gravity(self):
        if self.speed_y < 5:
            self.speed_y += config.GRAVITY
        
    def acceleration(self):
        self.speed_y += -math.cos(math.radians(self.angle))
        self.speed_x +=  math.sin(math.radians(self.angle))
            
    def hitObject(self, group): # denne e litt rar siden du gjør ting til en anna class
        hit_list = pygame.sprite.spritecollide(self, group, False)
        for object in hit_list:
            if object != self:
                if isinstance(object, Obstacle):
                    self.health = 0
                if isinstance(object, Fuel):
                    self.fuel = 100
                    object.kill()
                    group.add(Fuel(config.F_IMAGE, 50))

            
    def update(self):
        # self.gravity()
        self.screen_bars_update()
        self.rect.move_ip(round(self.speed_x),round(self.speed_y))
        
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.sprite_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.fuel_group = pygame.sprite.Group()
        self.sprite_group.add(Player_Object(1, config.T_IMAGE, 30)) # Spiller 1
        self.sprite_group.add(Player_Object(2, config.T_IMAGE, 30)) # Spiller 2
        self.player_group = self.sprite_group.sprites()
        self.sprite_group.add(Obstacle(config.O_IMAGE, 100))
        self.sprite_group.add(Fuel(config.F_IMAGE, 50))
        

    def key_inputs(self, player1, player2):
        keys = pygame.key.get_pressed() 
        if player1:
            if keys[pygame.K_w]: 
                if player1.fuel > 0:
                    player1.fuel -= 0.5
                    player1.acceleration()
            if keys[pygame.K_d]:
                player1.rotateObject(5)
            if keys[pygame.K_a]:
                player1.rotateObject(-5)
            if keys[pygame.K_SPACE]:
                self.bullet_group.add(player1.shoot())      
        if player2:
            if keys[pygame.K_UP]: 
                if player2.fuel > 0:
                    player2.fuel -= 0.5
                    player2.acceleration()
            if keys[pygame.K_RIGHT]:
                player2.rotateObject(5)
            if keys[pygame.K_LEFT]:
                player2.rotateObject(-5)
            if keys[pygame.K_DOWN]:
                self.bullet_group.add(player2.shoot())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    config.DONE = True
                if event.key == pygame.K_r:
                    self.resetGame()
                    
    def winnerWinnerChickenDinner(self, player1, player2):
        if player1.score == 3 or player2.score == 3:
            pg_init.screen.fill(config.BLACK)
            font = pygame.font.Font('freesansbold.ttf', 100)
            if player1.score == 3:
                gameOver = font.render("PLAYER 1 WINS!", True, config.WHITE, None)
            else:
                gameOver = font.render("PLAYER 2 WINS!", True, config.WHITE, None)
            gameOverRect= gameOver.get_rect()
            gameOverRect.center = (config.SCREEN_X/2,config.SCREEN_Y/2)
            pg_init.screen.blit(gameOver, gameOverRect)
            pygame.display.update()
            pygame.time.wait(3000)
            self.resetGame()

    def resetGame(self):
        pygame.sprite.Group.empty(self.sprite_group)
        pygame.sprite.Group.empty(self.bullet_group)
        self.sprite_group.add(Player_Object(1, config.T_IMAGE, 30)) # Spiller 1
        self.sprite_group.add(Player_Object(2, config.T_IMAGE, 30)) # Spiller 2
        self.sprite_group.add(Obstacle(config.O_IMAGE, 100))
        self.sprite_group.add(Fuel(config.F_IMAGE, 50))
        self.player_group = self.sprite_group.sprites()

    def play_game(self):
        while not config.DONE:
            player1 = self.player_group[0]
            player2 = self.player_group[1]

            if player1.health <= 0:
                player2.score += 1
                player1.resetAll()
            if player2.health <= 0:
                player1.score += 1
                player2.resetAll()


            self.winnerWinnerChickenDinner(player1, player2)
            self.key_inputs(player1,player2)
            
            # text for spillere

            pg_init.screen.fill(config.BLACK)
            
            self.sprite_group.update()
            self.bullet_group.update(self.sprite_group) 
            for player in self.player_group:
                if isinstance(player, Player_Object):
                    player.hitObject(self.sprite_group)
            
            self.bullet_group.draw(pg_init.screen)
            self.sprite_group.draw(pg_init.screen)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(config.FPS)


if __name__ == "__main__":
    Game().play_game()