import pygame
import random
import math
import config
import time 

# lag bensinkanne for fuel påfyll, eller landingsplatform
# lag tekst for spiller, liv og fuel
# lag objekt som man kan kræsje i
# hvis en spiller kræsjer, mister man poeng

# Må ha minimum to filer - OK
# Må ha timing for andre datamaskiner - OK
# Dette må være med
    # The game shall be started using Python’s if name == ’ main ’:
    # idiom. Inside the if test, a single line shall instantiate the game ob-
    #ject. All other code, except the configuration constants, shall be inside
    #classes. This will simplify profiling and documentation generation
# Alle klasser skal arve pygame.sprite.Sprite. Alle objektene skal bli grupert med pygame.spirte.Group
# Alle klassene skal oppdateres med Group.update OG Group.draw(?)
# alle modulene, klassene og metodene skal ha docstrings. Masse text i obligfilen, les den
# I raport, diskutert design patterns.
# Profiler med cProfiler. Ta en screenshot av test og ha det i rapport, diskuter den. 

class Sprite(pygame.sprite.Sprite): # Alle objektene henter inn denne for å kunne konstruere Sprites
    def __init__(self):
        super().__init__()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect() 
        
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        

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
        self.rect.centerx = float(random.uniform(0, config.SCREEN_X-self.width))
        self.rect.centery = float(random.uniform(140, config.SCREEN_Y-self.height))
        self.health = 100
        self.fuel = 100
        self.score = 0

    
    class Bullet(Sprite):
        def __init__(self, angle, x, y):
            self.image = pygame.Surface([3, 3])
            self.image.fill(config.WHITE)
            self.angle = angle
            self.speed_y = -math.cos(math.radians(self.angle))
            self.speed_x = math.sin(math.radians(self.angle))  
            super().__init__()
            self.rect.centery = y + self.speed_y * 40
            self.rect.centerx = x + self.speed_x * 40

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
        textScore = fontScore.render(str(self.score), True, config.WHITE, None)
        textScoreRect = textScore.get_rect()
        
        healthText = font.render('Health: ' + str(self.health), True, config.BLUE, None)
        healthTextRect = text1.get_rect()
        
        fuelText = font.render('Fuel: ' + str(self.fuel), True, config.BLUE, None)
        fuelTextRect = text1.get_rect()
        
        if self.number == 1:
            # Score tekst
            textScoreRect.topleft = (340, 50)
            

            healthTextRect.topleft = (35,61)
            

            fuelTextRect.topleft = (35,101)
            
            
            # Visuell framvisning av liv og drivstoff
            pygame.draw.rect(screen, config.GREEN, pygame.Rect(30, 60, self.health*3, 30)) # Health bar
            pygame.draw.rect(screen, config.YELLOW, pygame.Rect(30, 100, self.fuel*3, 30)) # Fuel bar

        if self.number == 2:
            # Samme som ovenfor, bare for andre siden

            textScoreRect.topright = (config.SCREEN_X-340, 50)
            
            healthTextRect.topleft = (config.SCREEN_X - 330 ,61)
            

            fuelTextRect.topleft = (config.SCREEN_X - 330,101)
            
            pygame.draw.rect(screen, config.GREEN, pygame.Rect(config.SCREEN_X - 330, 60, self.health*3, 30))
            pygame.draw.rect(screen, config.YELLOW, pygame.Rect(config.SCREEN_X - 330, 100, self.fuel*3, 30))
            
        screen.blit(textScore, textScoreRect)
        screen.blit(healthText, healthTextRect)
        screen.blit(fuelText, fuelTextRect)
            
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
        self.screen_bars_update()
        self.bullet_list.update()
        self.bullet_list.draw(screen)
        self.rect.move_ip(round(self.speed_x),round(self.speed_y))
            
      
        
    def boundries(self):
        pass
        
def create_objects(): 
    bullet_group = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()
    sprite_group.add(Player_Object(config.T_IMAGE, 1)) # Spiller 1
    sprite_group.add(Player_Object(config.T_IMAGE, 2)) # Spiller 2
    return sprite_group, bullet_group

def reset_game(group):
    pygame.sprite.Group.empty(group)
    pygame.sprite.Group.empty(bullet_group)
    group.add(Player_Object(config.T_IMAGE,1))
    group.add(Player_Object(config.T_IMAGE,2))

    player_group  = group.sprites()
    player1 = player_group[0]
    player2 = player_group[1]
    return player1, player2

def play_game(group):
    player_group  = group.sprites()
    player1 = player_group[0]
    player2 = player_group[1]

    if player1.health == 0:
        player2.score += 1
        player1.health = 100
    if player2.health == 0:
        player1.score += 1
        player2.health = 100

    if player1.score == 3 or player2.score == 3:
        screen.fill(config.BLACK)
        font = pygame.font.Font('freesansbold.ttf', 100)
        if player1.score == 3:
            gameOver = font.render("PLAYER 1 WINS!", True, config.WHITE, None)
        else:
            gameOver = font.render("PLAYER 2 WINS!", True, config.WHITE, None)
        gameOverRect= gameOver.get_rect()
        gameOverRect.center = (config.SCREEN_X/2,config.SCREEN_Y/2)
        screen.blit(gameOver,gameOverRect)
        pygame.display.update()
        pygame.time.wait(5000)
        player1, player2 = reset_game(group)

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
            player1.shoot()
            
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
            player2.shoot()




            
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                config.DONE = True
            if event.key == pygame.K_r:
                player1, player2 = reset_game(group)
                
    screen.fill(config.BLACK)

    screen.blit(text1, textrect1)
    screen.blit(text2, textrect2)

    group.update()
    group.draw(screen)
    pygame.display.update()
    # pygame.display.flip()
    clock.tick(config.FPS)


pygame.init()
pygame.font.init()

# Dette e rotete, få dette ut. lag en funksjon i config.py
font = pygame.font.Font('freesansbold.ttf', 30)
fontScore = pygame.font.Font('freesansbold.ttf', 90)

text1 = font.render('Player1', True, config.WHITE, None)
textrect1 = text1.get_rect()
textrect1.topleft = (35,30)

text2 = font.render('Player2', True, config.WHITE, None)
textrect2 = text2.get_rect()
textrect2.topright = (config.SCREEN_X-35, 30)



screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y))


# til hit



pygame.display.set_caption("Erling's Mayhamorama")
clock = pygame.time.Clock()


sprite_group, bullet_group = create_objects()


if __name__ == "__main__":
    while not config.DONE:
        play_game(sprite_group)