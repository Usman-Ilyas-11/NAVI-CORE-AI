from sklearn.tree import DecisionTreeClassifier
import random
from algorithms import bfs, dfs, astar

def generate_grid(rows, cols, density):
    import random
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < density:
                grid[r][c] = 1
    grid[0][0] = 0
    grid[rows - 1][cols - 1] = 0
    return grid

def train_model():
    X = []
    y = []
    for _ in range(100):  # training samples
        rows = random.randint(10, 30)
        cols = random.randint(10, 30)
        density = random.uniform(0.0, 0.6)
        grid = generate_grid(rows, cols, density)
        start = (0, 0)
        end = (rows - 1, cols - 1)
        results = {}
        for name, algo in [("BFS", bfs), ("DFS", dfs), ("A*", astar)]:
            try:
                path, visited = algo(grid, start, end)
                results[name] = len(visited)
            except:
                results[name] = float("inf")
        best = min(results, key=results.get)
        X.append([rows * cols, density])
        y.append(best)
    model = DecisionTreeClassifier()
    model.fit(X, y)

    return model


def predict(model, size, density):
    return model.predict([[size, density]])[0]