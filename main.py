import pygame
from pygame.locals import *


class Game():
    def __init__(self, l: int, w: int, h: int):
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

    def turn(self, player: str, x: int, y: int, z: int) -> bool:
        if self.board[z][x][y] == ' ':
            self.board[z][x][y] = player
            return True
        return False

    def __str__(self) -> str:
        string = ''
        for z in self.board:
            for x in z:
                string += ' '.join(map(lambda y: f'[{y}]',x))
                string += '\n'
            string += '\n'
        return string


def main():
    game = Game(3, 3, 3)

    print(game)
    game.turn('X', 0, 0, 0)
    print(game)


if __name__ == '__main__':
    main()
