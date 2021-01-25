import pygame
from constants import *
from maze import Maze


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    maze = Maze(0, 200, WIDTH, HEIGHT-200, 200)

    while True:
        clock.tick(FPS)
        window.fill(GREY)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        maze.update(window, events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ctrl_pressed:
                    pygame.quit()
                    return
        pygame.display.update()


main(WINDOW)
