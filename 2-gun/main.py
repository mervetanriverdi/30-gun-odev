import pygame
import sys

pygame.init()

ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Yılan Oyunu - 2. Gün")
saat = pygame.time.Clock()

siyah = (0, 0, 0)
yesil = (0, 255, 0)
hucre = 20

import pygame
import sys
import random

pygame.init()

ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Yılan Oyunu - 3. Gün")
saat = pygame.time.Clock()

siyah = (0, 0, 0)
yesil = (0, 255, 0)
hucre = 20

yilan = [(100, 100), (80, 100), (60, 100)]
yon = "sag"

elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                yon = "sol"
            elif e.key == pygame.K_RIGHT:
                yon = "sag"
            elif e.key == pygame.K_UP:
                yon = "yukari"
            elif e.key == pygame.K_DOWN:
                yon = "asagi"

    x, y = yilan[0]
    if yon == "sag":
        x += hucre
    elif yon == "sol":
        x -= hucre
    elif yon == "yukari":
        y -= hucre
    elif yon == "asagi":
        y += hucre

    yilan.insert(0, (x, y))

    if yilan[0] == elma:
        elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
    else:
        yilan.pop()

    ekran.fill(siyah)

    # Elmayı çiz
    pygame.draw.rect(ekran, (255, 0, 0), (elma[0], elma[1], hucre, hucre))

    # Yılanı çiz
    for parca in yilan:
        pygame.draw.rect(ekran, yesil, (parca[0], parca[1], hucre, hucre))

    pygame.display.flip()
    saat.tick(10)

