import pygame
import sys
import random
import time

pygame.init()

# Ekran ayarları
GENISLIK, YUKSEKLIK = 600, 400
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu - (yeni gün, yeni lezzetler!)")
saat = pygame.time.Clock()

# Renkler
siyah = (0, 0, 0)
yesil = (0, 255, 0)
koyu_yesil = (0, 150, 0)
kirmizi = (255, 0, 0)
beyaz = (255, 255, 255)
gri = (100, 100, 100)
arka_plan = (0, 80, 0)
hucre = 20

font = pygame.font.SysFont(None, 36)

def yeni_elma_uret(yilan, engeller):
    while True:
        elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
        if elma not in yilan and elma not in engeller:
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

def oyun(skor=0, hiz=10, sure_limit=30):
    yilan = [(100, 100), (80, 100), (60, 100)]
    yon = "sag"
    
    engeller = [
        (200, 100), (200, 120), (200, 140),
        (400, 200), (420, 200), (440, 200),
        (300, 300), (300, 320), (300, 340)
    ]

    elma = yeni_elma_uret(yilan, engeller)
    baslangic_zamani = time.time()

    mesaj = ""
    mesaj_zamani = 0
    duraklatildi = False

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
                elif e.key == pygame.K_p:
                    duraklatildi = not duraklatildi

        if duraklatildi:
            pygame.time.delay(100)
            continue

        gecen_zaman = time.time() - baslangic_zamani
        if gecen_zaman >= sure_limit:
            return skor

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

        if (
            x < 0 or x >= GENISLIK or 
            y < 0 or y >= YUKSEKLIK or 
            yeni_bas in yilan or 
            yeni_bas in engeller
        ):
            return skor

        yilan.insert(0, yeni_bas)

        if yeni_bas == elma:
            skor += 1
            mesaj = random.choice(["Taptaze!", "Güne güzel başladık!", "Lezzetliydi!", "Enerji depolandı!"])
            mesaj_zamani = time.time()
            if skor % 5 == 0 and hiz < 30:
                hiz += 2
            elma = yeni_elma_uret(yilan, engeller)
        else:
            yilan.pop()

        ekran.fill(arka_plan)
        pygame.draw.rect(ekran, kirmizi, (elma[0], elma[1], hucre, hucre))

        for engel in engeller:
            pygame.draw.rect(ekran, gri, (engel[0], engel[1], hucre, hucre))

        for i, parca in enumerate(yilan):
            if i == 0:
                pygame.draw.circle(ekran, koyu_yesil, (parca[0] + hucre // 2, parca[1] + hucre // 2), hucre // 2)
            else:
                pygame.draw.rect(ekran, yesil, (parca[0], parca[1], hucre, hucre))

        skor_yazi = font.render(f"Skor: {skor}", True, beyaz)
        ekran.blit(skor_yazi, (10, 10))

        kalan_sure = int(sure_limit - gecen_zaman)
        zaman_yazi = font.render(f"Kalan Süre: {kalan_sure}s", True, beyaz)
        ekran.blit(zaman_yazi, (GENISLIK - 200, 10))

        if mesaj and time.time() - mesaj_zamani < 1.5:
            mesaj_yazi = font.render(mesaj, True, beyaz)
            ekran.blit(mesaj_yazi, (10, 50))

        pygame.display.flip()
        saat.tick(hiz)

def oyun_bitti_ekrani(skor):
    yuksek_skor = yuksek_skoru_yukle()
    if skor > yuksek_skor:
        yuksek_skor = skor
        yuksek_skoru_kaydet(skor)

    while True:
        ekran.fill(arka_plan)
        oyun_bitti_yazi = font.render("Günün sonu geldi!", True, kirmizi)
        skor_yazi = font.render(f"Skorun: {skor}", True, beyaz)
        yuksek_yazi = font.render(f"Rekor: {yuksek_skor}", True, beyaz)
        tekrar_yazi = font.render("R - Tekrar Oyna | ESC - Çık", True, beyaz)

        ekran.blit(oyun_bitti_yazi, (200, 100))
        ekran.blit(skor_yazi, (240, 150))
        ekran.blit(yuksek_yazi, (230, 190))
        ekran.blit(tekrar_yazi, (160, 250))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def baslangic_ekrani():
    motivasyonlar = [
        "Yeni gün, yeni rekor!",
        "Bugün daha uzun hayatta kal!",
        "Kahvaltı vakti: Elmaları topla!",
        "Enerjini topla, rekoru kır!"
    ]
    rastgele_mesaj = random.choice(motivasyonlar)
    
    while True:
        ekran.fill(arka_plan)
        baslik = font.render("Yılan Oyunu - Günlük Doz", True, beyaz)
        alt_yazi = font.render(rastgele_mesaj, True, beyaz)
        basla_yazi = font.render("Başlamak için bir tuşa bas", True, beyaz)
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 100))
        ekran.blit(alt_yazi, (GENISLIK // 2 - alt_yazi.get_width() // 2, 150))
        ekran.blit(basla_yazi, (GENISLIK // 2 - basla_yazi.get_width() // 2, 200))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                return

# Ana döngü
while True:
    baslangic_ekrani()
    skor = oyun(skor=0, hiz=10, sure_limit=30)
    oyun_bitti_ekrani(skor)

