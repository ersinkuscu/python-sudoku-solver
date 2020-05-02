# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:20:44 2020

@author: ersinkuscu
"""

from matplotlib import pyplot as plt
import numpy as np
import sudoku.solver as sudoku_solver


def main():
    # main initials
    N = 9
    sudoku_matrix = [[0, 0, 0, 0, 0, 4, 0, 9, 0],
                     [8, 0, 2, 9, 7, 0, 0, 0, 0],
                     [9, 0, 1, 2, 0, 0, 3, 0, 0],
                     [0, 0, 0, 0, 4, 9, 1, 5, 7],
                     [0, 1, 3, 0, 5, 0, 9, 2, 0],
                     [5, 7, 9, 1, 2, 0, 0, 0, 0],
                     [0, 0, 7, 0, 0, 2, 6, 0, 3],
                     [0, 0, 0, 0, 3, 8, 2, 0, 5],
                     [0, 2, 0, 5, 0, 0, 0, 0, 0]]

    # get solution for the sudoku matrix
    sudoku_matrix, total_sol_trial, step_value = sudoku_solver.get_sudoku_sol(sudoku_matrix, N)

    # print solution of the sudoku game
    sudoku_solver.print_matrix(sudoku_matrix)

    # print number of trials made to get the solution
    print('Total Solution Trial : {}'.format(total_sol_trial))

    # plot the change of depth with respect to trials
    plt.plot(np.array(step_value), 'r', linewidth=3)
    plt.grid()
    plt.show()
    plt.xlabel('Trials')
    plt.ylabel('Solution Depth')
    plt.axis('tight')


if __name__ == '__main__':
    main()
