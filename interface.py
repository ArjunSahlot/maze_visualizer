import pygame
from elements import *
from constants import *


class Interface:
    def __init__(self, height):
        self.height = height
        self.gen = Button(
            WIDTH - 250 - 5,
            5,
            250,
            60,
            "Generate",
            5
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
            "Path Finding Algs",
            highlight_col=(100, 100, 100),
            color=(255,)*3,
            border_col=(255,)*3
        )

        self.gen_drop = Dropdown(
            (self.find_drop.loc[0] - 10 - self.find_drop.size[0], 5),
            self.find_drop.size,
            self.find_drop.pop_size,
            BLACK,
            "Maze Gen Algs",
            highlight_col=self.find_drop.highlight_col,
            color=self.find_drop.color,
            border_col=self.find_drop.border_col
        )

    def update(self, window, events):
        self.gen.update(window, events)
        self.find.update(window, events)
        self.speed.update(window, events)
        self.find_drop.update(window, events)
        self.gen_drop.update(window, events)
