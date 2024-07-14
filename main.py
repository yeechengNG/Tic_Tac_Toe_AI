import sys
import pygame
import numpy as np
import random

pygame.init()

# Constants for colors, board size, etc.
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe with AI')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)  
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board = board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False

def minimax(minimax_board, depth, is_maximizing):
    # AI wins
    if check_win(player=2, check_board=minimax_board):
        return float('inf')
    
    # Human wins
    elif check_win(player=1, check_board=minimax_board):
        return float('-inf')
    
    # Tie
    elif is_board_full(minimax_board):
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, is_maximizing=False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, is_maximizing=True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move(difficulty):
    best_score = -1000
    move = (-1, -1)
    
    if difficulty == "easy":
        # Random move for easy level
        while True:
            row = random.randint(0, BOARD_ROWS - 1)
            col = random.randint(0, BOARD_COLS - 1)
            if board[row][col] == 0:
                mark_square(row, col, player=2)
                return True
    
    elif difficulty == "medium":
        # Simple heuristic for medium level (e.g., prioritize center and corners)
        # Example: prioritize center, then corners, then random
        moves = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
        for move in moves:
            row, col = move
            if board[row][col] == 0:
                mark_square(row, col, player=2)
                return True
    
    elif difficulty == "impossible":
        # Minimax with alpha-beta pruning for impossible level
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth=0, is_maximizing=False)
                    board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        
        if move != (-1, -1):
            mark_square(move[0], move[1], player=2)
            return True
    
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def main():
    draw_lines()

    player = 1
    game_over = False
    difficulty = "medium"  # Default difficulty

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        game_over = True
                    # Switch player
                    player = player % 2 + 1

                    if not game_over:
                        if best_move(difficulty): 
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1

                    if not game_over:
                        if is_board_full():
                            game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    game_over = False
                    player = 1
                elif event.key == pygame.K_e:
                    difficulty = "easy"
                    restart_game()
                    game_over = False
                    player = 1
                elif event.key == pygame.K_m:
                    difficulty = "medium"
                    restart_game()
                    game_over = False
                    player = 1
                elif event.key == pygame.K_i:
                    difficulty = "impossible"
                    restart_game()
                    game_over = False
                    player = 1
    
        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GREY)
                draw_lines(GREY)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
