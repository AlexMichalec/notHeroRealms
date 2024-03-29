import pygame


class Button:
    def __init__(self, screen, text, x, y, padding = 10, function= None):
        self.state = "active"
        self.screen = screen
        self.text = text
        self.function = function
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.padding = padding
        self.color = (110, 163, 255)
        self.border_color = (183, 207, 247)
        self.font = pygame.font.SysFont('Arial', 30)
        self.button_text = self.font.render(self.text, True, "white")
        self.width = self.button_text.get_rect().width + 2*self.padding
        self.height = self.button_text.get_rect().height + 2*self.padding
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 3)
        self.screen.blit(self.button_text, (self.x + self.padding, self.y + self.padding))

    def use(self):
        self.function()

    def update_rect(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)







