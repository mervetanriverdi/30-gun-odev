import pygame
import sys
import random

pygame.init()

# Ekran ve temel ayarlar
GENISLIK, YUKSEKLIK = 600, 400
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu - 8. Gün Gelişmiş")
saat = pygame.time.Clock()

# Renkler
siyah = (0, 0, 0)
yesil = (0, 255, 0)
kirmizi = (255, 0, 0)
mavi = (0, 0, 255)
beyaz = (255, 255, 255)
hucre = 20

font = pygame.font.SysFont(None, 36)

def yeni_elma_uret(yilan):
    while True:
        elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
        if elma not in yilan:
            return elma

def yuksek_skoru_yukle():
    try:
        with open("skor.txt", "r") as dosya:
            return int(dosya.read())
    except:
        return 0

def yuksek_skoru_kaydet(skor):
    with open("skor.txt", "w") as dosya:
        dosya.write(str(skor))

def oyun(skor=0, hiz=10):
    yilan = [(100, 100), (80, 100), (60, 100)]
    yon = "sag"
    elma = yeni_elma_uret(yilan)

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

        # Çarpma kontrolleri
        if x < 0 or x >= GENISLIK or y < 0 or y >= YUKSEKLIK or yeni_bas in yilan:
            return skor  # Skoru döndür, ana döngüde oyun bitti ekranı aç

        yilan.insert(0, yeni_bas)

        if yeni_bas == elma:
            skor += 1
            if skor % 5 == 0 and hiz < 30:  # Maksimum hızı sınırla
                hiz += 2
            elma = yeni_elma_uret(yilan)
        else:
            yilan.pop()

        ekran.fill(mavi)  # Yeni arka plan rengi
        pygame.draw.rect(ekran, kirmizi, (elma[0], elma[1], hucre, hucre))

        # Yılanın daha ilginç şekilde çizilmesi
        for i, parca in enumerate(yilan):
            if i == 0:  # Baş kısmı daha farklı yapalım
                pygame.draw.circle(ekran, yesil, (parca[0] + hucre // 2, parca[1] + hucre // 2), hucre // 2)
            else:
                pygame.draw.rect(ekran, yesil, (parca[0], parca[1], hucre, hucre))

        skor_yazi = font.render(f"Skor: {skor}", True, beyaz)
        ekran.blit(skor_yazi, (10, 10))

        pygame.display.flip()
        saat.tick(hiz)

def oyun_bitti_ekrani(skor):
    yuksek_skor = yuksek_skoru_yukle()
    if skor > yuksek_skor:
        yuksek_skor = skor
        yuksek_skoru_kaydet(skor)

    while True:
        ekran.fill(mavi)
        oyun_bitti_yazi = font.render("Oyun Bitti!", True, kirmizi)
        skor_yazi = font.render(f"Skor: {skor}", True, beyaz)
        yuksek_yazi = font.render(f"Yüksek Skor: {yuksek_skor}", True, beyaz)
        tekrar_yazi = font.render("R - Tekrar Oyna | ESC - Çık", True, beyaz)

        ekran.blit(oyun_bitti_yazi, (200, 110))
        ekran.blit(skor_yazi, (240, 160))
        ekran.blit(yuksek_yazi, (210, 200))
        ekran.blit(tekrar_yazi, (160, 250))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return  # Oyunu yeniden başlat
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Ana döngü
while True:
    skor = oyun()
    oyun_bitti_ekrani(skor)
