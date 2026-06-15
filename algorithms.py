from collections import deque
import heapq

# ================= NEIGHBORS =================
def get_neighbors(node, grid):
    r, c = node
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

# ================= PATH RECONSTRUCTION =================
def reconstruct_path(parent, start, end):
    path = []
    node = end

    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []

    path.append(start)
    path.reverse()
    return path


# ================= BFS =================
def bfs(grid, start, end):
    queue = deque([start])
    visited = set([start])
    parent = {}
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)

        if node == end:
            break

        for n in get_neighbors(node, grid):
            r, c = n

            if n not in visited and grid[r][c] == 0:
                visited.add(n)
                parent[n] = node
                queue.append(n)

    path = reconstruct_path(parent, start, end)
    return path, order


# ================= DFS =================
def dfs(grid, start, end):
    stack = [start]
    visited = set([start])
    parent = {}
    order = []

    while stack:
        node = stack.pop()
        order.append(node)

        if node == end:
            break

        for n in get_neighbors(node, grid):
            r, c = n

            if n not in visited and grid[r][c] == 0:
                visited.add(n)
                parent[n] = node
                stack.append(n)

    path = reconstruct_path(parent, start, end)
    return path, order

# ================= HEURISTIC =================
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
# ================= A* =================
def astar(grid, start, end):
    pq = []
    heapq.heappush(pq, (0, start))
    parent = {}
    cost = {start: 0}
    visited = set()
    order = []
    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        if node == end:
            break
        for n in get_neighbors(node, grid):
            r, c = n
            if grid[r][c] == 1:
                continue
            new_cost = cost[node] + 1
            if n not in cost or new_cost < cost[n]:
                cost[n] = new_cost
                priority = new_cost + heuristic(n, end)
                heapq.heappush(pq, (priority, n))
                parent[n] = node
    path = reconstruct_path(parent, start, end)
    return path, order