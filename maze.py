import pygame
from random import randint


class Maze:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rows, self.cols = height // 15, width // 15
        self.cells = [[Cell(row, col, 15) for col in range(self.cols)] for row in range(self.rows)]

    def update(self, window, events):
        self.draw(window)

    def draw(self, window):
        for row in self.cells:
            for cell in row:
                cell.draw(window, self.x, self.y)


class Cell:
    colors = {
        True: (255,) * 3,
        False: (0,) * 3
    }

    def __init__(self, row, col, width):
        self.row, self.col, self.width = row, col, width
        self.state = randint(1, 2) == 1

    def draw(self, window, x_off, y_off):
        x = x_off + self.col*self.width
        y = y_off + self.row*self.width
        pygame.draw.rect(window, self.colors[self.state], (x, y, self.width, self.width))
