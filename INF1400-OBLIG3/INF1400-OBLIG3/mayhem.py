""" 
INF-1400
ASSIGMENT 3
By Erling Heimstad Willassen
EWI012
Made on: 25.04.2025

Two-player game clone inspired by the game Mayhem. 
Two players fight against each other by shooting each other down.
First to three points wins the game. 
Fuel cannister can be touched to gain more fuel for movement.
Black holes are obstacles that will instantly kill the player. 
Boundaries make player bounce and lose health. 
If player has no fuel left, touching the lower boundary will make the player die. 

Player 1 keys:
W - Move up
A - Rotate left
D - Rotate right
Space - Shoot

Player 2 keys:
Arrow Up - Move up
Arrow Left - Rotate left
Arrow Right - Rotate right
Arrow Down - Shoot

General keys:
R - Restart game
ESC - Exits game

"""

import pygame
import random
import math
import config
import text_file
import pg_init
import cProfile

# TODO:
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
    """
    Main class for sprite inheritance. 
    
    Creates image and rect parameters for game use. 
    
     Args:
        pygame.sprite.Sprite:
            Inherits from pygame.sprite class to gain functions for image rendering on screen. 
    """
    def __init__(self, image, image_size):
        """
        Initialization of Sprite class.

        Args:
            image (type: string):
                The adress of image on computer to be used in the rendition in game. 

            image_size (type: int):
                Size by size of image to be rendered on screen. 
        """
        super().__init__()
        self.image = image
        self.image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (image_size,image_size))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect() 
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1
         
    def moving_ypos(self): # Moving object up and down
        """
        Inherited functions for moving of unplayable objects.
        
        Will be used by obstacles and fuel objects.
        """
        self.rect.centery += self.speed
        if self.rect.centery >= self.original_ypos + 100 or self.rect.centery <= self.original_ypos - 100:
            self.speed *= -1

class Obstacle(Sprite):
    """
    Obstacle class for game manipulation.
    
    Visualized as a black hole.
    
    Inherits from Sprite class for image rendering. 
    """
    def __init__(self, image, image_size):
        super().__init__(image, image_size)
        self.original_image = self.image
        self.rect.centerx = float(random.uniform(200, config.SCREEN_X-200))
        self.rect.centery = float(random.uniform(200, config.SCREEN_Y-200))
        self.original_ypos = self.rect.centery
        self.angle = 0
        
    def rotate(self):
        """
        Function for self rotation of image to simulate black hole in reality. 
        
        Non-functional for game play.
        """
        self.angle += 1
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(self.image, self.rect)
        
    def update(self):
        """
        Self updating function for obstacle class.
        Consists of auto movement in y-axis and rotation of center point. 
        """
        self.moving_ypos()
        self.rotate()
        
class Fuel(Sprite):
    """
    Fuel class for object in game. Players can gain fuel when touched in game. 

    Args:
        Sprite(Class): 
            Inherits Sprite to gain functions and rendering of image to be seen on screen. 
    """
    def __init__(self, image, image_size):
        super().__init__(image, image_size)
        self.rect.centerx = float(random.uniform(400, config.SCREEN_X-400))
        self.rect.centery = float(random.uniform(400, config.SCREEN_Y-400))
        self.original_ypos = self.rect.centery
        self.speed = -1
        
    def update(self):
        self.moving_ypos()


