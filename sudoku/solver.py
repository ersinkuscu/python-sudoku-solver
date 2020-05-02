# print matrix as rows and columns
def print_matrix(M):
    n = len(M)
    for k in range(n):
        for j in range(n):
            print(M[k][j], end=' ')
        print('\n')
    print('\n\n')


# check the current sudoku board
# whether it is correctly filled according to rules or not
def check_solution(s, k, j):
    # initials
    lst = []
    N = 9
    n = 3

    # first check 3x3 matrix
    r = int(k / n)
    c = int(j / n)
    for t in range(n):
        for y in range(n):
            lst.append(s[n * r + t][n * c + y])
    for x in range(1, N+1):
        if lst.count(x) > 1:
            return False
    lst = []

    # second check rows
    for y in range(N):
        lst.append(s[k][y])
    for x in range(1, N + 1):
        if lst.count(x) > 1:
            return False
    lst = []

    # third check columns
    for y in range(N):
        lst.append(s[y][j])
    for x in range(1, N + 1):
        if lst.count(x) > 1:
            return False
    return True


def check_entire_sudoku_matrix(s):
    # initials
    lst = []
    N = 9
    n = 3
    
    # first check 3x3 matrix
    for r in range(n):
        for c in range(n):
            for t in range(n):
                for y in range(n):
                    lst.append(s[n * r + t][n * c + y])
            for x in range(1, N + 1):
                if lst.count(x) > 1:
                    return False
            lst = []
    
    # second check rows
    for k in range(N):
        for y in range(N):
            lst.append(s[k][y])
        for x in range(1, N + 1):
            if lst.count(x) > 1:
                return False
        lst = []
    
    # third check columns
    for j in range(N):
        for y in range(N):
            lst.append(s[y][j])
        for x in range(1, N + 1):
            if lst.count(x) > 1:
                return False
        lst = []
    return True


# get empty set in sudoku matrix
def get_empty_list(sudoku_matrix, N):
    lst = []
    for row in range(N):
        for col in range(N):
            if sudoku_matrix[row][col] == 0:
                lst.append([row, col])
    return lst


# backtracking algorithm complete solution
def get_sudoku_sol(sudoku_matrix, N):
    lst = get_empty_list(sudoku_matrix, N)
    
    # initials
    total_sol_trial = 0
    sol_step = 0
    run = True
    step_value = []

    # running until finding a solution
    while run:
        # select row and column index from our list
        k_row = lst[sol_step][0]
        j_col = lst[sol_step][1]

        # increase the number by one
        # if it is greater than 9 than go to the upper node
        # and increase it by one again
        # do this until
        # you get a node value which is not greater than 9
        sudoku_matrix[k_row][j_col] += 1
        while sudoku_matrix[k_row][j_col] == 9 + 1:
            sudoku_matrix[k_row][j_col] = 0
            sol_step -= 1
            k_row = lst[sol_step][0]
            j_col = lst[sol_step][1]
            sudoku_matrix[k_row][j_col] += 1

        # check the solution obtain at each iteration
        # if it is correct, go down the next node
        if check_solution(sudoku_matrix, k_row, j_col):
            sol_step += 1

        # check the condition where the solution is obtained
        # and no need for further iteration
        if sol_step >= len(lst):
            run = False

        # increase the trial number by one and store it
        total_sol_trial = total_sol_trial + 1
        step_value.append(sol_step)
    return sudoku_matrix, total_sol_trial, step_value


# backtracking algorithm iterative solution
def get_sudoku_sol_iter(sudoku_matrix, total_sol_trial, sol_step, step_value, lst):
    # initals
    completed = False
    
    # running until finding a solution
    # select row and column index from our list
    k_row = lst[sol_step][0]
    j_col = lst[sol_step][1]
    
    # increase the number by one
    # if it is greater than 9 than go to the upper node
    # and increase it by one again
    # do this until
    # you get a node value which is not greater than 9
    sudoku_matrix[k_row][j_col] += 1
    while sudoku_matrix[k_row][j_col] == 9 + 1:
        sudoku_matrix[k_row][j_col] = 0
        sol_step -= 1
        k_row = lst[sol_step][0]
        j_col = lst[sol_step][1]
        sudoku_matrix[k_row][j_col] += 1
    
    # check the solution obtain at each iteration
    # if it is correct, go down the next node
    if check_solution(sudoku_matrix, k_row, j_col):
        sol_step += 1
    
    # check the condition where the solution is obtained
    # and no need for further iteration
    if sol_step >= len(lst):
        completed = True
    
    # increase the trial number by one and store it
    total_sol_trial = total_sol_trial + 1
    step_value.append(sol_step)
    return sudoku_matrix, total_sol_trial, step_value, total_sol_trial, sol_step, step_value, lst, completed
