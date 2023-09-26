# -*- coding = utf-8 -*-
# @Time : 2023-9-26 16:22
# @Author : Lurume
# @File : my_test.py
# @Software : PyCharm
import sudoku
count = 0
def solve_sudoku(grid):
    # 寻找空格的位置
    global count
    count += 1
    row, col = find_empty_cell(grid)

    # 如果没有找到空格，说明数独已经解决
    if row == -1 and col == -1:
        return 1

    # 尝试填入数字
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            # 递归解决剩余的空格
            if solve_sudoku(grid):
                return 1

            # 如果递归未能解决数独，回溯并尝试下一个数字
            grid[row][col] = 0

    # 所有数字都尝试过了，无解
    return 0


def find_empty_cell(grid):
    # 寻找数值为0的空格
    for i in range(9):
        for j in range(9):
            if grid[i][j] == " ":
                return i, j
    return -1, -1


def is_valid(grid, row, col, num):
    # 检查所在行是否合法
    for i in range(9):
        if grid[i][col] == num:
            return False

    # 检查所在列是否合法
    for j in range(9):
        if grid[row][j] == num:
            return False

    # 检查所在3x3子网格是否合法
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

if __name__ == '__main__':
    sum = 0
    for i in range(100):
        problem, answer = sudoku.generate_sudoku_task("hard")
        solve_sudoku(problem)
        sum += count
        count = 0
    print("hard平均递归次数为：", sum/100)
    sum = 0
    for i in range(100):
        problem, answer = sudoku.generate_sudoku_task("medium")
        solve_sudoku(problem)
        sum += count
        count = 0
    print("medium平均递归次数为：", sum/100)
    sum = 0
    for i in range(100):
        problem, answer = sudoku.generate_sudoku_task("easy")
        solve_sudoku(problem)
        sum += count
        count = 0
    print("easy平均递归次数为：", sum / 100)