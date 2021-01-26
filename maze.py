import pygame
from constants import *
import threading
import random
from random_utils.datatypes import Stack


class Maze:
    algs = {
        "Recursive Backtracker": "recursive_backtrack",
        "Kruskal's": "kruskal",
        "Alphastar": "astar"
    }

    def __init__(self, x, y, width, height, cell_size):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.cell_size = cell_size
        self.rows, self.cols = height // cell_size, width // cell_size
        self.cells = [[Cell(row, col, cell_size) for col in range(self.cols)] for row in range(self.rows)]
        self.start = self.cells[0][0]
        self.end = self.cells[0][1]
        self.active = True

    def visualize(self, alg, speed):
        threading.Thread(target=getattr(self, self.algs[alg]), args=(speed,)).start()

    def recursive_backtrack(self, speed):
        cell = self.start
        visited = [cell]
        path = Stack()
        while path:
            pass

    def kruskal(self, speed):
        pass

    def astar(self, speed):
        pass

    def update(self, window, events=None):
        self.draw(window)

        if self.active:
            mx, my = pygame.mouse.get_pos()
            rel = pygame.mouse.get_rel()
            if self.x < mx < self.x + self.cols*self.cell_size and self.y < my < self.y + self.rows*self.cell_size:
                mouse_pressed = pygame.mouse.get_pressed()
                if any(mouse_pressed):
                    row = (my - self.y) // self.cell_size
                    col = (mx - self.x) // self.cell_size
                    cell = self.cells[row][col]
                    if mouse_pressed[0]:
                        if self.start is None and cell != "end":
                            cell.start()
                            self.start = cell
                        if self.end is None and cell != "start":
                            cell.end()
                            self.end = cell
                        if cell not in ("start", "end"):
                            cell.block()
                    if mouse_pressed[2]:
                        if sum(map(abs, rel)) > 45:
                            for r in (row-1, row, row+1):
                                for c in (col-1, col, col+1):
                                    r = min(max(r, 0), self.rows-1)
                                    c = min(max(c, 0), self.cols-1)
                                    if (cell := self.cells[r][c]) not in ("start", "end"):
                                        cell.free()
                        else:
                            if cell == "start":
                                self.start = None
                            elif cell == "end":
                                self.end = None

                            cell.free()

    def draw(self, window):
        for row in self.cells:
            for cell in row:
                cell.draw(window, self.x, self.y)

        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 4)


class Cell:
    colors = {
        "free": (255,) * 3,
        "block": (0,) * 3,
        "start": (0, 255, 0),
        "end": (255, 0, 0),
        "path": (0, 255, 0),
    }

    def __init__(self, row, col, width):
        self.row, self.col, self.width = row, col, width
        self.state = "free"

    def draw(self, window, x_off, y_off):
        x = x_off + self.col*self.width
        y = y_off + self.row*self.width
        pygame.draw.rect(window, self.colors[self.state], (x, y, self.width, self.width))

    def free(self):
        self.state = "free"

    def block(self):
        self.state = "block"

    def start(self):
        self.state = "start"

    def end(self):
        self.state = "end"

    def path(self):
        self.state = "path"

    def get_pos(self):
        return (self.row, self.col)

    def __eq__(self, other):
        return self.state == other

    def __ne__(self, other):
        return self.state != other
