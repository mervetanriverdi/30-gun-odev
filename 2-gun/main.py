import pygame
import sys
import random

pygame.init()

ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Yılan Oyunu - 4. Gün")
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
            if e.key == pygame.K_LEFT and yon != "sag":
                yon = "sol"
            elif e.key == pygame.K_RIGHT and yon != "sol":
                yon = "sag"
            elif e.key == pygame.K_UP and yon != "asagi":
                yon = "yukari"
            elif e.key == pygame.K_DOWN and yon != "yukari":
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

    yeni_bas = (x, y)

    if yeni_bas in yilan:
        print("Oyun Bitti! Yılan kendine çarptı.")
        pygame.quit()
        sys.exit()

    yilan.insert(0, yeni_bas)

    if yeni_bas == elma:
        elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
    else:
        yilan.pop()

    ekran.fill(siyah)

    pygame.draw.rect(ekran, (255, 0, 0), (elma[0], elma[1], hucre, hucre))

    for parca in yilan:
        pygame.draw.rect(ekran, yesil, (parca[0], parca[1], hucre, hucre))

    pygame.display.flip()
    saat.tick(10)

