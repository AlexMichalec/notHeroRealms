import pygame
class Window():
    def __init__(self, width, height, visible = True):
        self.width = width
        self.height = height
        self.visible = visible
        self.card_views = []

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self):
        for view in self.card_views:
            view.draw()