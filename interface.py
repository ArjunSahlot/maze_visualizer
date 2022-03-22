#
#  Maze visualizer
#  Visualize path finding as well as maze generating algorithms!
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

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
    big_font = pygame.font.SysFont("comicsans", 80)
    small_font = pygame.font.SysFont("comicsans", 35)
    color_map = {
        "READY": GREEN,
        "FINISHED": GREEN,
        "PATH FOUND": GREEN,
        "CALCULATING": WHITE,
        "RETRACING": BLUE,
        "STOPPED": RED,
        "PATH NOT FOUND": (255, 140, 0),
        "NO POSSIBLE PATH": (255, 140, 0)
    }

    def __init__(self, height):
        self.height = height

        self.clear_canvas = Button(
            WIDTH - 87.5 - 5,
            5,
            87.5,
            60,
            "Clear Canvas",
            4,
            2
        )
        self.clear_canvas.colors["border"] = self.clear_canvas.colors["text"] = (255, 140, 70)

        self.clear_path = Button(
            self.clear_canvas.x - self.clear_canvas.width - 5,
            self.clear_canvas.y,
            self.clear_canvas.width,
            self.clear_canvas.height,
            "Clear Path",
            self.clear_canvas.border,
            2
        )
        self.clear_path.colors["border"] = self.clear_path.colors["text"] = (255, 140, 70)

        self.stop = Button(
            self.clear_path.x,
            self.clear_path.y + self.clear_path.height + 5,
            180,
            self.clear_path.height,
            "Stop",
            self.clear_path.border
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
            self.find.width + (self.find.x + self.find.width - self.stop.x) + self.stop.width,
            label="Speed",
            init_val=100,
            val_range=(1, 200)
        )

        self.find_drop = Dropdown(
            (self.gen.x - 20 - 350, 5),
            (350, 50),
            (350, 140),
            BLACK,
            self.find_drop_text,
            list(Maze.path_algs.keys()),
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
            list(Maze.maze_algs.keys()),
            highlight_col=self.find_drop.highlight_col,
            color=self.find_drop.color,
            border_col=self.find_drop.border_col
        )

        self.cell_size = Slider(
            10,
            10,
            self.gen_drop.loc[0] - 25,
            40,
            20,
            (1, 200),
            "Cell Size",
        )

        self.maze = Maze(0, height, WIDTH, HEIGHT-height, 10)

    def update(self, window, events):
        self.clear_canvas.update(window, events)
        self.clear_path.update(window, events)
        self.stop.update(window, events)
        self.gen.update(window, events)
        self.find.update(window, events)
        self.speed.update(window, events)
        self.find_drop.update(window, events)
        self.gen_drop.update(window, events)
        self.cell_size.update(window, events)
        if self.cell_size.dragging or self.cell_size.clicked:
            self.maze.update_dim(self.cell_size.value)
        self.maze.update(window, events)

        text = self.big_font.render(state := self.maze.state, 1, self.color_map[state])
        x = self.gen_drop.loc[0] / 2 - text.get_width() / 2
        y = self.height - 5 - text.get_height() - 50
        window.blit(text, (x, y))

        pygame.draw.line(window, (255,)*3, (self.cell_size.x, self.height - 5 - 50), (self.cell_size.x + self.cell_size.width, self.height - 5 - 50), 5)
        pygame.draw.line(window, (255,)*3, (self.cell_size.x, self.height - 5 - 50), (self.cell_size.x, self.height), 5)
        pygame.draw.line(window, (255,)*3, (self.cell_size.x + self.cell_size.width/2, self.height - 5 - 50), (self.cell_size.x + self.cell_size.width/2, self.height), 5)
        pygame.draw.line(window, (255,)*3, (self.cell_size.x + self.cell_size.width, self.height - 5 - 50), (self.cell_size.x + self.cell_size.width, self.height), 5)

        t1 = self.small_font.render(f"{self.maze.visited} cells visited", 1, (255,)*3)
        t2 = self.small_font.render(f"{round(self.maze.time, 3)} secs", 1, (255,)*3)
        window.blit(t1, (self.cell_size.x + self.cell_size.width/4 - t1.get_width()/2, self.height - 27 - t1.get_height()/2))
        window.blit(t2, (self.cell_size.x + self.cell_size.width*3/4 - t2.get_width()/2, self.height - 27 - t2.get_height()/2))

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

        elif self.clear_canvas.clicked(events):
            self.maze.clear_canvas()

        elif self.clear_path.clicked(events):
            self.maze.clear_path()

    def quit(self):
        self.maze.stop()
