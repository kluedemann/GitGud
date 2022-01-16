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


    def heuristic(self, game: 'Game'):
        """
        Args:
        game: Tic tac toe game
        """
        score = 0
        n = game.l
        # player score
        for i in range(n):
            for j in range(n):
                count = [0, 0, 0]
                for k in range(n):
                    if game.board[i][j][k] == self.player:
                        count[0] += 1
                    if game.board[i][k][j] == self.player:
                        count[1] += 1
                    if game.board[k][i][j] == self.player:
                        count[2] += 1
                for k in range(3):
                    if count[k] == n - 1:
                        score += 0.5
                    if count[k] == n - 2:
                        score += 0.25
        for i in range(n):
            count = [0] * 6
            for k in range(n):
                if game.board[i][k][k] == self.player:
                    count[0] += 1
                if game.board[k][i][k] == self.player:
                    count[1] += 1
                if game.board[k][k][i] == self.player:
                    count[2] += 1
                if game.board[i][n-k-1][k] == self.player:
                    count[3] += 1
                if game.board[n-k-1][i][k] == self.player:
                    count[4] += 1
                if game.board[n-k-1][k][i] == self.player:
                    count[5] += 1
            for k in range(6):
                if count[k] == n - 1:
                    score += 0.5
                if count[k] == n - 2:
                    score += 0.25
        count = [0] * 4
        for k in range(n):
            if game.board[k][k][k] == self.player:
                count[0] += 1
            if game.board[k][k][n-k-1] == self.player:
                count[1] += 1
            if game.board[k][n-k-1][k] == self.player:
                count[2] += 1
            if game.board[k][n-k-1][n-k-1] == self.player:
                count[3] += 1
        for k in range(4):
            if count[k] == n - 1:
                score += 0.5
            if count[k] == n - 2:
                score += 0.25
        # opponent score
        for i in range(n):
            for j in range(n):
                count = [0, 0, 0]
                for k in range(n):
                    if game.board[i][j][k] == self.opponent:
                        count[0] += 1
                    if game.board[i][k][j] == self.opponent:
                        count[1] += 1
                    if game.board[k][i][j] == self.opponent:
                        count[2] += 1
                for k in range(3):
                    if count[k] == n - 1:
                        score -= 0.5
                    if count[k] == n - 2:
                        score -= 0.25
        for i in range(n):
            count = [0] * 6
            for k in range(n):
                if game.board[i][k][k] == self.opponent:
                    count[0] += 1
                if game.board[k][i][k] == self.opponent:
                    count[1] += 1
                if game.board[k][k][i] == self.opponent:
                    count[2] += 1
                if game.board[i][n-k-1][k] == self.opponent:
                    count[3] += 1
                if game.board[n-k-1][i][k] == self.opponent:
                    count[4] += 1
                if game.board[n-k-1][k][i] == self.opponent:
                    count[5] += 1
            for k in range(6):
                if count[k] == n - 1:
                    score -= 0.5
                if count[k] == n - 2:
                    score -= 0.25
        count = [0] * 4
        for k in range(n):
            if game.board[k][k][k] == self.opponent:
                count[0] += 1
            if game.board[k][k][n-k-1] == self.opponent:
                count[1] += 1
            if game.board[k][n-k-1][k] == self.opponent:
                count[2] += 1
            if game.board[k][n-k-1][n-k-1] == self.opponent:
                count[3] += 1
        for k in range(4):
            if count[k] == n - 1:
                score -= 0.5
            if count[k] == n - 2:
                score -= 0.25
        return score


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

        return self.heuristic(game)


    def minimax(self, game: 'Game', player: str, alpha = - inf, beta = inf, depth: int = 0):
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
                            alpha,
                            beta,
                            depth + 1
                        )
                        game.board[z][x][y] = ' '
                        score[0], score[1], score[2] = z, x, y

                        if player == self.player:
                            if score[-1] > best[-1]:
                                best = score

                            if best[-1] >= beta:
                                return best

                            alpha = max(alpha, best[-1])
                        else:
                            if score[-1] < best[-1]:
                                best = score

                            if best[-1] <= alpha:
                                return best

                            beta = min(beta, best[-1])

        return best

    def action(self, game: 'Game'):
        """
        Args:
        game: Tic tac toe game
        """
        if game.turn_num < 5 or random.random() < self.epsilon:
            z, x, y = random.randint(0, game.h - 1), random.randint(0, game.l - 1), random.randint(0, game.w - 1)
            return z, x, y, 0
        else:
            return self.minimax(game, self.player)
