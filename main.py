import tkinter as tk
from PIL import Image, ImageTk
from gui import MazeApp
from map_gui import MapApp


class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NAVI-CORE AI")
        self.root.state("zoomed")

        self.bg_main = "#3B7597"
        self.bg_dark = "#093C5D"
        self.accent = "#6FD1D7"

        self.bg_image = Image.open("d1.png")
        self.bg_image = self.bg_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            120,
            text="Navi-Core AI",
            font=("Segoe UI", 28, "bold"),
            fill="black"
        )

        self.create_button("Maze Solver", self.open_maze, 250)
        self.create_button("Map Paths", self.open_map, 320)
        self.create_button("Exit", self.root.destroy, 390)

    def create_button(self, text, cmd, y):
        btn = tk.Button(
            self.root,
            text=text,
            command=cmd,
            width=20,
            height=2,
            bg=self.bg_dark,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2"
        )

        btn.bind("<Enter>", lambda e: btn.config(bg=self.accent))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.bg_dark))

        self.canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            y,
            window=btn
        )

    def open_maze(self):
        self.root.destroy()
        MazeApp().run()

    def open_map(self):
        self.root.destroy()
        MapApp().run()


if __name__ == "__main__":
    Dashboard().root.mainloop()