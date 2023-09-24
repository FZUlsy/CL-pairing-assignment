# -*- coding = utf-8 -*-
# @Time : 2023-9-17 16:19
# @Author : Lurume
# @File : jiugong.py
# @Software : PyCharm
from flask import jsonify
import random
from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.debug = True
# Flask路由，渲染前端页面
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_sudoku', methods=['POST'])
def generate_sudoku():
    data = request.get_json()
    difficulty = data.get('difficulty', 'easy')
    count = data.get('count', 1)
    count = int(count)

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(generate_sudoku_task, difficulty) for _ in range(count)]

    sudokus = []
    answers = []

    for result in results:
        sudoku, answer = result.result()
        sudokus.append(sudoku)
        answers.append(answer)

    return jsonify({'sudokus': sudokus, 'answers': answers})

def generate_sudoku_task(difficulty):
    # 创建一个空的9x9数独网格
    grid = [[0 for _ in range(9)] for _ in range(9)]

    # 填充对角线上的3x3子网格
    for i in range(0, 9, 3):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = nums.pop()

    # 使用回溯法填充剩余的空格
    solve_sudoku(grid)

    # 随机移除一些数字作为题目
    if difficulty == 'easy':
        remove_count = random.randint(30, 40)
    elif difficulty == 'medium':
        remove_count = random.randint(40, 50)
    elif difficulty == 'hard':
        remove_count = random.randint(50, 60)
    elif difficulty == 'expert':
        remove_count = random.randint(60, 70)
    else:
        remove_count = random.randint(30, 50)

    # 创建一个空的9x9数独网格用于答案
    answer = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            answer[i][j] = grid[i][j]
    for _ in range(remove_count):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    return grid, answer


def solve_sudoku(grid):
    # 寻找空格的位置
    row, col = find_empty_cell(grid)

    # 如果没有找到空格，说明数独已经解决
    if row == -1 and col == -1:
        return True

    # 尝试填入数字
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            # 递归解决剩余的空格
            if solve_sudoku(grid):
                return True

            # 如果递归未能解决数独，回溯并尝试下一个数字
            grid[row][col] = 0

    # 所有数字都尝试过了，无解
    return False


def find_empty_cell(grid):
    # 寻找数值为0的空格
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
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
    app.run()

# # 交互式接口
# print("欢迎来到数独生成器！")
# difficulty = input("请选择数独的难度（easy/medium/hard/expert）：")
# count = int(input("请输入要生成的数独题目数量："))
#
# # 并行生成数独题目
# with ThreadPoolExecutor() as executor:
#     results = [executor.submit(generate_sudoku, difficulty) for _ in range(count)]
#
# # 打印生成的数独题目
# for i, result in enumerate(results):
#     sudoku = result.result()
#     print(f"数独题目 {i + 1}:")
#     for row in sudoku:
#         print(' '.join(map(str, row)))
#     print()