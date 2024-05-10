import pygame
import random
import sys
import copy

 # check valid current dimension from the current position
def validDirections(x, y, minX = 0, minY = 0, maxX = 7, maxY = 7):
    directions = []
    if x != minX:
        directions.append((x-1, y))
    if x != minX and y != minY:
        directions.append((x-1, y-1))
    if x != minX and y != maxY:
        directions.append((x-1, y+1))
    if x != maxX:
        directions.append((x+1, y))
    if x != maxX and y != minY:
        directions.append((x+1, y-1))
    if x != maxX and y != maxY:
        directions.append((x+1, y+1))
    if y != minY:
        directions.append((x, y-1))
    if y != maxY:
        directions.append((x, y+1))
    return directions
def loadImage(path, size):
    image = pygame.image.load(f"{path}").convert_alpha()
    image = pygame.transform.scale(image, size)
    return image


class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption('Othello')

        self.rows = 8
        self.columns = 8
        self.grid = Grid(self.rows, self.columns, (50, 50), self)
        self.difficulty = 0

        self.currentPlayer = 1
        self.RUN = True

    def start(self):
        while self.difficulty == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUN = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy_button.collidepoint(event.pos):
                        self.difficulty = 1
                    elif self.medium_button.collidepoint(event.pos):
                        self.difficulty = 3
                    elif self.hard_button.collidepoint(event.pos):
                        self.difficulty = 5

            self.screen.fill((0, 0, 0))

            # Centering the buttons
            button_width = 150  # Increased button width
            button_height = 50
            button_x = (self.screen.get_width() - button_width) // 2
            button_margin = 20
            button_y_start = 150

            # Draw difficulty selection buttons
            self.easy_button = pygame.Rect(button_x, button_y_start, button_width, button_height)
            self.medium_button = pygame.Rect(button_x, button_y_start + button_height + button_margin, button_width,
                                             button_height)
            self.hard_button = pygame.Rect(button_x, button_y_start + 2 * (button_height + button_margin), button_width,
                                           button_height)

            # Change button color to gray
            button_color = (150, 150, 150)
            pygame.draw.rect(self.screen, button_color, self.easy_button)
            pygame.draw.rect(self.screen, button_color, self.medium_button)
            pygame.draw.rect(self.screen, button_color, self.hard_button)

            font = pygame.font.Font(None, 36)
            text_color = (255, 255, 255)

            # Centering the text on buttons
            easy_text_width, easy_text_height = font.size('Easy')
            easy_text_x = button_x + (button_width - easy_text_width) // 2
            easy_text_y = button_y_start + (button_height - easy_text_height) // 2

            medium_text_width, medium_text_height = font.size('Medium')
            medium_text_x = button_x + (button_width - medium_text_width) // 2
            medium_text_y = button_y_start + button_height + button_margin + (button_height - medium_text_height) // 2

            hard_text_width, hard_text_height = font.size('Hard')
            hard_text_x = button_x + (button_width - hard_text_width) // 2
            hard_text_y = button_y_start + 2 * (button_height + button_margin) + (button_height - hard_text_height) // 2

            self.screen.blit(font.render('Easy', True, text_color), (easy_text_x, easy_text_y))
            self.screen.blit(font.render('Medium', True, text_color), (medium_text_x, medium_text_y))
            self.screen.blit(font.render('Hard', True, text_color), (hard_text_x, hard_text_y))

            pygame.display.flip()
    def run(self):
        self.start()
        while self.RUN:
            self.input()
            self.update()
            self.draw()
        pygame.quit()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.drawGrid()
                    self.grid.drawGUIGrid(self.screen)

    def update(self):
        pass

    def draw(self):
        self.screen.fill((128, 128, 128))
        self.grid.drawGUIGrid(self.screen)
        pygame.display.update()


class Grid:
    def __init__(self, rows, columns, size, main):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.GAME = main

        self.whiteToken = loadImage('Image/WhiteToken.png', (48, 48))
        self.blackToken = loadImage('Image/BlackToken.png', (48, 48))

        self.Tokens = {}

        # # Initialize the grid with all cells empty
        self.gridLogic = [[0 for _ in range(columns)] for _ in range(rows)]

        self.gridLogic = self.GenerateGrid(self.rows, self.columns)

    def GenerateGrid(self, rows, columns):
        grid = []
        for row in range(rows):
            line = []
            for column in range(columns):
                line.append(0)
            grid.append(line)

        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, 2, 3, 4)
        self.insertToken(grid, 2, 4, 3)
        self.insertToken(grid, 1, 4, 4)
        return grid



    def checkValidMove(self, grid, currentPlayer):
        validMoves = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:       # If the cell is not empty, already has a token
                    continue
                DIRECTIONS = validDirections(gridX, gridY)
                for direc in DIRECTIONS:          # check adjacent cells for valid moves
                    dirx, dirx = direc
                    checkCell = grid[dirx][dirx]

                    if checkCell == 0 or checkCell == currentPlayer:
                        continue
                    if (dirx, dirx) in validMoves:          # If the cell is already in the valid moves list, not add it again
                        continue
                    validMoves.append((dirx, dirx))        # Add the cell to the valid moves list
        return validMoves


    def drawGrid(self):
        print('Drawing Grid')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for column in row:
                line += f"{column} ".center(3, " ") + '|'
            print(line)
        print()

    def drawGUIGrid(self, screen):
        cell_size = 50  # Adjust the size of each grid cell
        for row_index in range(self.rows):
            for col_index in range(self.columns):
                x = col_index * cell_size
                y = row_index * cell_size
                pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

                if (row_index, col_index) in self.Tokens:
                    token = self.Tokens[(row_index, col_index)]
                    token.drawToken(screen)

                availableMoves = self.checkValidMove(self.gridLogic, self.GAME.currentPlayer)
                for move in availableMoves:
                    x = move[1] * cell_size
                    y = move[0] * cell_size
                    pygame.draw.circle(screen, (0, 255, 0), (x + 25, y + 25), 5)

    def insertToken(self,grid, currentPlayer, y, x):
        if currentPlayer == 1:
            tokenImage = self.whiteToken
        else:
            tokenImage = self.blackToken

        self.Tokens[(y, x)] = Token(currentPlayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.Tokens[(y, x)].player




class Token:
    def __init__(self, player, gridx, gridy, image, main):
        self.player = player
        self.gridx = gridx
        self.gridy = gridy
        self.posX =  (gridx * 50)
        self.posY =  (gridy * 50)
        self.image = image
        self.GAME = main

    def transition(self):
        pass

    def drawToken(self, screen):
        self.GAME.screen.blit(self.image, (self.posX, self.posY))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Othello()
    game.run()
