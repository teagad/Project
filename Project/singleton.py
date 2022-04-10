import pygame


class Singleton:
    pygame.init()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    block_size = 40
    left_margin = 40
    upper_margin = 50
    size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)
    screen = pygame.display.set_mode(size)
    font_size = int(block_size / 1.5)
    font = pygame.font.SysFont('notosans', font_size)
    pygame.display.set_caption("Морской бой")
