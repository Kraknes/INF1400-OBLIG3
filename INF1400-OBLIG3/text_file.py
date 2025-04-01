import pygame
import config
import pg_init

pygame.init()
pygame.font.init()

# Text
FONT_TEXT = pygame.font.Font('freesansbold.ttf', 30)
FONT_SCORE = pygame.font.Font('freesansbold.ttf', 90)

player_1_text = FONT_TEXT.render('Player 1', True, config.WHITE, None)
textRect1 = player_1_text.get_rect()
textRect1.topleft = (35,30)

player_2_text = FONT_TEXT.render('Player2', True, config.WHITE, None)
textRect2 = player_2_text.get_rect()
textRect2.topright = (config.SCREEN_X-35, 30)

def showTextAndBar(number, score, health, fuel):
    pg_init.screen.blit(player_1_text, textRect1)
    pg_init.screen.blit(player_2_text, textRect2)
    
    scoreText = FONT_SCORE.render(str(score), True, config.WHITE, None)
    textScoreRect = scoreText.get_rect()

    healthText = FONT_TEXT.render('Health: ' + str(health), True, config.BLUE, None)
    healthTextRect = healthText.get_rect()

    fuelText = FONT_TEXT.render('Fuel: ' + str(fuel), True, config.BLUE, None)
    fuelTextRect = fuelText.get_rect()

    if number == 1:
        # Score tekst
        textScoreRect.topleft = (340, 50)
        healthTextRect.topleft = (35,61)
        fuelTextRect.topleft = (35,101)

        # Visuell framvisning av liv og drivstoff
        pygame.draw.rect(pg_init.screen, config.GREEN, pygame.Rect(30, 60, health*3, 30)) # Health bar
        pygame.draw.rect(pg_init.screen, config.YELLOW, pygame.Rect(30, 100, fuel*3, 30)) # Fuel bar
        pg_init.screen.blit(scoreText, textScoreRect)
        pg_init.screen.blit(healthText, healthTextRect)
        pg_init.screen.blit(fuelText, fuelTextRect)

    if number == 2:
        # Samme som ovenfor, bare for andre siden
        textScoreRect.topright = (config.SCREEN_X-340, 50)
        healthTextRect.topleft = (config.SCREEN_X - 330 ,61)
        fuelTextRect.topleft = (config.SCREEN_X - 330,101)
        
        pygame.draw.rect(pg_init.screen, config.GREEN, pygame.Rect(config.SCREEN_X - 330, 60, health*3, 30))
        pygame.draw.rect(pg_init.screen, config.YELLOW, pygame.Rect(config.SCREEN_X - 330, 100, fuel*3, 30))
        
    pg_init.screen.blit(scoreText, textScoreRect)
    pg_init.screen.blit(healthText, healthTextRect)
    pg_init.screen.blit(fuelText, fuelTextRect)