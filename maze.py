import pygame
from constants import *


class Maze:
    def __init__(self, x, y, width, height, cell_size):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.cell_size = cell_size
        self.rows, self.cols = height // cell_size, width // cell_size
        self.cells = [[Cell(row, col, cell_size) for col in range(self.cols)] for row in range(self.rows)]
        self.active = True

    def update(self, window):
        self.draw(window)

        if self.active:
            mx, my = pygame.mouse.get_pos()
            rel = pygame.mouse.get_rel()
            if self.x < mx < self.x + self.width and self.y < my < self.y + self.height:
                mouse_pressed = pygame.mouse.get_pressed()
                if any(mouse_pressed):
                    row = (my - self.y) // self.cell_size
                    col = (mx - self.x) // self.cell_size
                    cell = self.cells[row][col]
                    if mouse_pressed[0]:
                        cell.block()
                    if mouse_pressed[2]:
                        if sum(map(abs, rel)) > 80:
                            for r in (row-1, row, row+1):
                                for c in (col-1, col, col+1):
                                    r = min(max(r, 0), self.rows-1)
                                    c = min(max(c, 0), self.cols-1)
                                    self.cells[r][c].free()
                        else:
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

    def get_pos(self):
        return (self.row, self.col)
