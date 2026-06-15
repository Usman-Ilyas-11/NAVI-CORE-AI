import tkinter as tk
import time
from algorithms import bfs, dfs, astar
from maze import generate_maze
from ml_model import train_model, predict

CELL_SIZE = 25


class MazeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Intelligent Maze & Pathfinding Studio")
        self.root.state("zoomed")

        # ===== ML MODEL =====
        self.model = train_model()
        self.rows = 20
        self.cols = 20
        self.mode = "wall"

        self.bg_dark = "#0f172a"
        self.bg_light = "#1e293b"
        self.btn_color = "#2563eb"
        self.btn_hover = "#3b82f6"

        self.left_panel = tk.Frame(self.root, bg=self.bg_dark, width=230)
        self.left_panel.pack(side="left", fill="y")

        self.right_panel = tk.Frame(self.root, bg=self.bg_light, width=230)
        self.right_panel.pack(side="right", fill="y")

        self.center_panel = tk.Frame(self.root, bg="white")
        self.center_panel.pack(expand=True)

        tk.Label(
            self.center_panel,
            text="Intelligent Maze & Pathfinding Studio",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            pady=10
        ).pack()

        self.canvas = tk.Canvas(
            self.center_panel,
            width=self.cols * CELL_SIZE,
            height=self.rows * CELL_SIZE,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.draw_wall)
        self.canvas.bind("<Button-1>", self.set_point)
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)
        self.create_buttons()
        self.create_size_inputs()
        self.create_stats()
        self.draw_grid()

    def styled_button(self, text, cmd):
        btn = tk.Button(
            self.left_panel,
            text=text,
            command=cmd,
            width=22,
            bg=self.btn_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.btn_hover,
            activeforeground="white"
        )

        btn.bind("<Enter>", lambda e: btn.config(bg=self.btn_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_color))

        return btn

    def create_stats(self):
        tk.Label(
            self.right_panel,
            text="Statistics",
            fg="white",
            bg=self.bg_light,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

        self.stats = tk.Label(
            self.right_panel,
            text="Nodes: 0\nTime: 0s",
            fg="white",
            bg=self.bg_light,
            font=("Segoe UI", 12)
        )
        self.stats.pack()

    def create_buttons(self):
        tk.Label(
            self.left_panel,
            text="Controls",
            bg=self.bg_dark,
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.styled_button("Generate Maze", self.generate).pack(pady=4)
        self.styled_button("Run BFS", self.run_bfs).pack(pady=4)
        self.styled_button("Run DFS", self.run_dfs).pack(pady=4)
        self.styled_button("Run A*", self.run_astar).pack(pady=4)
        #self.styled_button("Back", self.go_back).pack(pady=4)
        tk.Label(self.left_panel, bg=self.bg_dark).pack(pady=12)

        self.styled_button("Compare All", self.compare_all).pack(pady=4)
        self.styled_button("Predict Best", self.predict_best).pack(pady=4)

        tk.Label(self.left_panel, bg=self.bg_dark).pack(pady=12)
        self.styled_button("Back to Dashboard", self.go_back).pack(pady=4)

    def go_back(self):
        self.root.destroy()
        from main import Dashboard
        Dashboard().root.mainloop()

    def create_size_inputs(self):
        tk.Label(self.left_panel, text="Rows", bg=self.bg_dark, fg="white").pack()
        self.row_entry = tk.Entry(self.left_panel)
        self.row_entry.pack(pady=2)

        tk.Label(self.left_panel, text="Cols", bg=self.bg_dark, fg="white").pack()
        self.col_entry = tk.Entry(self.left_panel)
        self.col_entry.pack(pady=2)

        self.styled_button("Set Size", self.set_size).pack(pady=5)

        self.styled_button("Make Wall", lambda: self.set_mode("wall")).pack(pady=2)
        self.styled_button("Set Start", lambda: self.set_mode("start")).pack(pady=2)
        self.styled_button("Set End", lambda: self.set_mode("end")).pack(pady=2)

    def set_mode(self, mode):
        self.mode = mode

    def set_size(self):
        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())

            self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            self.canvas.config(
                width=self.cols * CELL_SIZE,
                height=self.rows * CELL_SIZE
            )

            self.start = (0, 0)
            self.end = (self.rows - 1, self.cols - 1)

            self.draw_grid()
        except:
            self.stats.config(text="Invalid size")

    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"

                if self.grid[r][c] == 1:
                    color = "#111111"
                if (r, c) == self.start:
                    color = "#22c55e"
                if (r, c) == self.end:
                    color = "#ef4444"

                self.canvas.create_rectangle(
                    c * CELL_SIZE, r * CELL_SIZE,
                    (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                    fill=color, outline="#d1d5db"
                )

    def draw_wall(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.mode == "wall":
                if (r, c) != self.start and (r, c) != self.end:
                    self.grid[r][c] = 1
            self.draw_grid()

    def set_point(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.mode == "start":
                self.start = (r, c)
            elif self.mode == "end":
                self.end = (r, c)
            self.draw_grid()

    def generate(self):
        self.grid = generate_maze(self.rows, self.cols)
        self.draw_grid()

    def run_bfs(self):
        self.run_algorithm(bfs, "#3b82f6")

    def run_dfs(self):
        self.run_algorithm(dfs, "#a855f7")

    def run_astar(self):
        self.run_algorithm(astar, "#f59e0b")

    def run_algorithm(self, algo, color):
        self.draw_grid()

        start_time = time.time()
        path, visited = algo(self.grid, self.start, self.end)
        end_time = time.time()

        if not path:
            self.stats.config(text="❌ No path exists (all paths blocked)")
            return

        for (r, c) in visited:
            self.canvas.create_rectangle(
                c * CELL_SIZE, r * CELL_SIZE,
                (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                fill="#e5e7eb"
            )
            self.root.update()
            self.root.after(1)

        for (r, c) in path:
            self.canvas.create_rectangle(
                c * CELL_SIZE, r * CELL_SIZE,
                (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                fill=color
            )
            self.root.update()
            self.root.after(10)

        self.stats.config(
            text=f"Nodes: {len(visited)}\nTime: {round(end_time-start_time,4)}s"
        )

    #(LINE GRAPH & BETTER TIMING)
    def compare_all(self):
        import matplotlib.pyplot as plt
        import time

        names = []
        times = []

        for name, algo in [("BFS", bfs), ("DFS", dfs), ("A*", astar)]:
            start = time.perf_counter()
            algo(self.grid, self.start, self.end)
            end = time.perf_counter()

            names.append(name)
            times.append(end - start)

        plt.figure()
        plt.plot(names, times, marker='o')
        plt.title("Algorithm Time Comparison")
        plt.xlabel("Algorithms")
        plt.ylabel("Time (seconds)")
        plt.grid()
        plt.show()

    def predict_best(self):
        import matplotlib.pyplot as plt

        total = self.rows * self.cols
        walls = sum(cell for row in self.grid for cell in row)
        density = walls / total
        size = total

        ml_prediction = predict(self.model, size, density)

        results = {}
        nodes = {}

        for name, algo in [("BFS", bfs), ("DFS", dfs), ("A*", astar)]:
            start = time.time()
            path, visited = algo(self.grid, self.start, self.end)
            end = time.time()

            results[name] = end - start
            nodes[name] = len(visited)

        actual_best = min(nodes, key=nodes.get)

        win = tk.Toplevel(self.root)
        win.title("AI Analysis")
        win.geometry("650x450")

        text = f"""
AI MODEL PREDICTION: {ml_prediction}
ACTUAL BEST: {actual_best}

BFS  → Time: {results['BFS']:.4f}s | Nodes: {nodes['BFS']}
DFS  → Time: {results['DFS']:.4f}s | Nodes: {nodes['DFS']}
A*   → Time: {results['A*']:.4f}s | Nodes: {nodes['A*']}
"""

        tk.Label(
            win,
            text=text,
            font=("Times New Roman", 13, "bold"),
            justify="left"
        ).pack(pady=20)

        plt.bar(results.keys(), results.values())
        plt.title("Time Comparison")
        plt.show()

    def run(self):
        self.root.mainloop()