import pygame
import sys
import random
import time

pygame.init()

GENISLIK, YUKSEKLIK = 600, 400
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu - (yeni gün, yeni lezzetler!)")
saat = pygame.time.Clock()

siyah = (0, 0, 0)
yesil = (0, 255, 0)
koyu_yesil = (0, 150, 0)
kirmizi = (255, 0, 0)
beyaz = (255, 255, 255)
gri = (100, 100, 100)
arka_plan = (0, 80, 0)
hucre = 20

font = pygame.font.SysFont(None, 36)

def yuksek_skoru_yukle():
    try:
        with open("skor.txt", "r") as dosya:
            return int(dosya.read())
    except:
        return 0

def yuksek_skoru_kaydet(skor):
    with open("skor.txt", "w") as dosya:
        dosya.write(str(skor))

class Yilan:
    def __init__(self):
        self.parcalar = [(100, 100), (80, 100), (60, 100)]
        self.yon = "sag"
    
    def hareket_et(self):
        x, y = self.parcalar[0]
        if self.yon == "sag":
            x += hucre
        elif self.yon == "sol":
            x -= hucre
        elif self.yon == "yukari":
            y -= hucre
        elif self.yon == "asagi":
            y += hucre
        yeni_bas = (x, y)
        self.parcalar.insert(0, yeni_bas)
        return yeni_bas
    
    def kuyrugu_kisalt(self):
        self.parcalar.pop()

    def carpisma_var_mi(self, pozisyon, engeller):
        x, y = pozisyon
        return (
            x < 0 or x >= GENISLIK or
            y < 0 or y >= YUKSEKLIK or
            pozisyon in self.parcalar or
            pozisyon in engeller
        )

class Elma:
    def __init__(self, yilan, engeller):
        self.pozisyon = self.yeni_elma_uret(yilan, engeller)
    
    def yeni_elma_uret(self, yilan, engeller):
        while True:
            elma = (random.randint(0, 29) * hucre, random.randint(0, 19) * hucre)
            if elma not in yilan and elma not in engeller:
                return elma

class Oyun:
    def __init__(self, hiz=10, sure_limit=30):
        self.hiz = hiz
        self.sure_limit = sure_limit
        self.skor = 0
        self.yilan = Yilan()
        self.engeller = [
            (200, 100), (200, 120), (200, 140),
            (400, 200), (420, 200), (440, 200),
            (300, 300), (300, 320), (300, 340)
        ]
        self.elma = Elma(self.yilan.parcalar, self.engeller).pozisyon
        self.baslangic_zamani = time.time()
        self.mesaj = ""
        self.mesaj_zamani = 0
        self.duraklatildi = False

    def baslat(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT and self.yilan.yon != "sag":
                        self.yilan.yon = "sol"
                    elif e.key == pygame.K_RIGHT and self.yilan.yon != "sol":
                        self.yilan.yon = "sag"
                    elif e.key == pygame.K_UP and self.yilan.yon != "asagi":
                        self.yilan.yon = "yukari"
                    elif e.key == pygame.K_DOWN and self.yilan.yon != "yukari":
                        self.yilan.yon = "asagi"
                    elif e.key == pygame.K_p:
                        self.duraklatildi = not self.duraklatildi

            if self.duraklatildi:
                pygame.time.delay(100)
                continue

            gecen = time.time() - self.baslangic_zamani
            if gecen >= self.sure_limit:
                return self.skor

            yeni_bas = self.yilan.hareket_et()
            if self.yilan.carpisma_var_mi(yeni_bas, self.engeller):
                return self.skor

            if yeni_bas == self.elma:
                self.skor += 1
                self.mesaj = random.choice(["Taptaze!", "Güne güzel başladık!", "Lezzetliydi!", "Enerji depolandı!"])
                self.mesaj_zamani = time.time()
                if self.skor % 5 == 0 and self.hiz < 30:
                    self.hiz += 2
                self.elma = Elma(self.yilan.parcalar, self.engeller).pozisyon
            else:
                self.yilan.kuyrugu_kisalt()

            self.ekrani_guncelle(gecen)

    def ekrani_guncelle(self, gecen):
        ekran.fill(arka_plan)
        pygame.draw.rect(ekran, kirmizi, (*self.elma, hucre, hucre))
        for engel in self.engeller:
            pygame.draw.rect(ekran, gri, (*engel, hucre, hucre))

        for i, parca in enumerate(self.yilan.parcalar):
            if i == 0:
                pygame.draw.circle(ekran, koyu_yesil, (parca[0] + hucre // 2, parca[1] + hucre // 2), hucre // 2)
            else:
                pygame.draw.rect(ekran, yesil, (*parca, hucre, hucre))

        ekran.blit(font.render(f"Skor: {self.skor}", True, beyaz), (10, 10))
        kalan = int(self.sure_limit - gecen)
        ekran.blit(font.render(f"Kalan Süre: {kalan}s", True, beyaz), (GENISLIK - 200, 10))
        if self.mesaj and time.time() - self.mesaj_zamani < 1.5:
            ekran.blit(font.render(self.mesaj, True, beyaz), (10, 50))
        pygame.display.flip()
        saat.tick(self.hiz)

# Diğer fonksiyonlar (baslangic_ekrani, oyun_bitti_ekrani) aynen korunabilir.
# Ana döngüde sadece `Oyun().baslat()` şeklinde çağrılır.

