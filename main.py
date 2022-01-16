import pygame
from pygame.locals import *
import math
from bot import Bot

class Game():

    def __init__(
            self,
            surface: pygame.Surface,
            l: int = 4,
            w: int = 4,
            h: int = 4):
        self.surface = surface
        self.bg_color = pygame.Color('black')

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
        self.game_over = False
        self.exit = False
        self.turn_num = 0
        self.players = ['X', 'O']
        self.board_coords = self.get_coords()
        self.bot = Bot(self.players[1], 2, 0)
        self.mode = 'AI'
        self.pos = None


    def draw(self):
        # Draw board with coloured circles
        for z, board in enumerate(self.board):
            for x, row in enumerate(board):
                for y, cube in enumerate(row):
                    center = self.board_coords[z][x][y]
                    radius = 5 * (1.15) ** (x + y)
                    if cube == 'X':
                        color = (255, 0, 0)
                    elif cube == 'O':
                        color = (0, 0, 255)
                    else:
                        color = (255, 255, 255)
                    pygame.draw.circle(
                            self.surface,
                            color,
                            center,
                            radius
                        )
        pygame.display.update()
        return


    def turn(self, player: str, x: int, y: int, z: int) -> bool:
        # Update board state
        if self.board[z][x][y] == ' ':
            self.board[z][x][y] = player
            return True
        return False


    def play(self):
        # Run main game loop
        self.draw()
        while not self.exit:
            self.get_events()
        return

    def update(self, player: str):
        print(self)
        self.draw()
        self.turn_num += 1
        if self.check_win(player) or self.turn_num == (self.l * self.w * self.h):
            self.game_over = True
            self.draw_over(player)


    def get_events(self):
        # Get pygame events
        events = pygame.event.get()
        for event in events:
            # Exit game
            if event.type == pygame.QUIT:
                self.exit = True
            elif event.type == pygame.MOUSEBUTTONUP and not self.game_over:
                # Attempt to play turn
                player = self.players[self.turn_num % 2]
                coords = pygame.mouse.get_pos()
                pos = self.get_pos(coords)
                if self.turn(player, pos[0], pos[1], pos[2]):
                    # Successful turn
                    self.update(player)
                    if self.mode == 'AI' and not self.game_over:
                        z, x, y, _ = self.bot.action(self)
                        player = self.players[self.turn_num % 2]
                        self.turn(player, x, y, z)
                        self.update(player)

            elif event.type == pygame.MOUSEMOTION:
                coords = pygame.mouse.get_pos()
                if self.pos is not None:
                    self.highlight(False)
                self.pos = self.get_pos(coords)
                if self.pos is not None:
                    self.highlight(True)
                pygame.display.update()

        return

    def highlight(self, is_yellow):
        x, y, z = self.pos

        if self.board[z][x][y] == 'X':
            color = (255, 0, 0)
        elif self.board[z][x][y] == 'O':
            color = (0, 0, 255)
        elif is_yellow:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        center = self.board_coords[z][x][y]
        radius = 5 * (1.15) ** (x + y)
        pygame.draw.circle(
            self.surface,
            color,
            center,
            radius
        )

        return

    def draw_over(self, player):
        if player != ' ':
            text_str = f"{player} wins!"
        else:
            text_str = f"Tie!"
        if player == 'X':
            color = (255, 0, 0)
        elif player == 'O':
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)
        text_font = pygame.font.SysFont('', 75)
        text_image = text_font.render(text_str, True, color)
        self.surface.blit(text_image, (500, 475))
        self.surface.blit(text_image, (50, 475))
        pygame.display.update()
        return

    def get_pos(self, coords):
        # Play a move at given coordinates
        for z, board in enumerate(self.board):
            for x, row in enumerate(board):
                for y, cube in enumerate(row):
                    if self.dist(coords, self.board_coords[z][x][y]) < 25:
                        return (x, y, z)
        return

    def dist(self, pos1, pos2):
        # Get dist between points
        total = 0
        for i in range(2):
            total += (pos1[i] - pos2[i]) ** 2
        return total ** (1/2)

    def get_coords(self):
        # Calculate board coordinates
        angle = math.pi / 4
        offset = {
            'x': self.surface.get_width() / 2,
            'y': self.surface.get_height() / 2 - 480
        }
        coords = []

        for z, board in enumerate(self.board):
            table = []
            for x, row in enumerate(board):
                col = []
                for y, cube in enumerate(row):
                    center = (
                        int(offset['x'] - 100 * x * math.cos(angle) + 100 * y * math.sin(angle)),
                        int(offset['y'] + 50 * x * math.cos(angle) + 50 * y * math.sin(angle) + z * 250)
                    )
                    col.append(center)
                table.append(col)
            coords.append(table)
        return coords

    def check_win(self, player):
        # Check rows/cols
        # assuming x == y == z
        n = self.l
        for i in range(n):
            for j in range(n):
                count = [0, 0, 0]
                for k in range(n):
                    if self.board[i][j][k] == player:
                        count[0] += 1
                    if self.board[i][k][j] == player:
                        count[1] += 1
                    if self.board[k][i][j] == player:
                        count[2] += 1
                for k in range(3):
                    if count[k] == n:
                        return True
        for i in range(n):
            count = [0] * 6
            for k in range(n):
                if self.board[i][k][k] == player:
                    count[0] += 1
                if self.board[k][i][k] == player:
                    count[1] += 1
                if self.board[k][k][i] == player:
                    count[2] += 1
                if self.board[i][n-k-1][k] == player:
                    count[3] += 1
                if self.board[n-k-1][i][k] == player:
                    count[4] += 1
                if self.board[n-k-1][k][i] == player:
                    count[5] += 1
            for k in range(6):
                if count[k] == n:
                    return True
        count = [0] * 4
        for k in range(n):
            if self.board[k][k][k] == player:
                count[0] += 1
            if self.board[k][k][n-k-1] == player:
                count[1] += 1
            if self.board[k][n-k-1][k] == player:
                count[2] += 1
            if self.board[k][n-k-1][n-k-1] == player:
                count[3] += 1
        for k in range(4):
            if count[k] == n:
                return True
        return False


    def __str__(self) -> str:
        # Convert board to string
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
    pygame.display.set_mode((720, 1000))
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
