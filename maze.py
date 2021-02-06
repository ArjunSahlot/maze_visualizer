import pygame
from constants import *
import threading
import random
from random_utils.datatypes import Stack
from queue import PriorityQueue, Queue
from tkinter import Tk, messagebox
from time import time
Tk().withdraw()


class Maze:
    maze_algs = {
        "Recursive Backtracker": "recursive_backtrack",
        "Randomized Kruskal's": "kruskal",
        "Randomized Prim's": "prim",
        "Aldous-Broder Alg": "aldous_broder",
        "Recursive Division": "recursive_division",
    }
    path_algs = {
        "A* Search (Astar)": "astar",
        "Dijkstra's Alg": "dijkstra",
        "Best First Search": "bestfirst",
        "Depth First Search": "depth_first",
        "Breadth First Search": "breadth_first"
    }

    def __init__(self, x, y, width, height, cell_size):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.cell_size = cell_size
        self.rows, self.cols = height // cell_size, width // cell_size
        self.cells = [[Cell(row, col, cell_size) for col in range(self.cols)] for row in range(self.rows)]
        self.start = self.cells[self.rows//5][self.cols//5]
        self.start.start()
        self.end = self.cells[self.rows*4//5][self.cols*4//5]
        self.end.end()
        self.state = "READY"
        self.active = True

    def update_dim(self, cell_size):
        self.cell_size = cell_size
        self.rows, self.cols = self.height // cell_size, self.width // cell_size
        self.cells = [[Cell(row, col, cell_size) for col in range(self.cols)] for row in range(self.rows)]
        self.start = self.cells[self.rows//5][self.cols//5]
        self.start.start()
        self.end = self.cells[self.rows*4//5][self.cols*4//5]
        self.end.end()

    def clear_canvas(self):
        self.stop()
        for row in self.cells:
            for cell in row:
                cell.free()

        self.start = self.end = None

    def clear_path(self):
        self.stop()
        for row in self.cells:
            for cell in row:
                if cell in ("closed", "open", "path"):
                    cell.free()

    def stop(self):
        self.state = "STOPPED"
        self.active = True

    def finish(self):
        self.state = "FINISHED"
        self.active = True

    def visualize(self, alg, speed):
        if alg in self.path_algs:
            if self.start is None or self.end is None:
                messagebox.showerror("Maze Generator", "Please choose a start and end point to find the path.")
                return
            threading.Thread(target=getattr(self, self.path_algs[alg]), args=(speed,)).start()
        else:
            threading.Thread(target=getattr(self, self.maze_algs[alg]), args=(speed,)).start()

        self.state = "CALCULATING"

    def depth_first(self, speed):
        self.active = False
        clock = pygame.time.Clock()
        open = Stack(self.start)
        visited = set()
        path = {}
        while open:
            if not self.active:
                clock.tick(speed.value*100)
                curr = open.pop()
                if curr not in ("start", "end"):
                    curr.open()
                visited.add(curr)
                for n in self.get_pathfind_neighbors(curr):
                    if n not in visited:
                        path[n] = curr
                        if n == "end":
                            self.reconstruct(path, speed)
                            return
                        else:
                            open.push(n)
                            if n not in ("start", "end"):
                                n.close()
            else:
                return

        self.not_found()

    def breadth_first(self, speed):
        self.active = False
        clock = pygame.time.Clock()
        count = 0
        open = Queue()
        open.put((0, count, self.start))
        path = {}
        g_score = {cell: float("inf") for row in self.cells for cell in row}
        g_score[self.start] = 0

        while not open.empty():
            if not self.active:
                clock.tick(speed.value*100)
                curr = open.get()[2]

                temp_g = g_score[curr] + 1
                for n in self.get_pathfind_neighbors(curr):
                    if n == "end":
                        path[n] = curr
                        self.reconstruct(path, speed)
                        return
                    if temp_g < g_score[n]:
                        path[n] = curr
                        g_score[n] = temp_g
                        if not any(n == item[2] for item in open.queue):
                            count += 1
                            open.put((g_score[n], count, n))
                            n.close()

                if curr != self.start:
                    curr.open()
            else:
                return

        self.not_found()

    def not_found(self):
        self.state = "NO POSSIBLE PATH"
        self.active = True

    def recursive_division(self, speed):
        for row in range(self.rows):
            for col in range(self.cols):
                if row in (0, self.rows - 1) or col in (0, self.cols - 1):
                    self.cells[row][col].block()
                else:
                    self.cells[row][col].free()

        self.start = self.end = None
        region = Stack(((1, 1), (self.rows - 2, self.cols - 2)))
        self.active = False
        clock = pygame.time.Clock()

        while region:
            if not self.active:
                clock.tick(speed.value*10)
                curr = region.pop()
                min_y, max_y = curr[0][0], curr[1][0]
                min_x , max_x = curr[0][1], curr[1][1]
                h = max_y - min_y + 1
                w = max_x - min_x + 1

                if h <= 1 or w <= 1: continue

                if w < h:
                    cut_dir = 1
                elif w > h:
                    cut_dir = 0
                else:
                    if w == 2:
                        continue
                    cut_dir = random.randrange(2)

                cut_length = (h, w)[(cut_dir + 1) % 2]
                if cut_length < 3:
                    continue

                cut_pos = random.randrange(1, cut_length, 2)
                door_pos = random.randrange(0, (h, w)[cut_dir], 2)
                if cut_dir:
                    for col in range(min_x, max_x + 1):
                        self.cells[min_y + cut_pos][col].block()
                    self.cells[min_y + cut_pos][min_x + door_pos].free()
                else:
                    for row in range(min_y, max_y + 1):
                        self.cells[row][min_x + cut_pos].block()
                    self.cells[min_y + door_pos][min_x + cut_pos].free()

                if cut_dir:
                    region.extend((((min_y, min_x), (min_y + cut_pos - 1, max_x)), ((min_y + cut_pos + 1, min_x), (max_y, max_x))))
                else:
                    region.extend((((min_y, min_x), (max_y, min_x + cut_pos - 1)), ((min_y, min_x + cut_pos + 1), (max_y, max_x))))
            else:
                return

        self.finish()

    def aldous_broder(self, speed):
        for row in self.cells:
            for cell in row:
                if cell not in ("start", "end"):
                    cell.block()

        self.active = False
        clock = pygame.time.Clock()
        self.start = self.start if self.start is not None else self.cells[self.rows//5][self.cols//5]
        self.start.start()
        row, col = self.start.get_pos()
        visited = 1
        total = self.rows * self.cols

        while visited < total:
            if not self.active:
                clock.tick(speed.value**2/4)
                if not (neighbors := self.get_generation_neighbors(row, col)):
                    row, col = random.choice(self.get_generation_neighbors(row, col, types=("free",)))
                    continue
                for r, c in neighbors:
                    if (cell := self.cells[r][c]) in ("block", "end"):
                        if cell != "end":
                            self.cells[(r + row) // 2][(c + col) // 2].free()
                            cell.free()
                        visited += 1
                        row, col = r, c
                        break
            else:
                return

        self.finish()

    def prim(self, speed):
        for row in self.cells:
            for cell in row:
                if cell != "start":
                    cell.block()
        self.end = None
        self.start = self.start if self.start is not None else self.cells[self.rows//5][self.cols//5]
        self.start.start()

        clock = pygame.time.Clock()
        frontiers = [(*self.start.get_pos(), *self.start.get_pos())]
        self.active = False

        while frontiers:
            if not self.active:
                clock.tick(speed.value*100)
                f = frontiers.pop(random.randrange(len(frontiers)))
                row, col = f[2:]
                if self.cells[row][col] in ("block", "start"):
                    if (cell := self.cells[f[0]][f[1]]) != "start":
                        cell.free()
                    if (cell := self.cells[row][col]) != "start":
                        cell.free()

                    if row > 1 and self.cells[row - 2][col] == "block":
                        frontiers.append((row - 1, col, row - 2, col))

                    if row < self.rows - 2 and self.cells[row + 2][col] == "block":
                        frontiers.append((row + 1, col, row + 2, col))

                    if col > 1 and self.cells[row][col - 2] == "block":
                        frontiers.append((row, col - 1, row, col - 2))

                    if col < self.cols - 2 and self.cells[row][col + 2] == "block":
                        frontiers.append((row, col + 1, row, col + 2))
            else:
                return

        self.finish()

    def recursive_backtrack(self, speed):
        self.start = self.start if self.start is not None else self.cells[self.rows//5][self.cols//5]
        self.start.start()
        cell = self.start
        visited = [cell.get_pos()]
        path = Stack(cell)
        clock = pygame.time.Clock()
        self.active = False
        for row in self.cells:
            for cell in row:
                if cell not in ("start", "end"):
                    cell.block()

        while path:
            if not self.active:
                clock.tick(speed.value*10)
                cell = path.pop()
                neighbors = self.get_generation_neighbors(*cell.get_pos())
                if neighbors:
                    for row, col in neighbors:
                        if (row, col) not in visited:
                            n = self.cells[row][col]
                            path.push(cell)
                            if n != "end":
                                n.free()
                            self.cells[(cell.get_pos()[0] + row)//2][(cell.get_pos()[1] + col)//2].free()
                            visited.append((row, col))
                            path.push(n)
                            break
            else:
                return

        self.finish()

    def kruskal(self, speed):
        for row in self.cells:
            for cell in row:
                cell.block()

        self.start = self.end = None
        self.active = False
        clock = pygame.time.Clock()

        trees = []
        for row in range(1, self.rows - 1, 2):
            for col in range(1, self.cols - 1, 2):
                trees.append([(row, col)])
                self.cells[row][col].free()

        edges = []
        edges.extend((row, col) for row in range(2, self.rows - 1, 2) for col in range(1, self.cols - 1, 2))
        edges.extend((row, col) for row in range(1, self.rows - 1, 2) for col in range(2, self.cols - 1, 2))

        random.shuffle(edges)

        while len(trees) > 1:
            if not self.active:
                clock.tick(speed.value*100)
                row, col = edges.pop(0)

                tree1 = tree2 = -1

                if row % 2:
                    tree1 = sum([i if (row, col - 1) in j else 0 for i, j in enumerate(trees)])
                    tree2 = sum([i if (row, col + 1) in j else 0 for i, j in enumerate(trees)])
                else:
                    tree1 = sum([i if (row - 1, col) in j else 0 for i, j in enumerate(trees)])
                    tree2 = sum([i if (row + 1, col) in j else 0 for i, j in enumerate(trees)])

                if tree1 != tree2:
                    t1, t2 = trees[tree1], trees[tree2]
                    new_tree = t1 + t2
                    trees.remove(t1)
                    trees.remove(t2)
                    trees.append(new_tree)
                    self.cells[row][col].free()
            else:
                return

        self.finish()

    def astar(self, speed):
        self.active = False
        clock = pygame.time.Clock()
        count = 0
        open = PriorityQueue()
        open.put((0, count, self.start))
        path = {}
        g_score = {cell: float("inf") for row in self.cells for cell in row}
        g_score[self.start] = 0

        f_score = {cell: float("inf") for row in self.cells for cell in row}
        f_score[self.start] = self.heuristic(self.start)

        while not open.empty():
            if not self.active:
                clock.tick(speed.value*80)
                curr = open.get()[2]

                temp_g = g_score[curr] + 1
                for n in self.get_pathfind_neighbors(curr):
                    if n == "end":
                        self.reconstruct(path, speed)
                        return
                    if temp_g < g_score[n]:
                        path[n] = curr
                        g_score[n] = temp_g
                        f_score[n] = temp_g + self.heuristic(n)
                        if not any(n == item[2] for item in open.queue):
                            count += 1
                            open.put((f_score[n], count, n))
                            n.close()

                if curr != self.start:
                    curr.open()
            else:
                return

        self.not_found()

    def dijkstra(self, speed):
        self.active = False
        clock = pygame.time.Clock()
        count = 0
        open = PriorityQueue()
        open.put((0, count, self.start))
        path = {}
        g_score = {cell: float("inf") for row in self.cells for cell in row}
        g_score[self.start] = 0

        while not open.empty():
            if not self.active:
                clock.tick(speed.value*100)
                curr = open.get()[2]

                temp_g = g_score[curr] + 1
                for n in self.get_pathfind_neighbors(curr):
                    if n == "end":
                        path[n] = curr
                        self.reconstruct(path, speed)
                        return
                    if temp_g < g_score[n]:
                        path[n] = curr
                        g_score[n] = temp_g
                        if not any(n == item[2] for item in open.queue):
                            count += 1
                            open.put((g_score[n], count, n))
                            n.close()

                if curr != self.start:
                    curr.open()
            else:
                return

        self.not_found()

    def bestfirst(self, speed):
        self.active = False
        clock = pygame.time.Clock()
        count = 0
        open = PriorityQueue()
        open.put((0, count, self.start))
        path = {}
        g_score = {cell: float("inf") for row in self.cells for cell in row}
        g_score[self.start] = 0

        f_score = {cell: float("inf") for row in self.cells for cell in row}
        f_score[self.start] = self.heuristic(self.start)

        while not open.empty():
            if not self.active:
                clock.tick(speed.value*100)
                curr = open.get()[2]

                temp_g = g_score[curr] + 1
                for n in self.get_pathfind_neighbors(curr):
                    if n == "end":
                        path[n] = curr
                        self.reconstruct(path, speed)
                        return
                    if temp_g < g_score[n]:
                        path[n] = curr
                        g_score[n] = temp_g
                        f_score[n] = self.heuristic(n)
                        if not any(n == item[2] for item in open.queue):
                            count += 1
                            open.put((f_score[n], count, n))
                            n.close()

                if curr != self.start:
                    curr.open()
            else:
                return

        self.not_found()

    def reconstruct(self, path, speed):
        self.state = "RETRACING"
        self.reconstruct_path(path, speed)
        self.state = "PATH FOUND"
        self.active = True

    def reconstruct_path(self, path, speed):
        clock = pygame.time.Clock()
        curr = self.end
        while curr in path:
            if not self.active:
                clock.tick(speed.value*6)
                curr = path[curr]
                if curr != self.start:
                    curr.path()
            else:
                return

    def update(self, window, events=None):
        self.draw(window)

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

    def get_generation_neighbors(self, row, col, types=("block", "end")):
        neighbors = []
        if row > 1 and self.cells[row - 2][col] in types:
            neighbors.append((row - 2, col))
        if row < self.rows - 2 and self.cells[row + 2][col] in types:
            neighbors.append((row + 2, col))
        if col > 1 and self.cells[row][col - 2] in types:
            neighbors.append((row, col - 2))
        if col < self.cols - 2 and self.cells[row][col + 2] in types:
            neighbors.append((row, col + 2))

        random.shuffle(neighbors)

        return neighbors

    def get_pathfind_neighbors(self, cell):
        neighbors = []
        row, col = cell.get_pos()
        if row and (cell := self.cells[row - 1][col]) != "block":
            neighbors.append(cell)
        if row < self.rows - 1 and (cell := self.cells[row + 1][col]) != "block":
            neighbors.append(cell)
        if col and (cell := self.cells[row][col - 1]) != "block":
            neighbors.append(cell)
        if col < self.cols - 1 and (cell := self.cells[row][col + 1]) != "block":
            neighbors.append(cell)

        return neighbors

    def heuristic(self, cell):
        x1, y1 = cell.get_pos()
        x2, y2 = self.end.get_pos()
        return abs(x2-x1) + abs(y2-y1)


class Cell:
    colors = {
        "free": (255,) * 3,
        "block": (0,) * 3,
        "start": (0, 255, 0),
        "end": (255, 0, 0),
        "path": (0, 0, 255),
        "open": (255, 255, 120),
        "closed": (255, 140, 0),
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

    def open(self):
        self.state = "open"

    def close(self):
        self.state = "closed"

    def get_pos(self):
        return (self.row, self.col)

    def __hash__(self):
        return hash(self.get_pos())

    def __eq__(self, other):
        return self.state == other

    def __ne__(self, other):
        return self.state != other

    def __repr__(self):
        return f"{self.state} at {self.row, self.col}"
