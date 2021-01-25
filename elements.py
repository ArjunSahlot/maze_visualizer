import pygame
import numpy as np
pygame.init()


class Slider:
    colors = {
        "text": (255,) * 3,
        "slider": (50,) * 3,
        "cursor": (130,) * 3,
        "arrows": (255,) * 3,
        "boxes": (80,) * 3,
        "highlighted_boxes": (120,) * 3,
    }

    def __init__(self, x, y, width, height=40, init_val=80, val_range=(1, 100), label="Slider", only_int=True):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.font = pygame.font.SysFont("comicsans", height - 5)
        self.label = label
        self.range = val_range
        self.value = init_val
        self.dragging = False
        self.to_int = only_int
        self.left = pygame.Surface((height,)*2, pygame.SRCALPHA)
        self.right = pygame.Surface((height,)*2, pygame.SRCALPHA)
        self.create_surfs()

    def create_surfs(self):
        self.left.fill(self.colors["boxes"])
        self.right.fill(self.colors["boxes"])
        pad = 3
        l = pad
        r = self.height - pad
        t = pad
        m = self.height/2
        b = self.height - pad
        pygame.draw.polygon(self.left, self.colors["arrows"], ((r, t), (l, m), (r, b)))
        pygame.draw.polygon(self.right, self.colors["arrows"], ((l, t), (r, m), (l, b)))

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                    self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

    def draw(self, window):
        pygame.draw.rect(window, self.colors["slider"], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.colors["cursor"], (self.value_to_loc(), self.y, self.height, self.height))
        window.blit(self.left, (self.x, self.y))
        window.blit(self.right, (self.x + self.width - self.height, self.y))
        text = self.font.render(f"{self.label}: {self.value}", 1, self.colors["text"])
        text_loc = (self.x + (self.width-text.get_width()) // 2, self.y + self.height + 5)
        window.blit(text, text_loc)

    def value_to_loc(self):
        val = np.interp(self.value, self.range, (self.x + self.height, self.x + self.width - self.height*2))
        return int(val) if self.to_int else val


class Button:
    pass


class Dropdown:
    pass



window = pygame.display.set_mode((400, 400))
a = Slider(20, 20, 200)
while True:
    window.fill((10, 120, 148))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    a.update(window, events)
    pygame.display.update()
