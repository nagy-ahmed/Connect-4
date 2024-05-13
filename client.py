import socket
import threading
import numpy as np
import pygame
import sys
import math

host = '127.0.0.1'
port = 8080
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

row_count = 6
col_count = 7
game_over = False
turn = False
flag = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

def create_thread(target):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()

def receive_data():
    global flag, game_over, turn,board

    while True:
        data = sock.recv(1024).decode()  # Receive the data
        dataa = data.split('-')
        print(dataa)
        row = int(dataa[0])
        col = int(dataa[1])
        if not turn:
            if dataa[2] == 'YourTurn':
                if isValidLocation(board, col):
                    row = nextOpenRow(board, col)
                    dropPiece(board, row, col, 2)
                    drawBoard(board)
                    flag += 1
                    gameOver(board)
                    if winningMove(board, 2):
                        label = myfont.render("Player 1 wins !!!", 1, yellow)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        
                turn=True


def createBoard():
    b = np.zeros((row_count, col_count))
    return b

def drawBoard(board):
    for c in range(col_count):
        for r in range(row_count):
            pygame.draw.rect(screen, blue, (c * squaresize, r * squaresize + squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, black, (int(c * squaresize + squaresize / 2), int(r * squaresize + squaresize + squaresize / 2)), radius)

    for c in range(col_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, yellow, (int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, red, (int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
    pygame.display.update()


def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isValidLocation(board, col):
    return board[row_count-1][col] == 0

def nextOpenRow(board, col):
    for row in range(row_count):
        if board[row][col] == 0:
            return row

def printBoard(board):
    print(np.flip(board, 0))

def gameOver(board):
    global flag
    if flag == 42 and not winningMove(board, 1) and not winningMove(board, 2):
        print("Game Over")
        label = myfont.render("Tied Game !!!", 1, green)
        screen.blit(label, (40, 10))

        pygame.display.update()
        pygame.time.wait(5000)
        board=createBoard()
        flag = 0
        drawBoard(board)

def winningMove(board, piece):
    # Check horizontal locations
    for c in range(col_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(col_count):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively diagonals
    for c in range(col_count - 3):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively diagonals
    for c in range(col_count - 3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True



board = createBoard()
pygame.init()

squaresize = 80
width = col_count * squaresize
height = (row_count + 1) * squaresize
size = (width, height)
radius = int(squaresize / 2 - 5)
screen = pygame.display.set_mode(size)

drawBoard(board)

myfont = pygame.font.SysFont("monospace", 50)

create_thread(receive_data)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0,0, width, squaresize))
            posx=event.pos[0]

            if flag==42 or winningMove(board, 1) or winningMove(board, 2):
                board=createBoard()
                flag=0
                drawBoard(board)

            if turn:
                pygame.draw.circle(screen, yellow, (posx, int(squaresize/2)), radius)
           

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.draw.rect(screen, black, (0,0, width, squaresize))
            
            if turn:
                posx=event.pos[0]
                col=int(math.floor(posx/squaresize))

                if isValidLocation(board, col):
                    row=nextOpenRow(board, col)
                    dropPiece(board, row, col, 1)
                    flag+=1

                    send_data=f"{row}-{col}-YourTurn"
                    sock.send(send_data.encode())
                    print(send_data)
                    turn=False
                    gameOver(board)
                    drawBoard(board)


                    if winningMove(board, 1):
                        label= myfont.render("You wins !!!", 1, red)
                        screen.blit(label, (40,10))
                        pygame.display.update()
                        pygame.time.wait(5000)



                        

                        
         



