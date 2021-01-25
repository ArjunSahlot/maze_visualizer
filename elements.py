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

    def draw_arrows(self):
        left = pygame.Surface((self.height,)*2, pygame.SRCALPHA)
        right = pygame.Surface((self.height,)*2, pygame.SRCALPHA)
        mx = pygame.mouse.get_pos()[0]
        colliding = self.x <= mx <= self.x + self.height
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        left.fill(color)
        colliding = self.x + self.width - self.height <= mx <= self.x + self.width
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        right.fill(color)
        xpad = 8
        ypad = 5
        l = xpad
        r = self.height - xpad
        t = ypad
        m = self.height/2
        b = self.height - ypad
        pygame.draw.polygon(left, self.colors["arrows"], ((r, t), (l, m), (r, b)))
        pygame.draw.polygon(right, self.colors["arrows"], ((l, t), (r, m), (l, b)))
        window.blit(left, (self.x, self.y))
        window.blit(right, (self.x + self.width - self.height, self.y))

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = (self.x + self.height <= mx <= self.x + self.width - self.height and self.y <= my <= self.y + self.height)
                if self.x <= mx <= self.x + self.height:
                    self.value = max(self.value - 1, self.range[0])
                elif self.x + self.width - self.height <= mx <= self.x + self.width:
                    self.value = min(self.value + 1, self.range[1])
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging:
            self.loc_to_value()

    def draw(self, window):
        pygame.draw.rect(window, self.colors["slider"], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.colors["cursor"], (self.value_to_loc() - self.height/2, self.y, self.height, self.height))
        self.draw_arrows()
        text = self.font.render(f"{self.label}: {self.value}", 1, self.colors["text"])
        text_loc = (self.x + (self.width-text.get_width()) // 2, self.y + self.height + 5)
        window.blit(text, text_loc)

    def loc_to_value(self):
        val = np.interp(pygame.mouse.get_pos()[0], (self.x + self.height*1.5, self.x + self.width - self.height*1.5), self.range)
        self.value = int(val) if self.to_int else val

    def value_to_loc(self):
        return np.interp(self.value, self.range, (self.x + self.height*1.5, self.x + self.width - self.height*1.5))


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
