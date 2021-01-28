import pygame
from constants import *
import threading
import random
from random_utils.datatypes import Stack


class Maze:
    algs = {
        "Recursive Backtracker": "recursive_backtrack",
        "Randomized Kruskal's": "kruskal",
        "Randomized Prim's": "prim",
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
        self.stop()
        for row in self.cells:
            for cell in row:
                if cell not in ("start", "end"):
                    cell.free()

    def stop(self):
        self.active = True

    def visualize(self, alg, speed):
        threading.Thread(target=getattr(self, self.algs[alg]), args=(speed,)).start()

    def prim(self, speed):
        for row in self.cells:
            for cell in row:
                if cell != "start":
                    cell.block()
        self.end = None
        self.start = self.start if self.start is not None else self.cells[0][0]

        clock = pygame.time.Clock()
        cell = self.start

        neighbors = self.get_generation_neighbors(*cell.get_pos(), "free")

        visited = 1
        self.active = False
        total = (self.rows - 1)//2 + (self.cols - 1)//2
        while visited < total:
            if not self.active:
                clock.tick(speed.value*100)
                n_i = random.randrange(len(neighbors))
                n = neighbors[n_i]
                cell = self.cells[n[0]][n[1]]
                visited += 1
                cell.free()
                neighbors = neighbors[:n_i] + neighbors[n_i + 1:]
                pos = cell.get_pos()
                near_n0, near_n1 = self.get_generation_neighbors(*pos)[0]
                self.cells[(pos[0] + near_n0) // 2][(pos[1] + near_n1) // 2] = 0

                unvisited = self.get_generation_neighbors(*pos, "free")
                neighbors = list(set(neighbors + unvisited))
            else:
                return
        # walls = self.get_generation_neighbors(*self.start.get_pos())
        # self.active = False
        # while walls:
        #     if not self.active:
        #         clock.tick(speed.value*100)
        #         wall = random.choice(walls)
        #         if self.cells[wall[0]][wall[1]] != "block":
        #             self.cells[(cell.get_pos()[0] + wall[0])//2][(cell.get_pos()[1] + wall[1])//2].free()
        #         walls.extend(self.get_generation_neighbors(*wall))
        #         walls.remove(wall)
        #     else:
        #         return

        self.active = True

    def recursive_backtrack(self, speed):
        self.start = self.start if self.start is not None else self.cells[0][0]
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
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].block()
        
        self.start = self.end = None

        clock = pygame.time.Clock()
        trees = []
        for row in range(1, self.rows - 1, 2):
            for col in range(1, self.cols - 1, 2):
                trees.append([(row, col)])
                self.cells[row][col].free()
        self.active = False
        edges = []
        edges.extend([(row, col) for col in range(1, self.cols - 1, 2) for row in range(2, self.rows - 1, 2)])
        edges.extend([(row, col) for col in range(2, self.cols - 1, 2) for row in range(1, self.rows - 1, 2)])
        random.shuffle(edges)

        while len(trees) > 1:
            if not self.active:
                clock.tick(speed.value*100)
                row, col = edges.pop(0)

                enum_trees = enumerate(trees)

                if not row % 2:
                    tree1 = sum([i if (row - 1, col) in t else 0 for i, t in enum_trees])
                    tree2 = sum([i if (row + 1, col) in t else 0 for i, t in enum_trees])
                else:
                    tree1 = sum([i if (row, col - 1) in t else 0 for i, t in enum_trees])
                    tree2 = sum([i if (row, col + 1) in t else 0 for i, t in enum_trees])

                if tree1 != tree2:
                    t1, t2 = trees[tree1], trees[tree2]
                    trees.remove(t1)
                    trees.remove(t2)
                    trees.append(t1 + t2)
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
    
    def get_generation_neighbors(self, row, col, type="block"):
        neighbors = []
        # if row > 0:
        #     neighbors.append((row - 1, col))
        # if row < self.rows - 1:
        #     neighbors.append((row + 1, col))
        # if col > 0:
        #     neighbors.append((row, col - 1))
        # if col < self.cols - 1:
        #     neighbors.append((row, col + 1))

        if row > 1 and self.cells[row - 2][col] == type:
            neighbors.append((row - 2, col))
        if row < self.rows - 2 and self.cells[row + 2][col] == type:
            neighbors.append((row + 2, col))
        if col > 1 and self.cells[row][col - 2] == type:
            neighbors.append((row, col - 2))
        if col < self.cols - 2 and self.cells[row][col + 2] == type:
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
