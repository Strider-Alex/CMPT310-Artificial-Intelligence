"""
Lights Out Puzzle
"""
import random
import copy
import math
import timeit
import numpy as np

""" global var """
move_count = 0

def create_puzzle(rows, cols):
    """ create a new puzzle and set all OFF """
    puzzle = [[0 for x in range(cols)] for x in range(rows)]
    return puzzle

def perform_move(puzzle, row, col):
    """ Toggle the cell and adjacent cells """
    global move_count
    move_count+=1
    steps = ((0, 0), (0, 1), (0, -1), (1, 0),(-1, 0))
    for step in steps:
        new_row = row+step[0]
        new_col = col+step[1]
        if new_row>=0 and new_row<len(puzzle) and new_col>=0 and new_col<len(puzzle[0]):
            puzzle[new_row][new_col]^=1
    return puzzle

def scramble(puzzle):
    """ Initialize the puzzle """
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if(random.random()>0.5):
                perform_move(puzzle,i,j)
    return puzzle

def is_solved(puzzle):
    """ Check if the puzzle has been solved """
    for row in puzzle:
        for item in row:
            if item==1:
                return False
    return True

def next_cell(rows, cols, row, col):
    """ Get the coordinates of the next cell """
    if(col+1<cols):
        col+=1
    else:
        col=0
        row+=1
    if(row>=rows):
        row=0
    return row,col

def solve_puzzle_smart_size5(puzzle):
    puzzle = copy.deepcopy(puzzle)
    solution = set()
    for i in range(len(puzzle)-1):
        for j in range(len(puzzle[0])):
            if puzzle[i][j]:
                perform_move(puzzle,i+1,j)
                solution.add((i+1,j))
    if puzzle[len(puzzle)-1]==[0,0,0,0,0]:
        return solution
    conditions = {(1,1,1,0,0):(1,),(1,1,0,1,1):(2,),(1,0,1,1,0):(4,),(1,0,0,0,1):(0,1),(0,1,1,0,1):(0,),(0,1,0,1,0):(0,3),(0,0,1,1,1):(3,)}
    condition = conditions[tuple(puzzle[len(puzzle)-1])]
    for i in condition:
        perform_move(puzzle,0,i)
        solution.add((0,i))
    for i in range(len(puzzle)-1):
        for j in range(len(puzzle[0])):
            if puzzle[i][j]:
                perform_move(puzzle,i+1,j)
                solution.add((i+1,j))
    return solution


def solve_puzzle_smart_general(the_puzzle):
    size = len(the_puzzle)
    for it in range(2**size):
        puzzle = copy.deepcopy(the_puzzle)
        solution = set()
        toggle_list = [int(x) for x in bin(it)[2:].zfill(size)]
        for i in range(len(toggle_list)):
            if toggle_list[i]==1:
                perform_move(puzzle,0,i)
                solution.add((0,i))
        for i in range(len(puzzle)-1):
            for j in range(len(puzzle[0])):
                if puzzle[i][j]:
                    perform_move(puzzle,i+1,j)
                    solution.add((i+1,j))
        if puzzle[len(puzzle)-1]==[0 for i in range(size)]:
            return solution
    return {}

iter = 100
puzzles=[]
for i in range(iter):
    puzzles.append(create_puzzle(5, 5))
    scramble(puzzles[i])

print("5*5 Chasing the Light Test:")
time_sum = 0
solution_sum=0
move_count=0
start = timeit.default_timer()
for i in range(iter):
    solution_sum+=len(solve_puzzle_smart_size5(puzzles[i]))
end = timeit.default_timer()
print("total time: "+str(end-start)+" sec")
print("total solution length: "+str(solution_sum))
print("total steps: "+str(move_count))

iter = 100
puzzles=[]
for i in range(iter):
    puzzles.append(create_puzzle(8, 8))
    scramble(puzzles[i])

print("General(8*8) Chasing the Light Test:")
time_sum = 0
solution_sum=0
move_count=0
start = timeit.default_timer()
for i in range(iter):
    solution_sum+=len(solve_puzzle_smart_general(puzzles[i]))
end = timeit.default_timer()
print("total time: "+str(end-start)+" sec")
print("total solution length: "+str(solution_sum))
print("total steps: "+str(move_count))




