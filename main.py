from typing import Tuple
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
        self.bot = Bot(self.players[1], max_depth=3, epsilon=0)
        self.mode = 'AI'
        self.pos = None
        self.winning_line = []
        self.start = True
        self.help = False

    def draw_start(self):
        the_image = pygame.image.load("./Start.png")
        the_image = pygame.transform.scale(the_image, self.surface.get_size())
        self.surface.blit(the_image, (0, 0))
        if self.mode == 'AI':
            the_image = pygame.image.load("./croppedAI.PNG")
            the_image = pygame.transform.scale(the_image, (335, 160))
            self.surface.blit(the_image, (367, 561))
        else:
            the_image = pygame.image.load("./cropped2P.PNG")
            the_image = pygame.transform.scale(the_image, (345, 162))
            self.surface.blit(the_image, (13, 557))
        pygame.display.update()
        return

    def draw_help(self):
        self.surface.fill((0, 0, 0))
        lines = ["This game is 4x4x4 Tic-Tac-Toe.", "Click a dot to play a move.", "You win by aligning four dots in a row.", "They may be connected",  "horizontally, vertically, or diagonally.",
        "Play against a friend or the AI.", "Red is X and goes first. O is blue.", "Click to go back."]
        color = (255, 100, 0)
        text_font = pygame.font.SysFont('', 50)
        for i, line in enumerate(lines):
            text_image = text_font.render(line, True, color)
            self.surface.blit(text_image, (50, 75 + 75*i))
        pygame.display.update()
        return


    def draw(self, test=True):
        # Draw board with coloured circles
        self.surface.fill((0, 0, 0))
        for z, board in enumerate(self.board):
            for x, row in enumerate(board):
                for y, cube in enumerate(row):
                    center = self.board_coords[z][x][y]
                    radius = 5 * (1.25) ** (math.cos(self.angle) * x + math.sin(self.angle) *y)
                    if cube == 'X':
                        color = (255, 0, 0)
                    elif cube == 'O':
                        color = (0, 0, 255)
                    else:
                        #color = (100 + 155 * ((z) % 2), 255, 100 + 155 * ((z) % 2))
                        color = (255, 255, 255)

                    pygame.draw.circle(
                            self.surface,
                            color,
                            center,
                            radius
                        )
        if not self.game_over:
            self.draw_turn()
        else:
            self.draw_over()
        if test:
            pygame.display.update()
        return

    def draw_turn(self):
        player = self.players[self.turn_num % 2]
        text_str = f"{player}'s turn!"
        if player == 'X':
            color = (255, 0, 0)
        elif player == 'O':
            color = (0, 0, 255)
        text_font = pygame.font.SysFont('', 75)
        text_image = text_font.render(text_str, True, color)
        self.surface.blit(text_image, (0, 0))
        return


    def turn(self, player: str, x: int, y: int, z: int) -> bool:
        # Update board state
        if self.board[z][x][y] == ' ':
            self.board[z][x][y] = player
            return True
        return False


    def play(self):
        # Run main game loop
        # BOT GO FIRST
        # self.turn_num = 1
        self.draw_start()
        while self.start:
            self.get_events()

        if not self.exit:
            self.draw()

        # BOT GO FIRST
        # z, x, y, _ = self.bot.action(self)
        # player = self.players[self.turn_num % 2]
        # self.turn(player, x, y, z)
        # self.update(player)

        while not self.exit:
            self.get_events()
        return

    def update(self, player: str):
        print(self)
        self.turn_num += 1
        self.draw()
        won, self.winning_line = self.check_win(player)

        if won or self.turn_num == (self.l * self.w * self.h):
            self.game_over = True
            self.draw()




    def get_events(self):
        # Get pygame events
        events = pygame.event.get()
        for event in events:
            # Exit game
            if event.type == pygame.QUIT:
                self.start = False
                self.exit = True
            elif event.type == pygame.MOUSEBUTTONUP and not self.game_over and not self.start:
                # Attempt to play turn
                player = self.players[self.turn_num % 2]
                coords = pygame.mouse.get_pos()
                pos = self.get_pos(coords)
                if pos is not None and self.turn(player, pos[0], pos[1], pos[2]):
                    # Successful turn
                    self.update(player)
                    if self.mode == 'AI' and not self.game_over:
                        z, x, y, _ = self.bot.action(self)
                        player = self.players[self.turn_num % 2]
                        self.turn(player, x, y, z)
                        self.update(player)
            elif event.type == pygame.MOUSEBUTTONUP and self.start:
                coords = pygame.mouse.get_pos()
                print(coords)
                if self.help:
                    self.help = False
                    self.draw_start()
                elif 132 <= coords[0] <= 586 and 86 <= coords[1] <= 296:
                    self.start = False
                elif 16 <= coords[0] <= 357 and 561 <= coords[1] <= 720:
                    self.mode = ''
                    self.draw_start()
                elif 368 <= coords[0] <= 700 and 563 <= coords[1] <= 728:
                    self.mode = 'AI'
                    self.draw_start()
                elif 133 <= coords[0] <= 584 and 327 <= coords[1] <= 539:
                    self.help = True
                    self.draw_help()
            elif event.type == pygame.MOUSEMOTION and not self.start:
                coords = pygame.mouse.get_pos()
                update = False
                if self.pos is not None:
                    #self.highlight(False)
                    self.draw(False)
                    update = True
                self.pos = self.get_pos(coords)
                if self.pos is not None:
                    self.highlight(True)
                    update = True
                if update:
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
        radius = 5 * (1.25) ** (math.cos(self.angle) * x + math.sin(self.angle) *y)
        pygame.draw.circle(
            self.surface,
            color,
            center,
            radius
        )
        self.draw_lines()

        return

    def draw_lines(self):
        color = (255, 255, 0)
        x, y, z = self.pos
        start = self.board_coords[z][x][0]
        end = self.board_coords[z][x][3]
        pygame.draw.line(self.surface, color, start, end)
        start = self.board_coords[z][0][y]
        end = self.board_coords[z][3][y]
        pygame.draw.line(self.surface, color, start, end)
        start = self.board_coords[0][x][y]
        end = self.board_coords[3][x][y]
        pygame.draw.line(self.surface, color, start, end)
        # if x == y:
        #     start = self.board_coords[z][0][0]
        #     end = self.board_coords[z][3][3]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == z:
        #     start = self.board_coords[0][0][y]
        #     end = self.board_coords[3][3][y]
        #     pygame.draw.line(self.surface, color, start, end)
        # if z == y:
        #     start = self.board_coords[0][x][0]
        #     end = self.board_coords[3][x][3]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == 3 - y:
        #     start = self.board_coords[z][0][3]
        #     end = self.board_coords[z][3][0]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == 3 - z:
        #     start = self.board_coords[0][3][y]
        #     end = self.board_coords[3][0][y]
        #     pygame.draw.line(self.surface, color, start, end)
        # if z == 3 - y:
        #     start = self.board_coords[0][x][3]
        #     end = self.board_coords[3][x][0]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == y and z == y:
        #     start = self.board_coords[0][0][0]
        #     end = self.board_coords[3][3][3]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == y and z == 3 - y:
        #     start = self.board_coords[0][3][3]
        #     end = self.board_coords[3][0][0]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == 3 - y and z == x:
        #     start = self.board_coords[0][0][3]
        #     end = self.board_coords[3][3][0]
        #     pygame.draw.line(self.surface, color, start, end)
        # if x == 3 - y and z == y:
        #     start = self.board_coords[3][0][3]
        #     end = self.board_coords[0][3][0]
        #     pygame.draw.line(self.surface, color, start, end)
        return


    def draw_winning_line(self, color: Tuple[int, int, int]):
        point1, point2 = self.winning_line
        start = self.board_coords[point1[0]][point1[1]][point1[2]]
        end = self.board_coords[point2[0]][point2[1]][point2[2]]
        pygame.draw.line(self.surface, color, start, end)

    def draw_over(self):
        if self.turn_num == self.l * self.w*self.h:
            player = ' '
        else:
            player = self.players[1 - self.turn_num % 2]
        if player == 'X':
            color = (255, 0, 0)
        elif player == 'O':
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)
        if player != ' ':
            text_str = f"{player} wins!"
            self.draw_winning_line(color)
        else:
            text_str = f"Tie!"

        text_font = pygame.font.SysFont('', 75)
        text_image = text_font.render(text_str, True, color)
        self.surface.blit(text_image, (500, 475))
        self.surface.blit(text_image, (50, 475))
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
        self.angle = (math.pi / 4) + 0.1
        angle = self.angle
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
                        if k == 0:
                            winning_line = [(i, j, 0), (i, j, n - 1)]
                        elif k == 1:
                            winning_line = [(i, 0, j), (i, n - 1, j)]
                        elif k == 2:
                            winning_line = [(0, i, j), (n - 1, i, j)]
                        return True, winning_line
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
                    if k == 0:
                        winning_line = [(i, 0, 0), (i, n - 1, n - 1)]
                    elif k == 1:
                        winning_line = [(0, i, 0), (n - 1, i, n - 1)]
                    elif k == 2:
                        winning_line = [(0, 0, i), (n - 1, n - 1, i)]
                    elif k == 3:
                        winning_line = [(i, n - 1, 0), (i, 0, n - 1)]
                    elif k == 4:
                        winning_line = [(n - 1, i, 0), (0, i, n - 1)]
                    elif k == 5:
                        winning_line = [(n - 1, 0, i), (0, n - 1, i)]
                    return True, winning_line
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
                if k == 0:
                    winning_line = [(0, 0, 0), (n - 1, n - 1, n - 1)]
                elif k == 1:
                    winning_line = [(0, 0, n - 1), (n - 1, n - 1, 0)]
                elif k == 2:
                    winning_line = [(0, n - 1, 0), (n - 1, 0, n - 1)]
                elif k == 3:
                    winning_line = [(0, n - 1, n - 1), (n - 1, 0, 0)]
                return True, winning_line
        return False, []


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
    pygame.display.set_caption('Tic Tac Toe Tub')
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
