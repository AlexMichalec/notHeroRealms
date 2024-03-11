import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienie rozmiaru okna
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pół-przezroczysty prostokąt")

# Kolor pół-przezroczystego prostokąta w formacie RGBA (czerwony, zielony, niebieski, przezroczystość)
color = (0, 0, 255, 128)  # Niebieski z poziomem przezroczystości 128 (na 255)

# Pozycja i rozmiar prostokąta
x = 100
y = 100
width_rect = 200
height_rect = 100

# Pętla główna programu
run = True
while run:
    # Sprawdzenie zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Wypełnienie okna kolorem tła
    win.fill((255, 255, 255))

    # Narysowanie pół-przezroczystego prostokąta
    pygame.draw.rect(win, color, (x, y, width_rect, height_rect))

    # Zaktualizowanie ekranu
    pygame.display.update()

# Zamknięcie Pygame
pygame.quit()
sys.exit()
