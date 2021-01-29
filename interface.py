import pygame
from elements import *
from constants import *
from maze import Maze
from tkinter import messagebox, Tk
Tk().withdraw()
pygame.init()


class Interface:
    maze_drop_text = "Maze Gen Algs"
    find_drop_text = "Path Finding Algs"

    def __init__(self, height):
        self.height = height

        self.clear = Button(
            WIDTH - 180 - 5,
            5,
            180,
            60,
            "Clear",
            4
        )
        self.clear.colors["border"] = (255, 140, 70)
        self.clear.colors["text"] = (255, 140, 70)

        self.stop = Button(
            self.clear.x,
            self.clear.y + self.clear.height + 5,
            self.clear.width,
            self.clear.height,
            "Stop",
            self.clear.border
        )
        self.stop.colors["border"] = (255, 0, 0)
        self.stop.colors["text"] = (255, 0, 0)

        self.gen = Button(
            self.stop.x - 250 - 5,
            5,
            250,
            60,
            "Generate",
            self.stop.border
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
            self.find.y + self.find.height + 5,
            self.find.width + (self.find.x + self.find.width - self.clear.x) + self.clear.width,
            label="Speed",
            init_val=100,
            val_range=(1, 200)
        )

        self.gen_drop = Dropdown(
            (self.find_drop.loc[0] - 10 - self.find_drop.size[0], 5),
            self.find_drop.size,
            self.find_drop.pop_size,
            BLACK,
            self.maze_drop_text,
            ["Recursive Backtracker", "Randomized Kruskal's", "Randomized Prim's"],
            highlight_col=self.find_drop.highlight_col,
            color=self.find_drop.color,
            border_col=self.find_drop.border_col
        )

        self.maze = Maze(0, height, WIDTH, HEIGHT-height, 10)

        self.find_drop = Dropdown(
            (self.gen.x - 20 - 350, 5),
            (350, 50),
            (350, 140),
            BLACK,
            self.find_drop_text,
            list(self.maze.algs.keys()),
            highlight_col=(100, 100, 100),
            color=(255,)*3,
            border_col=(255,)*3
        )

    def update(self, window, events):
        self.clear.update(window, events)
        self.stop.update(window, events)
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
                self.maze.visualize(selected, self.speed)

        elif self.find.clicked(events):
            if (selected := self.find_drop.get_selection()) == self.find_drop_text:
                messagebox.showerror("Maze Generator", "Please choose an algorithm before path finding.")
            else:
                self.maze.visualize(selected, self.speed)
        
        elif self.stop.clicked(events):
            self.maze.stop()
        
        elif self.clear.clicked(events):
            self.maze.clear()

    def quit(self):
        self.maze.stop()
