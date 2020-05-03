import pygame as game
import copy
import sudoku.solver as sudoku_solver
import math as mt

# inital assignments
N = 9
SQUARE_SIZE = 50
LINE_WIDTH = 1
INFORMATION_HEIGHT = 75
SUDOKU_BOARD_WIDTH = N * SQUARE_SIZE + LINE_WIDTH
SUDOKU_BOARD_HEIGHT = N * SQUARE_SIZE + LINE_WIDTH
GAME_BOARD_WIDTH = SUDOKU_BOARD_WIDTH
GAME_BOARD_HEIGHT = SUDOKU_BOARD_HEIGHT + INFORMATION_HEIGHT

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)


def check_exit():
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            quit()


def print_number(board, number: int, pos, color):
    # text properties
    font = game.font.Font('freesansbold.ttf', 32)
    
    # set a number to a specific position
    x = pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2
    y = pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2
    text = font.render('{}'.format(number), True, color, WHITE)
    textRect = text.get_rect()
    textRect.center = (x, y)
    board.blit(text, textRect)


def print_time(board, last_time, pos, color):
    # text properties
    font = game.font.Font('freesansbold.ttf', 32)
    
    # set a number to a specific position
    x = pos[0]
    y = pos[1]
    text = font.render('{}'.format(last_time), True, color, WHITE)
    textRect = text.get_rect()
    textRect.center = (x, y)
    board.blit(text, textRect)


def print_sudoku_board(board, sudoku_matrix, sudoku_matrix_ref, color, correct_wrong, lst):
    for k in range(N):
        for j in range(N):
            if sudoku_matrix_ref[k][j] == 0:
                if [k, j] in lst:
                    ind = lst.index([k, j])
                    if correct_wrong[ind] == 1:
                        print_number(board, sudoku_matrix[k][j], [k, j], GREEN)
                    elif sudoku_matrix[k][j] != 0:
                        print_number(board, sudoku_matrix[k][j], [k, j], color)
            else:
                print_number(board, sudoku_matrix[k][j], [k, j], RED)


def set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, pos):
    if sudoku_matrix_ref[pos[0]][pos[1]] == 0:
        sudoku_matrix[pos[0]][pos[1]] = number
    return sudoku_matrix


