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
    tri_padx = 8
    tri_pady = 5

    def __init__(self, x, y, width, height=40, init_val=80, val_range=(1, 100), label="Slider", only_int=True):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.font = pygame.font.SysFont("comicsans", height - 15)
        self.label = label
        self.range = val_range
        self.value = init_val
        self.dragging = False
        self.to_int = only_int

    def draw_arrows(self, window):
        left = pygame.Surface((self.height,)*2, pygame.SRCALPHA)
        right = pygame.Surface((self.height,)*2, pygame.SRCALPHA)
        mx, my = pygame.mouse.get_pos()
        colliding = self.x <= mx <= self.x + self.height and self.y <= my <= self.y + self.height
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        left.fill(color)
        colliding = self.x + self.width - self.height <= mx <= self.x + self.width and self.y <= my <= self.y + self.height
        color = self.colors["highlighted_boxes"] if colliding else self.colors["boxes"]
        right.fill(color)
        l = self.tri_padx
        r = self.height - self.tri_padx
        t = self.tri_pady
        m = self.height/2
        b = self.height - self.tri_pady
        pygame.draw.polygon(left, self.colors["arrows"], ((r, t), (l, m), (r, b)))
        pygame.draw.polygon(right, self.colors["arrows"], ((l, t), (r, m), (l, b)))
        window.blit(left, (self.x, self.y))
        window.blit(right, (self.x + self.width - self.height, self.y))

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.y <= my <= self.y + self.height:
                    self.dragging = self.x + self.height <= mx <= self.x + self.width - self.height
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
        self.draw_arrows(window)
        text = self.font.render(f"{self.label}: {self.value}", 1, self.colors["text"])
        text_loc = (self.x + (self.width-text.get_width()) // 2, self.y + self.height + 5)
        window.blit(text, text_loc)

    def loc_to_value(self):
        val = np.interp(pygame.mouse.get_pos()[0], (self.x + self.height*1.5, self.x + self.width - self.height*1.5), self.range)
        self.value = int(val) if self.to_int else val

    def value_to_loc(self):
        return np.interp(self.value, self.range, (self.x + self.height*1.5, self.x + self.width - self.height*1.5))


class Button:
    colors = {
        "bg": (0,) * 3,
        "border": (255,) * 3,
        "text": (255,) * 3,
        "highlight": (255, 255, 255, 100),
    }

    def __init__(self, x, y, width, height=50, text="Button", border=0):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text = text
        self.font = pygame.font.SysFont("comicsans", height-10)
        self.border = border

    def update(self, window, events=None):
        self.draw(window)

    def clicked(self):
        if self.hovered():
            return pygame.MOUSEBUTTONDOWN in [event.type for event in events]

    def draw(self, window):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.colors["highlight" if self.hovered() else "bg"], (0, 0, self.width, self.height))
        if self.border: pygame.draw.rect(surf, self.colors["border"], (0, 0, self.width, self.height), self.border)
        text = self.font.render(self.text, 1, self.colors["text"])
        loc = (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2)
        surf.blit(text, loc)
        window.blit(surf, (self.x, self.y))

    def hovered(self):
        mx, my = pygame.mouse.get_pos()
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height


