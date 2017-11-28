"""
Lights Out Puzzle
Kefan Yang
kefany@sfu.ca
"""
import random
import copy
import math
import timeit

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

def solve_puzzle_dfs_rec(puzzle, row, col, solution):
    puzzle = copy.deepcopy(puzzle)
    solution = copy.deepcopy(solution)
    perform_move(puzzle,row,col)
    if is_solved(puzzle):
        return solution
    row,col = next_cell(len(puzzle),len(puzzle[0]),row,col)
    while row!=0 or col!=0:
        ret = solve_puzzle_dfs_rec(puzzle,row,col,solution+[(row,col)])
        if ret:
            return ret
        row,col = next_cell(len(puzzle),len(puzzle[0]),row,col)
    return []

def solve_puzzle_dfs(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            ret = solve_puzzle_dfs_rec(puzzle,i,j,[(i,j)])
            if ret:
                return ret
    return []

def solve_puzzle_bfs(puzzle):
    row=col=0
    map_queue = [copy.deepcopy(puzzle)]
    solution_queue = [[]]
    while solution_queue:
        solution = solution_queue.pop(0)
        new_map = map_queue.pop(0)
        if is_solved(new_map):
            return solution
        if solution:
            row,col = solution[len(solution)-1]
            imax = len(puzzle)*len(puzzle[0])-len(puzzle[0])*row-col-1
        else:
            imax = len(puzzle)*len(puzzle[0])
            row = len(puzzle)-1
            col = len(puzzle[0])-1
        for i in range(imax):
            row,col = next_cell(len(puzzle),len(puzzle[0]),row,col)
            map_queue.append(perform_move(copy.deepcopy(new_map),row,col))
            solution_queue.append(solution+[(row,col)])

def heuristic(puzzle, row, col, on_count):
    """ calculate the heuristic function """
    steps = ((0, 0), (0, 1), (0, -1), (1, 0),(-1, 0))
    for step in steps:
        new_row = row+step[0]
        new_col = col+step[1]
        if new_row>=0 and new_row<len(puzzle) and new_col>=0 and new_col<len(puzzle[0]):
            if puzzle[new_row][new_col]==1:
                on_count-=1
            else:
                on_count+=1
    return on_count/5

def evaluate(puzzle,base):
    on_count = 0
    for row in puzzle:
        for item in row:
            if item==1:
                on_count+=1
    return [[heuristic(puzzle,i,j,on_count)+base for j in range(len(puzzle[0]))] for i in range(len(puzzle))]

def solve_puzzle_astar(puzzle):
    if is_solved(puzzle):
        return []
    puzzle = copy.deepcopy(puzzle)
    solution_set = [[]]
    chosen_set = [[]]
    map_set = [puzzle]
    evaluation_set = [evaluate(puzzle,0)]
    while True:
        min_eval = math.inf
        mink=mini=minj=-1
        for k in range(len(evaluation_set)):
            for i in range(len(puzzle)):
                for j in range(len(puzzle[0])):
                    if (i,j) in chosen_set[k]:
                        continue
                    if evaluation_set[k][i][j]<min_eval:
                        min_eval = evaluation_set[k][i][j]
                        mini=i
                        minj=j
                        mink=k
        new_map = copy.deepcopy(map_set[mink])
        perform_move(new_map,mini,minj)
        if is_solved(new_map):
            return solution_set[mink]+[(mini,minj)]
        chosen_set[mink].append((mini,minj))
        solution_set.append(solution_set[mink]+[(mini,minj)])
        #chosen_set.append(solution_set[mink]+[(mini,minj)])
        new_chosen = copy.deepcopy(chosen_set[mink])
        chosen_set.append(new_chosen)
        evaluation_set.append(evaluate(new_map,len(solution_set[mink])+1))
        map_set.append(new_map)

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

iter = 100
puzzles=[]
for i in range(iter):
    puzzles.append(create_puzzle(4, 4))
    scramble(puzzles[i])

# print("Chasing the Light Test:")
# time_sum = 0
# solution_sum=0
# move_count=0
# start = timeit.default_timer()
# for i in range(iter):
#     solution_sum+=len(solve_puzzle_smart_size5(puzzles[i]))
# end = timeit.default_timer()
# print("total time: "+str(end-start)+" sec")
# print("total solution length: "+str(solution_sum))
# print("total steps: "+str(move_count))


print("DFS Test:")
time_sum = 0
solution_sum=0
move_count=0
start = timeit.default_timer()
for i in range(iter):
    solution_sum+=len(solve_puzzle_dfs(puzzles[i]))
end = timeit.default_timer()
print("total time: "+str(end-start)+" sec")
print("total solution length: "+str(solution_sum))
print("total steps: "+str(move_count))

print("BFS Test:")
time_sum = 0
solution_sum=0
move_count=0
start = timeit.default_timer()
for i in range(iter):
    solution_sum+=len(solve_puzzle_bfs(puzzles[i]))
end = timeit.default_timer()
print("total time: "+str(end-start)+" sec")
print("total solution length: "+str(solution_sum))
print("total steps: "+str(move_count))

print("AStar Test:")
time_sum = 0
solution_sum=0
move_count=0
start = timeit.default_timer()
for i in range(iter):
    solution_sum+=len(solve_puzzle_astar(puzzles[i]))
end = timeit.default_timer()
print("total time: "+str(end-start)+" sec")
print("total solution length: "+str(solution_sum))
print("total steps: "+str(move_count))

