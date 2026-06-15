import tkinter as tk
import networkx as nx
from collections import deque
import heapq
import time
from ml_model import train_model, predict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk   

class MapApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Map Path Finder")
        self.root.state("zoomed")

        self.bg_img = Image.open("d3.png")
        self.bg_img = self.bg_img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # THEME
        self.bg_main = "#3B7597"
        self.bg_dark = "#093C5D"
        self.accent = "#6FD1D7"
        self.root.configure(bg=self.bg_main)
        self.model = train_model()
        self.graph = nx.Graph()
        self.blocked_nodes = set()
        self.create_country_selector()

    def btn(self, parent, text, cmd):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=self.bg_dark, fg="white",
                      font=("Segoe UI", 11, "bold"),
                      relief="flat", cursor="hand2")
        b.pack(pady=6, fill="x")

        b.bind("<Enter>", lambda e: b.config(bg=self.accent))
        b.bind("<Leave>", lambda e: b.config(bg=self.bg_dark))

    def create_country_selector(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        tk.Label(self.root, text="Select Country Map",
                 font=("Segoe UI", 24, "bold"),
                 bg=self.bg_main, fg="white").pack(pady=50)

        self.btn(self.root, "USA", lambda: self.load_map("usa"))
        self.btn(self.root, "Pakistan", lambda: self.load_map("pakistan"))
        self.btn(self.root, "India", lambda: self.load_map("india"))

    def load_map(self, country):
        self.graph.clear()
        self.blocked_nodes.clear()

        if country == "usa":
            edges = [
                ("New York","Chicago",8),("Chicago","Denver",10),
                ("Denver","San Francisco",6),("New York","Atlanta",6),
                ("Atlanta","Dallas",7),("Dallas","Houston",3),
                ("Houston","Miami",5),("Miami","Atlanta",4),
                ("Seattle","Denver",9),("Seattle","San Francisco",4),
                ("Las Vegas","Denver",5),("Las Vegas","LA",3),
                ("LA","San Francisco",4),("Boston","New York",2),
                ("Detroit","Chicago",3),

                ("Chicago","Dallas",6),
                ("Atlanta","Houston",4),
                ("Denver","LA",5),
                ("Miami","Dallas",6)
            ]

        elif country == "pakistan":
            edges = [
                ("Karachi","Hyderabad",2),("Hyderabad","Sukkur",4),
                ("Sukkur","Multan",6),("Multan","Lahore",4),
                ("Lahore","Islamabad",3),("Islamabad","Peshawar",2),
                ("Quetta","Sukkur",5),("Quetta","Gwadar",6),
                ("Gwadar","Karachi",7),("Faisalabad","Lahore",2),
                ("Sialkot","Lahore",2),("Bahawalpur","Multan",3),
                ("DI Khan","Peshawar",4),("Chaman","Quetta",3),
                ("Gilgit","Islamabad",8),

                ("Karachi","Quetta",7),
                ("Multan","Faisalabad",3),
                ("Hyderabad","Quetta",6),
                ("Islamabad","DI Khan",3)
            ]

        elif country == "india":
            edges = [
                ("Delhi","Jaipur",4),("Delhi","Lucknow",5),
                ("Lucknow","Patna",4),("Patna","Kolkata",5),
                ("Delhi","Chandigarh",3),("Chandigarh","Amritsar",2),
                ("Mumbai","Pune",2),("Pune","Hyderabad",5),
                ("Hyderabad","Bangalore",4),("Bangalore","Chennai",3),
                ("Chennai","Kolkata",8),("Mumbai","Ahmedabad",4),
                ("Ahmedabad","Jaipur",5),("Bhopal","Indore",2),
                ("Indore","Mumbai",6),

                ("Delhi","Bhopal",6),
                ("Hyderabad","Chennai",4),
                ("Kolkata","Delhi",7),
                ("Pune","Bangalore",5)
            ]

        self.graph.add_weighted_edges_from(edges)
        self.show_main_ui()

    def show_main_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        left = tk.Frame(self.root, bg=self.bg_dark, width=260)
        left.pack(side="left", fill="y")

        right = tk.Frame(self.root, bg=self.bg_main)
        right.pack(expand=True, fill="both")

        tk.Label(left, text="Start City", bg=self.bg_dark, fg="white").pack(pady=5)
        self.start = tk.Entry(left)
        self.start.pack()

        tk.Label(left, text="End City", bg=self.bg_dark, fg="white").pack(pady=5)
        self.end = tk.Entry(left)
        self.end.pack()

        tk.Label(left, text="Block City", bg=self.bg_dark, fg="white").pack(pady=5)
        self.block = tk.Entry(left)
        self.block.pack()

        self.btn(left, "Block City", self.block_city)
        self.btn(left, "Run BFS", lambda: self.run_algo("bfs"))
        self.btn(left, "Run DFS", lambda: self.run_algo("dfs"))
        self.btn(left, "Run A*", lambda: self.run_algo("astar"))
        self.btn(left, "ML Compare", self.run_ml_screen)
        self.btn(left, "Back", self.back)

        self.output = tk.Label(right, text="", bg=self.bg_main,
                               fg="white", font=("Segoe UI", 11))
        self.output.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(9, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        self.draw_graph(self.graph, [])

    def block_city(self):
        city = self.block.get()
        if city in self.graph.nodes:
            self.blocked_nodes.add(city)
            self.output.config(text=f"Blocked city: {city}")
        else:
            self.output.config(text="City not found")

    def bfs(self, G, start, end):
        q = deque([(start, [start])])
        visited = set()

        while q:
            node, path = q.popleft()
            if node == end:
                return path, len(visited)

            if node not in visited:
                visited.add(node)
                for n in G.neighbors(node):
                    q.append((n, path + [n]))

        return [], float("inf")

    def dfs(self, G, start, end):
        stack = [(start, [start])]
        visited = set()

        while stack:
            node, path = stack.pop()
            if node == end:
                return path, len(visited)

            if node not in visited:
                visited.add(node)
                for n in G.neighbors(node):
                    stack.append((n, path + [n]))
        return [], float("inf")

    def astar(self, G, start, end):
        pq = [(0, start, [start])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)
            if node == end:
                return path, len(visited)

            if node not in visited:
                visited.add(node)
                for n in G.neighbors(node):
                    w = G[node][n]["weight"]
                    heapq.heappush(pq, (cost + w, n, path + [n]))

        return [], float("inf")

    def run_algo(self, t):
        G = self.prepare_graph()
        s, e = self.start.get(), self.end.get()

        if s not in G or e not in G:
            self.output.config(text="Start or End city is blocked!")
            return

        start_time = time.time()

        if t == "bfs":
            path, nodes = self.bfs(G, s, e)
        elif t == "dfs":
            path, nodes = self.dfs(G, s, e)
        else:
            path, nodes = self.astar(G, s, e)

        end_time = time.time()

        if not path:
            self.output.config(text="❌ No Path Found")
            self.draw_graph(G, [])
            return

        self.output.config(
            text=f"{t.upper()} Path: {' → '.join(path)}\nNodes: {nodes}\nTime: {round(end_time-start_time,4)}s"
        )

        self.draw_graph(G, path)

    def run_ml_screen(self):
        G = self.prepare_graph()
        s, e = self.start.get(), self.end.get()

        results = {}
        paths = {}

        for name, func in [("BFS", self.bfs), ("DFS", self.dfs), ("A*", self.astar)]:
            if s not in G or e not in G:
                paths[name] = []
                results[name] = ("Blocked", 0)
                continue

            t1 = time.time()
            path, nodes = func(G, s, e)
            t2 = time.time()

            if not path:
                paths[name] = ["No Path"]
                results[name] = ("∞", 0)
            else:
                paths[name] = path
                results[name] = (nodes, round(t2 - t1, 4))

        size = len(G.nodes)
        density = len(G.edges) / (size * (size - 1))

        ml = predict(self.model, size, density)
        best = min(results, key=lambda x: results[x][0])

        win = tk.Toplevel(self.root)
        win.title("ML Analysis")
        win.geometry("700x500")

        text = f"ML Prediction: {ml}\nActual Best: {best}\n\n"

        for k in results:
            text += f"{k}:\nPath: {' → '.join(paths[k])}\nNodes: {results[k][0]} Time: {results[k][1]}s\n\n"

        tk.Label(win, text=text, justify="left",
                 font=("Segoe UI", 11)).pack(pady=20)

    def draw_graph(self, G, path):
        self.ax.clear()

        pos = self.get_positions(G)

        nx.draw(G, pos, ax=self.ax,
            with_labels=True,
            node_color="#6FD1D7",
            node_size=1000,
            font_size=9)

        if path:
            edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(
                G, pos,
                edgelist=edges,
                edge_color="red",
                width=3,
                ax=self.ax
        )

        self.canvas.draw()

    def prepare_graph(self):
        G = self.graph.copy()
        for node in self.blocked_nodes:
            if node in G:
                G.remove_node(node)
        return G

    def back(self):
        self.root.destroy()
        from main import Dashboard
        Dashboard().root.mainloop()
    
    def get_positions(self, G):
        usa_pos = {
        "Seattle": (0, 4), "San Francisco": (1, 3), "LA": (1, 2),
        "Las Vegas": (2, 2.5), "Denver": (3, 3),
        "Chicago": (5, 4), "Detroit": (6, 4),
        "New York": (8, 4), "Boston": (9, 4),
        "Atlanta": (7, 2), "Miami": (8, 1),
        "Dallas": (5, 1.5), "Houston": (5, 1)
        }

        pakistan_pos = {
    "Gwadar": (0, 0),
    "Karachi": (4, 1),
    "Hyderabad": (6, 2),

    "Quetta": (0, 5),
    "Chaman": (1, 6),

    "Sukkur": (6, 5),
    "Bahawalpur": (9, 5),

    "Multan": (8, 7),
    "Faisalabad": (12, 9),

    "Lahore": (14, 11),
    "Sialkot": (16, 12),

    "Islamabad": (13, 14),
    "Peshawar": (9, 15),

    "DI Khan": (7, 13),
    "Gilgit": (14, 18)
        }

        india_pos = {
        "Delhi": (4, 6), "Jaipur": (3, 5),
        "Lucknow": (5, 6), "Patna": (6, 5),
        "Kolkata": (7, 4), "Chandigarh": (4, 7),
        "Amritsar": (3, 7), "Mumbai": (2, 2),
        "Pune": (2.5, 1.5), "Hyderabad": (4, 2),
        "Bangalore": (3, 1), "Chennai": (4, 0),
        "Ahmedabad": (2, 4), "Bhopal": (3.5, 3),
        "Indore": (3, 2.5)
        }

        nodes = set(G.nodes)
        if "New York" in nodes:
            return usa_pos
        elif "Karachi" in nodes:
            return pakistan_pos
        else:
            return india_pos

    def run(self):
        self.root.mainloop()