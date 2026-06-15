import random

def generate_maze(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if random.random() < 0.3:
                grid[r][c] = 1

    grid[0][0] = 0
    grid[rows-1][cols-1] = 0

    return grid