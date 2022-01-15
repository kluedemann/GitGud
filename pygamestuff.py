import pygame

def main():
    pygame.init()
    pygame.display.set_mode((500, 400)) # set display size
    my_sur = pygame.display.get_surface()
    rect = pygame.Rect(100, 100, 200, 200)
    pygame.draw.rect(my_sur, pygame.Color('white'), rect)
    pygame.quit()
