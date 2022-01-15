import pygame

def main():
    # initialize pygame modules
    pygame.init()
    # create display window
    pygame.display.set_mode((600, 600))
    # title display window
    pygame.display.set_caption('Tic Tac Toe')   
    # get display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # begin the main game loop calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit()
