import pygame
import config



pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y))
clock = pygame.time.Clock()
pygame.display.set_caption("Erling's Mayhamorama")