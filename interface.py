import pygame
from elements import *
from constants import *


class Interface:
    def __init__(self, height):
        self.height = height
        self.gen = Button(WIDTH - 150 - 5, 5, 150, 60, "Generate", 5)
        self.find = Button(self.gen.x, self.gen.y + self.gen.height + 5, self.gen.width, 60, "Find Path", self.gen.border)
        self.speed = Slider(self.find.x, self.find.y + self.find.height + 10, self.find.width, 50, label="Speed")
        self.find_drop = Dropdown((self.gen.x - 10 - 200, 5), (200, 50), (200, 140), BLACK, "Path Finding Algs")
        self.gen_drop = Dropdown((self.find_drop.x - 10 - 200, 5), (200, 50), (200, 140), BLACK, "Maze Gen Algs")

    def update(self, window, events):
        pass
