from typing import List
from math import inf
import random

class Bot():
    def __init__(self, player: str, max_depth: int, epsilon: float):
        """
        Args:
        board: Tic tac toe board
        player: character for the bot player
        epsilon: Probability of taking a random action
        """
        self.epsilon = epsilon
        self.player = player
        self.max_depth = max_depth
        self.opponent = 'O' if player == 'X' else 'X'

    def game_over(self, game: 'Game'):
        """
        Args:
        game: Tic tac toe game
        """
        return any([game.check_win(player) for player in game.players])

    def evaluate(self, game: 'Game'):
        """
        Args:
        game: Tic tac toe game
        """
        if self.game_over(game):
            if game.check_win(self.player):
                return 1
            elif game.check_win(self.opponent):
                return -1
            else:
                return 0
        return 0

    def minimax(self, game: 'Game', player: str, depth: int = 0):
        """
        Args:
        game: Tic tac toe game
        player: character for player
        """
        if depth >= self.max_depth or self.game_over(game):
            score = self.evaluate(game)
            return [-1, -1, -1, score]

        if player == self.player:
            best = [-1, -1, -1, -inf]
        else:
            best = [-1, -1, -1, inf]

        for z, board in random.sample(list(enumerate(game.board)), game.h):
            for x, row in random.sample(list(enumerate(board)), game.l):
                for y, cube in random.sample(list(enumerate(row)), game.w):
                    if cube == ' ':
                        game.board[z][x][y] = player
                        score = self.minimax(
                            game,
                            self.opponent if player == self.player else self.player,
                            depth + 1
                        )
                        game.board[z][x][y] = ' '
                        score[0], score[1], score[2] = z, x, y
                        if player == self.player:
                            if score[-1] > best[-1]:
                                best = score
                        else:
                            if score[-1] < best[-1]:
                                best = score

        return best

    def action(self, game: 'Game'):
        """
        Args:
        game: Tic tac toe game
        """
        if random.random() < self.epsilon:
            z, x, y = random.randint(0, game.h - 1), random.randint(0, game.l - 1), random.randint(0, game.w - 1)
            return z, x, y, 0
        else:
            return self.minimax(game, self.player)
