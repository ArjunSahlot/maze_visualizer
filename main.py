import pygame
from constants import *
from interface import Interface


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    interface = Interface(200)

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        interface.update(window, events)
        for event in events:
            if event.type == pygame.QUIT:
                interface.quit()
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ctrl_pressed:
                    interface.quit()
                    pygame.quit()
                    return
        pygame.display.update()


main(WINDOW)
