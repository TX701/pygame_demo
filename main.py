import pygame
import random

pygame.init()

SCREEN_INFO = pygame.display.Info()
WINDOW_WIDTH = 800
GAME_WIDTH = 600
WINDOW_HEIGHT = 600
BLOCKSIZE = int(max(WINDOW_HEIGHT / 3, GAME_WIDTH / 3))
BLACK = (0, 0, 0)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.set_caption("Board")

class Tile:
  def __init__(self, rect, state):
    self.rect = rect
    self.state = state
    
    def __str__(self):
        return f"{self.state}"

def drawGrid(): 
    SCREEN.fill((255, 255, 255))
    
    board = [] # 2D array
    
    # creates a 3x3 grid
    for x in range(0, GAME_WIDTH, BLOCKSIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            board.append(Tile(rect, None))
            
    return board
            
# given an x coordinate and a y coordinate returns the tile that contains that coordinate
def getTile(x, y, board):
    for element in board:
        tile = element.rect
        if ((tile.left < x and x < (tile.left + BLOCKSIZE)) and (tile.top < y and y < (tile.top + BLOCKSIZE))):
            return element
        
    return Tile(None, -1)

# gets a random tile
def getRandTile(board):
    while not stale_mate(board):
        tile = board[random.randrange(0, len(board))]
        
        if tile.state == None:
            return tile
        
# adds a letter to the middle of a grid tile
def addSymbol(tile, symbol):
    if (tile.rect != None):
        square = tile.rect
        
        text = FONT.render(symbol, True, (0, 0, 0)) 
        rect = text.get_rect(center = (square.centerx, square.centery)) # places text in the middle of the tile
        SCREEN.blit(text, rect)

        tile.state = symbol

# checks if the given array of tiles all have the same state (and that state is not empty)   
def check(list):
    for element in list:
        if (list[0].state is None or list[0].state is not element.state):
            return False
        
    return list[0].state

# takes in indexs and returns corresponding elements from board
def create_list(list, board):
    created_list = []
    
    for i in list:
        created_list.append(board[i])
    
    return created_list

# uses the given 2D array as a faux 3D array to determine row / column / diagonal matches
def winCheck(board):
    winner = False
    
    for i in range(3):
        x = i * 3
        
        winner = check(create_list([x, x + 1, x + 2], board)) # get "rows"
        
        if winner != False and winner != None:
            return winner
        
        winner = check(create_list([i, i + 3, i + 6], board)) # get "columns"
        
        if winner != False and winner != None:
            return winner
        
    winner = check(create_list([0, 4, 8], board)) # back slash
        
    if winner != False and winner != None:
        return winner
        
    return check(create_list([2, 4, 6], board)) # forward slash

# checks if all tiles have a symbol on them
def stale_mate(board):
    for element in board:
        if element.state == None:
            return False       
    return True

def start_text(turn):
    starting_player = "X" if turn == 0 else "O"
    
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    text = FONT.render(f"{starting_player} starts", False, (0, 0, 0)) 
    
    SCREEN.blit(text, (625, 100))

def gameLoop():
    board = []
    
    board = drawGrid()
    turn = random.randint(0, 1)
    end_state = False
    exit = False
    
    x_win = 0; o_win = 0
    
    start_text(turn)
    
    while not exit:
        # if it is the COMPs turn
        if turn == 1:
            tile = getRandTile(board)
            addSymbol(tile, "O")
            
            end_state = winCheck(board)
            
            if end_state == "O":
                o_win += 1
            
            turn = 0
            
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                exit = True
                
            if event.type == pygame.MOUSEBUTTONUP and turn == 0:
                x, y = pygame.mouse.get_pos()
                tile = getTile(x, y, board)
                
                if tile.state == None:
                    addSymbol(tile, "X")
                    end_state = winCheck(board)
                    
                    if end_state == "X":
                        x_win += 1

                    turn = 1
                
            keys = pygame.key.get_pressed()
            
            # restart the game
            if keys[pygame.K_r]:
                board = drawGrid()
                
                turn = random.randint(0, 1)
                end_state = False           
                start_text(turn)    
                      
        # print(end_state)
        if end_state != False or stale_mate(board):
            
            text = f"Winner is: {end_state}" if not stale_mate(board) else "No winner"
            
            
            FONT = pygame.font.Font('freesansbold.ttf', 20)
            text = FONT.render(text, False, (0, 0, 0)) 
            SCREEN.blit(text, (625, 150))
            
            text = FONT.render(f"X wins: {x_win}", False, (0, 0, 0)) 
            SCREEN.blit(text, (625, 200))
            
            text = FONT.render(f"O wins: {o_win}", False, (0, 0, 0)) 
            SCREEN.blit(text, (625, 250))
            
            text = FONT.render(f"Press R to restart", False, (0, 0, 0)) 
            SCREEN.blit(text, (625, 300))
            
            turn = 2
            
        pygame.display.update()
        
gameLoop()