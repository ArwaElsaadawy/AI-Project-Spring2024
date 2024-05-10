import pygame
import random
import sys
import copy




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
        self.grid = Grid(self.rows, self.columns, (80, 80), self)

        self.RUN = True


    def run(self):
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

        self.whiteToken = loadImage('Image/WhiteToken.png', (50, 50))
        self.blackToken = loadImage('Image/BlackToken.png', (50, 50))

        self.Tokens = {}

        # # Initialize the grid with all cells empty
        self.gridLogic = [[0 for _ in range(columns)] for _ in range(rows)]
        # # Place initial tokens in the center
        # self.gridLogic[3][3] = 1  # White token
        # self.gridLogic[3][4] = 2  # Black token
        # self.gridLogic[4][3] = 2  # Black token
        # self.gridLogic[4][4] = 1  # White token

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
                # if self.gridLogic[row_index][col_index] == 1:  # White token
                #     pygame.draw.circle(screen, (255, 255, 255), (x + cell_size // 2, y + cell_size // 2), cell_size // 3)
                # elif self.gridLogic[row_index][col_index] == 2:  # Black token
                #     pygame.draw.circle(screen, (0, 0, 0), (x + cell_size // 2, y + cell_size // 2), cell_size // 3)


    def insertToken(self,grid, currentPlayer, x, y):
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
        self.posX = 80+ (gridx * 80)
        self.posY = 80 + (gridy * 80)
        self.image = image
        self.GAME = main

    def transition(self):
        pass

    def draw(self):
        self.GAME.screen.blit(self.image, (self.posX, self.posY))















# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Othello()
    game.run()