class Player_Object(Sprite): # Spiller klassea
    """
    Player object class for game and human manipulation. 
    Will only have two instances, one to each player in game. 

    Args:
        Sprite (Class):
            Inherits Sprite to gain functions and rendering of image to be seen on screen. 
    """
    class Bullet(pygame.sprite.Sprite):
        """
        Bullet class for bullet object from Player_Object.

        Players can shoot bullets at other players to take health points. 

        Bullets class will be used to detect collision on players, and use the speed and angle of spacecraft to its trajectory. 
        """
        def __init__(self, angle, x, y, number):
            """
            Initiation of bullet class.

            Args:
                Angle (type: int):
                    Takes in angle of spacecraft that shot to calculate velocity in x and y axis.

                x (type: int):
                    x coordinate of spacecraft when shot.
                
                y (type: int):
                    y coordinate of spacecraft when shot. 

                number (type int):
                    Number of player that shot bullet, dictates colour of bullet. 
            """
            super().__init__()
            self.image = pygame.Surface([3, 3])
            if number == 1:
                self.image.fill(config.PINK)
            else:
                self.image.fill(config.CYAN)
            self.rect = self.image.get_rect()
            self.angle = angle
            self.speed_y = -math.cos(math.radians(self.angle))
            self.speed_x = math.sin(math.radians(self.angle))  
            self.rect.centery = y + self.speed_y * 40
            self.rect.centerx = x + self.speed_x * 40
            
        def hitPlayer(self, group):
            """
            Hit detection function. Will go through list of collided objects, and find player classes.

            Will take health of player object in hit list and removes itself. 

            Args:
                Sprite group(type: list): 
                    Takes in list of all objects on screen. Finds the one that is in collission with bullet in list. 
            """
            hit_list = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)
            for sprite in hit_list:
                self.kill()
                if isinstance(sprite, Player_Object):
                    sprite.health -= 10
    
        def outOfBounds(self):
            """
            Out of bounds function for bullet.

            When out of screen, bullet is removed. 
            """
            if self.rect.centerx < 0 or self.rect.centerx > config.SCREEN_X:
                self.kill()
            if self.rect.centery < 160 or self.rect.centery > config.SCREEN_Y:
                self.kill()    

        def update(self, group):
            self.outOfBounds()
            self.hitPlayer(group)
            self.rect.move_ip(round(self.speed_x * 10),round(self.speed_y * 10))
            
    def __init__(self, player_number, image, image_size):
        """
        Initialization of Player object class.

        Args:
            player_number (type: int):
                Player object gets a specific number that dictates start position and colour. 

            image (type: string):
                The adress of image on computer to be used in the rendition in game. 

            image_size (type: int):
                Size by size of image to be rendered on screen. 
        """
        super().__init__(image, image_size)
        self.number = player_number
        self.original_image = self.image # Used for rotation of image to avoid pixel distortion
        self.score = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.resetAll()

    def resetAll(self):
        """
        Restart of self paramters. Nulls all parameters and sets player object to its respective position.

        Normally used after death. 
        """
        if self.number == 1: 
            self.rect.centerx = 100
            self.rect.centery = config.SCREEN_Y / 2
        else: 
            self.rect.centerx = config.SCREEN_X - 100
            self.rect.centery = config.SCREEN_Y / 2
        self.speed_x = 0
        self.speed_y = 0
        self.angle = 0
        self.fuel = config.FUEL
        self.health = config.HEALTH
            

    def screen_bars_update(self): ## Dette kan gå inni text_file
        """
        Simple function to visualize text and bars for health and fuel of player object. 

        Uses function in text_file.py.
        """
        text_file.showTextAndBar(self.number, self.score, self.health, self.fuel)
            
    def shoot(self):
        """
        Shoot function for player object.

        Returns bullet for Game class manipulation.
        """
        bullet = self.Bullet(self.angle, self.rect.centerx, self.rect.centery, self.number)
        return bullet # returneres for class Game controll
        
    def rotateObject(self, value):
        """
        Function to rotate spacecraft from human input. 

        Args:
            Value (int):
                The amount of change in angle of spacecraft from human input
        """
        self.angle += value
        self.angle = self.angle % 360
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(self.image, self.rect)

    def gravity(self):
        """
        Gravity influence on spacecraft. Does not go faster than 5 pixels in y direction.

        """
        if self.speed_y < 5:
            self.speed_y += config.GRAVITY
        
    def acceleration(self):
        """
        Function for speed when key pressed for acceleration. 

        Adds cos and sin for angle on velocity in y and x direction, respectively. 
        
        """
        self.speed_y += -math.cos(math.radians(self.angle))
        self.speed_x +=  math.sin(math.radians(self.angle))
            
    def hitObject(self, group):
        """
        Function to check for collision against objects on screen such as fuel, obstacle or other players. 

        Args:
            group (type: list of sprites)
                Acquire list of sprites/objects portrayed on screen.

                Will be used to check for collision depending on object/class type. 
        """
        hit_list = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)
        for object in hit_list:
            if object != self:
                if isinstance(object, Obstacle):
                    self.health = 0
                if isinstance(object, Fuel):
                    self.fuel = 100
                    object.kill()
                    group.add(Fuel(config.F_IMAGE, 50))
                if isinstance(object, Player_Object):
                    self.health -= 10
                    self.speed_x *= -1
                    self.speed_y *= -1

                    
    def BounceOfWall(self):
        """
        Function to bounce of walls if hit.

        Helps to keep the player object on screen. 

        Loses health on impact. 
        """
        if self.rect.centerx < 0+30 or self.rect.centerx > config.SCREEN_X-10:
            self.health -= 10
            self.speed_x *= -1
        if self.rect.centery < 160 or self.rect.centery > config.SCREEN_Y-10:
            self.health -= 10
            self.speed_y *= -1
            if self.fuel == 0:
                self.health = 0


    def update(self):
        self.gravity()
        self.BounceOfWall()
        self.screen_bars_update()
        self.rect.move_ip(round(self.speed_x),round(self.speed_y))
        
