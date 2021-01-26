from elements import *
from constants import *
from maze import Maze
from tkinter import messagebox
from tkinter import Tk
Tk().withdraw()


class Interface:
    maze_drop_text = "Maze Gen Algs"
    find_drop_text = "Path Finding Algs"

    def __init__(self, height):
        self.height = height
        self.gen = Button(
            WIDTH - 250 - 5,
            5,
            250,
            60,
            "Generate",
            4
        )

        self.find = Button(
            self.gen.x,
            self.gen.y + self.gen.height + 5,
            self.gen.width,
            60,
            "Find Path",
            self.gen.border
        )


        self.speed = Slider(
            self.find.x,
            self.find.y + self.find.height + 10,
            self.find.width,
            label="Speed"
        )

        self.find_drop = Dropdown(
            (self.gen.x - 20 - 300, 5),
            (300, 50),
            (300, 140),
            BLACK,
            self.find_drop_text,
            ["Alphastar"],
            highlight_col=(100, 100, 100),
            color=(255,)*3,
            border_col=(255,)*3
        )

        self.gen_drop = Dropdown(
            (self.find_drop.loc[0] - 10 - self.find_drop.size[0], 5),
            self.find_drop.size,
            self.find_drop.pop_size,
            BLACK,
            self.maze_drop_text,
            ["Recursive Backtracker", "Kruskal's"],
            highlight_col=self.find_drop.highlight_col,
            color=self.find_drop.color,
            border_col=self.find_drop.border_col
        )

        self.maze = Maze(0, height, WIDTH, HEIGHT-height, 80)

    def update(self, window, events):
        self.gen.update(window, events)
        self.find.update(window, events)
        self.speed.update(window, events)
        self.find_drop.update(window, events)
        self.gen_drop.update(window, events)
        self.maze.update(window, events)

        if self.gen.clicked(events):
            if (selected := self.gen_drop.get_selection()) == self.maze_drop_text:
                messagebox.showerror("Maze Generator", "Please choose an algorithm before generating maze.")
            else:
                self.maze.visualize(selected)

        elif self.find.clicked(events):
            if (selected := self.find_drop.get_selection()) == self.find_drop_text:
                messagebox.showerror("Maze Generator", "Please choose an algorithm before path finding.")
            else:
                self.maze.visualize(selected)
