import pygame
import copy


# check valid current directions from the current position
def validDirections(x, y, minX=0, minY=0, maxX=7, maxY=7):
    directions = []
    if x != minX:
        directions.append((x - 1, y))
    if x != minX and y != minY:
        directions.append((x - 1, y - 1))
    if x != minX and y != maxY:
        directions.append((x - 1, y + 1))
    if x != maxX:
        directions.append((x + 1, y))
    if x != maxX and y != minY:
        directions.append((x + 1, y - 1))
    if x != maxX and y != maxY:
        directions.append((x + 1, y + 1))
    if y != minY:
        directions.append((x, y - 1))
    if y != maxY:
        directions.append((x, y + 1))
    return directions


def loadImage(path, size):
    image = pygame.image.load(f"{path}").convert_alpha()
    image = pygame.transform.scale(image, size)
    return image


def evaluateBoard(grid, currentPlayer):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score


class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption('Othello')

        self.rows = 8
        self.columns = 8
        self.difficulty = 0
        self.grid = Grid(self.rows, self.columns, (50, 50), self)
        self.ComputerAI = ComputerAI(self.grid)


        self.player1 = -1
        self.player2 = 1

        self.currentPlayer = -1
        self.RUN = True

    def start(self):
        while self.difficulty == 0 and self.RUN:
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
        while self.RUN:
            # self.start()
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
                    self.grid.printGrid()
                    self.grid.drawGUIGrid(self.screen)
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x, y = (x) // 50, (y) // 50

                    validCells = self.grid.checkValidCells(self.grid.gridLogic, self.currentPlayer)
                    if not validCells:
                        pass
                    else:
                        if (y, x) in validCells:
                            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, x, y)
                            swapMoves = self.grid.changeColorOfTokens(y, x, self.grid.gridLogic, self.currentPlayer)
                            for move in swapMoves:
                                self.grid.animateTransitions(move, self.currentPlayer)
                                self.grid.gridLogic[move[0]][move[1]] *= -1
                            self.currentPlayer *= -1
                            self.grid.printGrid()
                            self.grid.drawGUIGrid(self.screen)

    def update(self):


        if self.currentPlayer == 1:

            move, score = self.ComputerAI.minMax(self.grid.gridLogic, 5, float('-inf'), float('inf'), 1)
            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, move[1], move[0])
            swapMoves = self.grid.changeColorOfTokens(move[0], move[1], self.grid.gridLogic, self.currentPlayer)
            for move in swapMoves:
                self.grid.animateTransitions(move, self.currentPlayer)
                self.grid.gridLogic[move[0]][move[1]] *= -1
            self.currentPlayer *= -1

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
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, -1, 4, 3)
        self.insertToken(grid, 1, 4, 4)
        return grid

    def checkValidCells(self, grid, currentPlayer):
        validMoves = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:  # If the cell is not empty, already has a token
                    continue
                DIRECTIONS = validDirections(gridX, gridY)

                for direction in DIRECTIONS:  # check adjacent cells for valid moves
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == currentPlayer:
                        continue

                    if (gridX, gridY) in validMoves:  # If the cell is already in the valid moves list, not add it again
                        continue

                    validMoves.append((gridX, gridY))  # Add the cell to the valid moves list
        return validMoves

    def changeColorOfTokens(self, x, y, grid, currentPlayer):
        surroundingTokens = validDirections(x, y)
        if len(surroundingTokens) == 0:
            return []
        changedTokens = []
        for token in surroundingTokens:
            tokenX, tokenY = token
            diffTokenX, diffTokenY = tokenX - x, tokenY - y
            currentLine = []

            RUN = True
            while RUN:  # search for the valid token that can be changed
                if grid[tokenX][tokenY] == currentPlayer * -1:
                    currentLine.append((tokenX, tokenY))
                elif grid[tokenX][tokenY] == currentPlayer:
                    RUN = False
                    break
                elif grid[tokenX][tokenY] == 0:
                    currentLine.clear()
                    RUN = False

                # Move the token to the current player
                tokenX += diffTokenX
                tokenY += diffTokenY

                if tokenX < 0 or tokenX > 7 or tokenY < 0 or tokenY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                changedTokens.extend(currentLine)
        return changedTokens

    def findAvailableMoves(self, grid, currentPlayer):
        validMoves = self.checkValidCells(grid, currentPlayer)
        availableMoves = []
        for move in validMoves:
            x, y = move
            if move in availableMoves:
                continue
            changedTokens = self.changeColorOfTokens(x, y, grid, currentPlayer)
            if len(changedTokens) > 0:
                availableMoves.append(move)
        return availableMoves

    def printGrid(self):
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

        for token in self.Tokens.values():
            token.drawToken(screen)

        avialableMoves = self.findAvailableMoves(self.gridLogic, self.GAME.currentPlayer)
        if self.GAME.currentPlayer == -1:
            for move in avialableMoves:
                x, y = move
                rect_x = y * cell_size + 2
                rect_y = x * cell_size + 2
                pygame.draw.rect(screen, (255, 255, 0), (rect_x, rect_y, cell_size - 4, cell_size - 4), 1)

    def insertToken(self, grid, currentPlayer, x, y):
        if currentPlayer == -1:
            tokenImage = self.blackToken
        else:
            tokenImage = self.whiteToken

        self.Tokens[(x, y)] = Token(currentPlayer, x, y, tokenImage, self.GAME)
        grid[y][x] = self.Tokens[(x, y)].player

    def animateTransitions(self, cell, player):
        if player == -1:
            self.Tokens[(cell[1], cell[0])].transition(self.whiteToken, self.blackToken)
        else:
            self.Tokens[(cell[1], cell[0])].transition(self.blackToken, self.whiteToken)