class Game:
    """
    Main class for orchestrating game functions. 

    Have control of all objects in respective groups for manipulation and game checks.
    """
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.sprite_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.fuel_group = pygame.sprite.Group()
        self.resetGame()
        
    def key_inputs(self, player1, player2):
        """
        Function to keep track of key inputs from human on interface.

        Key inputs manipulate player object trajectories and functions. 

        Args:
            player1/player2 (type: Player_Object Class):
                Key inputs manipulate parameters and functions of player object on screen. 

                The arguments of player objcts will be altered depending on which keys pressed. 

        """
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
        """
        Function that checks if player score has reached the final number of three, which indicates end of game.

        Game restarts after a 3 second wait to make the loser feel additionaly bad. 

        Args:
            player1/player2 (type: Player_Object Class):
                Enters the player objects score value to check for end of game. 
        """
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
        """
        Empties sprite and bullet group to create a new fresh start. 
        
        Used when initiating game, "R" key is pressed, or when one player has reached score value of 3. 
        """
        pygame.sprite.Group.empty(self.sprite_group)
        pygame.sprite.Group.empty(self.bullet_group)
        self.sprite_group.add(Player_Object(1, config.T_IMAGE, 30)) # Spiller 1
        self.sprite_group.add(Player_Object(2, config.T2_IMAGE, 30)) # Spiller 2
        self.player_group = self.sprite_group.sprites()
        self.sprite_group.add(Obstacle(config.O_IMAGE, 100))
        self.sprite_group.add(Obstacle(config.O_IMAGE, 100))
        self.sprite_group.add(Fuel(config.F_IMAGE, 50))

    def play_game(self):
        """
        Main game function, always running until the game is exited. 

        Controls player score and key inputs. 

        Blits also objects on screen and updates for each tick. 
        """
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

            pg_init.screen.blit(pg_init.B_IMAGE, (0,0))
            pygame.draw.rect(pg_init.screen, config.WHITE, pygame.Rect(0, 140, config.SCREEN_X, 5)) # Health bar
            self.sprite_group.update()
            self.bullet_group.update(self.player_group) 
            for player in self.player_group:
                player.hitObject(self.sprite_group)
            
            self.bullet_group.draw(pg_init.screen)
            self.sprite_group.draw(pg_init.screen)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(config.FPS)


if __name__ == "__main__":
    cProfile.run("Game().play_game()")
    