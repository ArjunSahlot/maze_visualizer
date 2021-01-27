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
        self.start.start()
        self.end = self.cells[0][1]
        self.end.end()
        self.state = "READY"
        self.active = True
    
    def clear(self):
        for row in self.cells:
            for cell in row:
                if cell not in ("start", "end"):
                    cell.free()

    def stop(self):
        self.active = True

    def visualize(self, alg, speed):
        threading.Thread(target=getattr(self, self.algs[alg]), args=(speed,)).start()

    def recursive_backtrack(self, speed):
        cell = self.start
        visited = [cell.get_pos()]
        path = Stack(cell)
        clock = pygame.time.Clock()
        self.active = False
        self.end = None
        for row in self.cells:
            for cell in row:
                if cell != "start":
                    cell.block()

        while path:
            if not self.active:
                clock.tick(speed.value*10)
                cell = path.pop()
                neighbors = self.get_generation_neighbors(*cell.get_pos())
                if neighbors:
                    for row, col in neighbors:
                        if (row, col) not in visited:
                            neighbor = self.cells[row][col]
                            path.push(cell)
                            neighbor.free()
                            self.cells[(cell.get_pos()[0] + row)//2][(cell.get_pos()[1] + col)//2].free()
                            visited.append((row, col))
                            path.push(neighbor)
                            break
            else:
                return

        self.active = True

    def kruskal(self, speed):
        forest = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].block()
                forest.append([(row, col)])

        self.active = False
        edges = []
        clock = pygame.time.Clock()
        edges.extend([(row, col) for row in range(2, self.rows - 1, 2) for col in range(1, self.cols - 1, 2)])
        edges.extend([(row, col) for row in range(1, self.rows - 1, 2) for col in range(2, self.cols - 1, 2)])
        random.shuffle(edges)

        while len(forest) > 1:
            if not self.active:
                clock.tick(speed.value*100)
                row, col = edges.pop(0)

                tree1 = tree2 = -1

                enum_forest = enumerate(forest)

                if row % 2:
                    tree1 = sum([i if (row, col - 1) in t else 0 for i, t in enum_forest])
                    tree2 = sum([i if (row, col + 1) in t else 0 for i, t in enum_forest])
                else:
                    tree1 = sum([i if (row - 1, col) in t else 0 for i, t in enum_forest])
                    tree2 = sum([i if (row + 1, col) in t else 0 for i, t in enum_forest])

                if tree1 != tree2:
                    t1, t2 = forest[tree1], forest[tree2]
                    tree = t1 + t2
                    forest = [x for x in forest if x not in (t1, t2)]
                    forest.append(tree)
                    self.cells[row][col].free()
            else:
                break

        self.active = True

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
                        diff = sum(map(abs, rel))
                        if diff > 100:
                            for r in range(row-3, row+4):
                                for c in range(col-3, col+4):
                                    r = min(max(r, 0), self.rows-1)
                                    c = min(max(c, 0), self.cols-1)
                                    if (cell := self.cells[r][c]) not in ("start", "end"):
                                        cell.free()
                        elif diff > 70:
                            for r in range(row-2, row+3):
                                for c in range(col-2, col+3):
                                    r = min(max(r, 0), self.rows-1)
                                    c = min(max(c, 0), self.cols-1)
                                    if (cell := self.cells[r][c]) not in ("start", "end"):
                                        cell.free()
                        elif diff > 45:
                            for r in range(row-1, row+2):
                                for c in range(col-1, col+2):
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
    
    def get_generation_neighbors(self, row, col):
        neighbors = []
        # if row > 0:
        #     neighbors.append((row - 1, col))
        # if row < self.rows - 1:
        #     neighbors.append((row + 1, col))
        # if col > 0:
        #     neighbors.append((row, col - 1))
        # if col < self.cols - 1:
        #     neighbors.append((row, col + 1))

        if row > 1 and self.cells[row - 2][col] == "block":
            neighbors.append((row - 2, col))
        if row < self.rows - 2 and self.cells[row + 2][col] == "block":
            neighbors.append((row + 2, col))
        if col > 1 and self.cells[row][col - 2] == "block":
            neighbors.append((row, col - 2))
        if col < self.cols - 2 and self.cells[row][col + 2] == "block":
            neighbors.append((row, col + 2))

        random.shuffle(neighbors)

        return neighbors

class Cell:
    colors = {
        "free": (255,) * 3,
        "block": (0,) * 3,
        "start": (0, 255, 0),
        "end": (255, 0, 0),
        "path": (0, 0, 255),
    }

    def __init__(self, row, col, width):
        self.row, self.col, self.width = row, col, width
        self.prev = None
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
