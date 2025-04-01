import pygame
import config

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