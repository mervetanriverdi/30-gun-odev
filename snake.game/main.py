import pygame
import sys
import random

pygame.init()

ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Yılan Oyunu - 6. Gün")
saat = pygame.time.Clock()

siyah = (0, 0, 0)
yesil = (0, 255, 0)
kirmizi = (255, 0, 0)
beyaz = (255, 255, 255)
hucre = 20

font = pygame.font.SysFont(None, 36)

yilan = [(100, 100), (80, 100), (60, 100)]
yon = "sag"

elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
skor = 0
hiz = 10  # Başlangıç hızı

def oyun_bitti_ekrani(skor):
    ekran.fill(siyah)
    oyun_bitti_yazi = font.render("Oyun Bitti!", True, kirmizi)
    skor_yazi = font.render(f"Skor: {skor}", True, beyaz)
    ekran.blit(oyun_bitti_yazi, (200, 150))
    ekran.blit(skor_yazi, (250, 200))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

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

    if x < 0 or x >= 600 or y < 0 or y >= 400 or yeni_bas in yilan:
        oyun_bitti_ekrani(skor)

    yilan.insert(0, yeni_bas)

    if yeni_bas == elma:
        skor += 1
        if skor % 5 == 0:
            hiz += 2  # Her 5 elmada hızlan
        elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
    else:
        yilan.pop()

    ekran.fill(siyah)
    pygame.draw.rect(ekran, kirmizi, (elma[0], elma[1], hucre, hucre))

    for parca in yilan:
        pygame.draw.rect(ekran, yesil, (parca[0], parca[1], hucre, hucre))

    skor_yazi = font.render(f"Skor: {skor}", True, beyaz)
    ekran.blit(skor_yazi, (10, 10))

    pygame.display.flip()
    saat.tick(hiz)