class Dropdown:
    def __init__(self,
                loc,
                size,
                pop_size,
                bg_col=(255, 255, 255),
                initial_text="Select",
                choices=["A", "B", "C", "D", "E", "F"],
                font=pygame.font.SysFont("comicsans", 35),
                color=(0, 0, 0),
                highlight_col=(80, 80, 255),
                border_col=(0, 0, 0),
                border = 5,
                pop_border = 3,
                rounding=10,
                text_padding=10,
                textbox_padding=10,
                tri_padding=15,
                sensitivity=5,
                view=1,):

        self.loc, self.size = loc, size
        self.selected = initial_text
        self.pop_loc = (loc[0] + size[0]/2 - pop_size[0]/2, loc[1] + size[1] - pop_border)
        self.pop_size = pop_size
        self.choices = list(choices)
        self.font = font
        self.color = color
        self.bg_col = bg_col
        self.highlight_col = highlight_col
        self.tri_padding = tri_padding
        self.border = border
        self.pop_border = pop_border
        self.border_col = border_col
        self.textbox_size = (self.pop_size[0], self.font.render("A", 1, (0, 0, 0)).get_height() + text_padding*2)
        self.textbox_padding = textbox_padding
        self.sensitivity, self.rounding = sensitivity, rounding
        self.popped = False
        width = self.size[1] - self.tri_padding*2
        self.tri_rect = (self.loc[0] + self.size[0] - self.tri_padding - width, self.loc[1] + self.tri_padding, width, width)
        self.surf = pygame.Surface(pop_size, pygame.SRCALPHA)
        self.slider_y = 0
        self.view = view

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(*self.loc, *self.size).collidepoint(mx, my):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.popped = not self.popped
        else:
            if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my) and self.popped:
                for i in range(len(self.choices)):
                    y = i * self.textbox_size[1] + self.slider_y
                    if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my):
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    self.selected = self.choices[i]
                                    self.popped = False
                                    return True

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.popped = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my) and self.popped:
                    if event.button == 4:
                        self.slider_y += self.sensitivity
                    if event.button == 5:
                        self.slider_y -= self.sensitivity
                self.slider_y = min(self.slider_y, 0)
                self.slider_y = max(self.slider_y, -self.textbox_size[1]*(len(self.choices)-self.view))

    def draw(self, window):
        left = self.tri_rect[0]
        right = self.tri_rect[0] + self.tri_rect[2]
        middle = self.tri_rect[0] + self.tri_rect[2]/2
        top = self.tri_rect[1]
        bottom = self.tri_rect[1] + self.tri_rect[3]

        if self.popped: self.draw_surf(window)
        if pygame.Rect(*self.loc, *self.size).collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, self.highlight_col, (*self.loc, *self.size), border_radius=self.rounding)
        else:
            pygame.draw.rect(window, self.bg_col, (*self.loc, *self.size), border_radius=self.rounding)

        pygame.draw.rect(window, self.border_col, (*self.loc, *self.size), self.border, border_top_left_radius=self.rounding, border_top_right_radius=self.rounding)
        text = self.font.render(self.selected, 1, self.color)
        window.blit(text, (self.loc[0] + self.size[0]/2 - text.get_width()/2, self.loc[1] + self.size[1]/2 - text.get_height()/2))

        if self.popped:
            pygame.draw.polygon(window, self.border_col, ((middle, top), (left, bottom), (right, bottom)))
            pygame.draw.rect(window, self.border_col, (*self.pop_loc, *self.pop_size), self.pop_border, border_bottom_left_radius=self.rounding, border_bottom_right_radius=self.rounding)
        else:
            pygame.draw.polygon(window, self.border_col, ((middle, bottom), (left, top), (right, top)))


    def get_selection(self):
        return self.selected

    def draw_surf(self, window):
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surf, self.bg_col, (0, 0, *self.pop_size), border_radius=self.rounding)
        mx, my = pygame.mouse.get_pos()
        for i, text in enumerate(self.choices):
            y = i * self.textbox_size[1] + self.slider_y
            if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my) or self.choices[i] == self.selected:
                pygame.draw.rect(self.surf, self.highlight_col, (self.textbox_padding/2, y + self.textbox_padding/2, self.textbox_size[0] - self.textbox_padding, self.textbox_size[1] - self.textbox_padding), border_radius=self.rounding)
            text = self.font.render(text, 1, self.color)
            self.surf.blit(text, (self.textbox_size[0]//2 - text.get_width()//2, y + self.textbox_size[1]//2 - text.get_height()//2))
        window.blit(self.surf, self.pop_loc)