def main():
    sudoku_matrix = [[0, 0, 0, 0, 0, 4, 0, 9, 0],
                     [8, 0, 2, 9, 7, 0, 0, 0, 0],
                     [9, 0, 1, 2, 0, 0, 3, 0, 0],
                     [0, 0, 0, 0, 4, 9, 1, 5, 7],
                     [0, 1, 3, 0, 5, 0, 9, 2, 0],
                     [5, 7, 9, 1, 2, 0, 0, 0, 0],
                     [0, 0, 7, 0, 0, 2, 6, 0, 3],
                     [0, 0, 0, 0, 3, 8, 2, 0, 5],
                     [0, 2, 0, 5, 0, 0, 0, 0, 0]]
    sudoku_matrix_ref = copy.deepcopy(sudoku_matrix)
    sudoku_matrix_sol = sudoku_solver.get_sudoku_sol(copy.deepcopy(sudoku_matrix), N)[0]
    game.init()
    
    # square position
    square_pos = [LINE_WIDTH, LINE_WIDTH]
    square_pos_index = [0, 0]
    
    # set sudoku board width and height
    sudoku_board = game.display.set_mode((GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT))
    
    # set title
    game.display.set_caption("9x9 Sudoku Game!")
    
    # empty set for sudoku matrix
    lst = sudoku_solver.get_empty_list(sudoku_matrix, N)
    
    # correct/wrong list
    correct_wrong = [0] * len(lst)
    
    # loop initials
    number = 0
    total_sol_trial = 0
    sol_step = 0
    step_value = []
    solved = False
    solve_iter = False
    key_released = False
    clock = game.time.Clock()
    start_time = clock.get_time()
    while True:
        lasting_time = round((game.time.get_ticks() - start_time)/1000*10)/10
        sudoku_board.fill(WHITE)
        check_exit()
        
        # draw horizontal lines
        for k in range(N + 1):
            game.draw.line(sudoku_board, BLACK, [0, k * SQUARE_SIZE], [SUDOKU_BOARD_WIDTH, k * SQUARE_SIZE], LINE_WIDTH)
        # draw vertical lines
        for j in range(N + 1):
            game.draw.line(sudoku_board, BLACK, [j * SQUARE_SIZE, 0], [j * SQUARE_SIZE, SUDOKU_BOARD_HEIGHT],
                           LINE_WIDTH)
        
        print_sudoku_board(sudoku_board, sudoku_matrix, sudoku_matrix_ref, GRAY, correct_wrong, lst)
        key = game.key.get_pressed()
        
        for event in game.event.get():
            if event.type == game.KEYUP:
                key_released = False
        
        if game.mouse.get_pressed()[0]:
            y, x = game.mouse.get_pos()
            if x < SUDOKU_BOARD_HEIGHT:
                square_pos[0] = x
                square_pos[1] = y
                square_pos_index[0] = (square_pos[0] - LINE_WIDTH) // SQUARE_SIZE
                square_pos_index[1] = (square_pos[1] - LINE_WIDTH) // SQUARE_SIZE
                square_pos[1] = square_pos_index[0] * SQUARE_SIZE + LINE_WIDTH
                square_pos[0] = square_pos_index[1] * SQUARE_SIZE + LINE_WIDTH
                
                if square_pos[0] >= SUDOKU_BOARD_WIDTH:
                    square_pos[0] = SUDOKU_BOARD_WIDTH - SQUARE_SIZE
                
                if square_pos[1] >= SUDOKU_BOARD_HEIGHT:
                    square_pos[1] = SUDOKU_BOARD_HEIGHT - SQUARE_SIZE
        
        if key[game.K_1]:
            number = 1
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_2]:
            number = 2
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_3]:
            number = 3
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_4]:
            number = 4
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_5]:
            number = 5
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
        elif key[game.K_6]:
            number = 6
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_7]:
            number = 7
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_8]:
            number = 8
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_9]:
            number = 9
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, number, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        elif key[game.K_DELETE]:
            sudoku_matrix = set_number_to_sudoku_board(sudoku_matrix, sudoku_matrix_ref, 0, square_pos_index)
            ind = lst.index([square_pos_index[0], square_pos_index[1]])
            correct_wrong[ind] = 0
        
        if key[game.K_SPACE] and not solve_iter:
            sudoku_matrix = copy.deepcopy(sudoku_matrix_ref)
            sudoku_matrix, total_sol_trial, step_value = sudoku_solver.get_sudoku_sol(sudoku_matrix, N)
            correct_wrong = [1] * len(correct_wrong)
        if key[game.K_BACKSPACE]:
            sudoku_matrix = copy.deepcopy(sudoku_matrix_ref)
            solved = False
            correct_wrong = [0] * len(correct_wrong)
            solve_iter = False
            start_time = game.time.get_ticks()
        
        if key[game.K_c] and not key_released and not solve_iter:
            key_released = True
            for ind, val in enumerate(lst):
                k = val[0]
                j = val[1]
                if sudoku_matrix[k][j] == sudoku_matrix_sol[k][j]:
                    correct_wrong[ind] = 1
                else:
                    correct_wrong[ind] = 0
        
        if key[game.K_KP_ENTER] and not solved:
            sudoku_matrix = copy.deepcopy(sudoku_matrix_ref)
            solve_iter = True
            total_sol_trial = 0
            sol_step = 0
            step_value = []
        
        if solve_iter:
            sudoku_matrix, total_sol_trial, step_value, total_sol_trial, sol_step, step_value, lst, completed \
                = sudoku_solver.get_sudoku_sol_iter(sudoku_matrix, total_sol_trial, sol_step, step_value, lst)
            for ind, val in enumerate(lst):
                k = val[0]
                j = val[1]
                if sudoku_matrix[k][j] == sudoku_matrix_sol[k][j]:
                    correct_wrong[ind] = 1
                else:
                    correct_wrong[ind] = 0
            if completed:
                solved = True
                solve_iter = False
        if key[game.K_ESCAPE]:
            game.quit()
            quit()
        
        game.draw.rect(sudoku_board, BLUE,
                       (square_pos[0], square_pos[1], SQUARE_SIZE - LINE_WIDTH, SQUARE_SIZE - LINE_WIDTH), LINE_WIDTH)

        print_time(sudoku_board, lasting_time, [SUDOKU_BOARD_WIDTH-50, SUDOKU_BOARD_HEIGHT+50],RED)
        game.display.update()
        clock.tick(100)


if __name__ == '__main__':
    main()
