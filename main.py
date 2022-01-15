import pygame
from pygame.locals import *
import math


class Game():

    def __init__(
            self,
            surface: pygame.Surface,
            l: int = 3,
            w: int = 3,
            h: int = 3):
        self.surface = surface
        self.bg_color = pygame.Color('black')
        width = self.surface.get_width() // 3
        height = self.surface.get_height() // 3

        self.board = [
            [
                [
                    ' ' for _ in range(l)
                ] for _ in range(w)
            ] for _ in range(h)
        ]
        self.l = l
        self.w = w
        self.h = h

    def draw(self):
        angle = math.pi / 4
        offset = {
            'x': self.surface.get_width() / 2,
            'y': self.surface.get_height() / 2 - 300
        }

        for z, board in enumerate(self.board):
            for x, row in enumerate(board):
                for y, cube in enumerate(row):
                    center = (
                        offset['x'] - 100 * x * math.cos(angle) + 100 * y * math.sin(angle),
                        offset['y'] + 50 * x * math.cos(angle) + 50 * y * math.sin(angle) + z * 250
                    )
                    if cube == 'X':
                        pygame.draw.circle(
                            self.surface,
                            (255, 0, 0),
                            center,
                            5
                        )
                    elif cube == 'O':
                        pygame.draw.circle(
                            self.surface,
                            (0, 0, 255),
                            center,
                            5
                        )
                    else:
                        pygame.draw.circle(
                            self.surface,
                            (255, 255, 255),
                            center,
                            5
                        )


    def turn(self, player: str, x: int, y: int, z: int) -> bool:
        if self.board[z][x][y] == ' ':
            self.board[z][x][y] = player
            return True
        return False


    def play(self):
        self.draw()
        pygame.display.update()
        input()


    def __str__(self) -> str:
        string = ''
        for z in self.board:
            for x in z:
                string += ' '.join(map(lambda y: f'[{y}]', x))
                string += '\n'
            string += '\n'
        return string


def main():
    # initialize pygame modules
    pygame.init()
    # create display window
    pygame.display.set_mode((720, 720))
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


if __name__ == '__main__':
    main()