class ComputerAI:
    def __init__(self, grid):
        self.grid = grid
    def minMax(self, grid, depth, alpha, beta, currentPlayer):
        copyGrid = copy.deepcopy(grid)

        validMoves = self.grid.findAvailableMoves(copyGrid, currentPlayer)
        if depth == 0 or len(validMoves) == 0:
            bestMove, score = None, evaluateBoard(grid, currentPlayer)
            return bestMove, score

        if currentPlayer == -1:
            maxEval = float('-inf')
            bestMove = None

            for move in validMoves:
                x, y = move
                swappedMoves = self.grid.changeColorOfTokens(y, x, copyGrid, currentPlayer)
                copyGrid[y][x] = currentPlayer
                for i in swappedMoves:
                    copyGrid[i[0]][i[1]] = currentPlayer

                bMove, value = self.minMax(copyGrid, depth - 1, alpha, beta, currentPlayer * -1)

                if value > maxEval:
                    maxEval = value
                    bestMove = move
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break

                copyGrid = copy.deepcopy(grid)
            return bestMove, maxEval

        if currentPlayer == 1:
            bestScore = float('inf')
            bestMove = None

            for move in validMoves:
                x, y = move
                swappedMoves = self.grid.changeColorOfTokens(y, x, copyGrid, currentPlayer)
                copyGrid[y][x] = currentPlayer
                for i in swappedMoves:
                    copyGrid[i[0]][i[1]] = currentPlayer

                bMove, value = self.minMax(copyGrid, depth - 1, alpha, beta, currentPlayer)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                copyGrid = copy.deepcopy(grid)
            return bestMove, bestScore


class Token:
    def __init__(self, player, gridx, gridy, image, main):
        self.player = player
        self.gridx = gridx
        self.gridy = gridy
        self.posX = (gridx * 50)
        self.posY = (gridy * 50)
        self.image = image
        self.GAME = main

    def transition(self, transitionImages, tokenImage):
        self.image = transitionImages
        self.GAME.draw()
        self.image = tokenImage

    def drawToken(self, screen):
        self.GAME.screen.blit(self.image, (self.posX, self.posY))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Othello()
    game.run()
