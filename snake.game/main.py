import pygame
import sys
import random
import time

pygame.init()

# Ekran ve hücre ayarları
GENISLIK, YUKSEKLIK = 600, 400
HUCRE = 20
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu - (mavi elma güncellemesi!)")
saat = pygame.time.Clock()

# Renkler
siyah = (0, 0, 0)
yesil = (0, 255, 0)
koyu_yesil = (0, 150, 0)
kirmizi = (255, 0, 0)
mavi = (0, 0, 255)
beyaz = (255, 255, 255)
gri = (100, 100, 100)
arka_plan = (0, 80, 0)
altin = (255, 215, 0)  # Altın sarısı


# Font
font = pygame.font.SysFont(None, 36)

# === Sınıflar ===

class Yilan:
    def __init__(self):
        self.beden = [(100, 100), (80, 100), (60, 100)]
        self.yon = "sag"

    def hareket_et(self):
        x, y = self.beden[0]
        if self.yon == "sag":
            x += HUCRE
        elif self.yon == "sol":
            x -= HUCRE
        elif self.yon == "yukari":
            y -= HUCRE
        elif self.yon == "asagi":
            y += HUCRE
        yeni_bas = (x, y)
        self.beden.insert(0, yeni_bas)
        return yeni_bas

    def kısalt(self, miktar=1):
        for _ in range(miktar):
            self.beden.pop()

    def carpisti_mi(self, engeller):
        bas = self.beden[0]
        return (
            bas in self.beden[1:] or
            bas in engeller or
            bas[0] < 0 or bas[0] >= GENISLIK or
            bas[1] < 0 or bas[1] >= YUKSEKLIK
        )

class Elma:
    def __init__(self, yilan, engeller):
        self.tur, self.konum = self.yeni_elma_uret(yilan, engeller)

    def yeni_elma_uret(self, yilan, engeller):
        while True:
            konum = (random.randint(0, 29) * HUCRE, random.randint(0, 19) * HUCRE)
            if konum not in yilan and konum not in engeller:
                tur = "altin" if random.random() < 0.2 else "kirmizi"
                return tur, konum

    def ciz(self):
        renk = mavi if self.tur == "mavi" else kirmizi
        pygame.draw.rect(ekran, renk, (*self.konum, HUCRE, HUCRE))

class Oyun:
    def __init__(self, hiz=10, sure_limit=30):
        self.yilan = Yilan()
        self.engeller = [
            (200, 100), (200, 120), (200, 140),
            (400, 200), (420, 200), (440, 200),
            (300, 300), (300, 320), (300, 340)
        ]
        self.elma = Elma(self.yilan.beden, self.engeller)
        self.skor = 0
        self.hiz = hiz
        self.sure_limit = sure_limit
        self.baslangic_zamani = time.time()
        self.duraklatildi = False
        self.mesaj = ""
        self.mesaj_zamani = 0

    def tus_kontrol(self, tus):
        if tus == pygame.K_LEFT and self.yilan.yon != "sag":
            self.yilan.yon = "sol"
        elif tus == pygame.K_RIGHT and self.yilan.yon != "sol":
            self.yilan.yon = "sag"
        elif tus == pygame.K_UP and self.yilan.yon != "asagi":
            self.yilan.yon = "yukari"
        elif tus == pygame.K_DOWN and self.yilan.yon != "yukari":
            self.yilan.yon = "asagi"
        elif tus == pygame.K_p:
            self.duraklatildi = not self.duraklatildi

    def calistir(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    self.tus_kontrol(e.key)

            if self.duraklatildi:
                pygame.time.delay(100)
                continue

            gecen = time.time() - self.baslangic_zamani
            if gecen >= self.sure_limit:
                return self.skor

            yeni_bas = self.yilan.hareket_et()

            if self.yilan.carpisti_mi(self.engeller):
                return self.skor

            if yeni_bas == self.elma.konum:
                if self.elma.tur == "kirmizi":
                    self.skor += 1
                    self.mesaj = random.choice(["Taptaze!", "Lezzetli!", "Güzel seçim!"])
                    self.yilan.kısalt(0)
                else:
                    self.skor += 3
                    self.mesaj = "ALTIN ELMAYI KAPTIN !"
                    self.yilan.kısalt(-2)
                self.mesaj_zamani = time.time()
                if self.skor % 5 == 0 and self.hiz < 30:
                    self.hiz += 2
                self.elma = Elma(self.yilan.beden, self.engeller)
            else:
                self.yilan.kısalt()

            self.ekrani_guncelle(gecen)

    def ekrani_guncelle(self, gecen):
        ekran.fill(arka_plan)
        self.elma.ciz()

        for engel in self.engeller:
            pygame.draw.rect(ekran, gri, (*engel, HUCRE, HUCRE))

        for i, parca in enumerate(self.yilan.beden):
            if i == 0:
                pygame.draw.circle(ekran, koyu_yesil, (parca[0] + HUCRE // 2, parca[1] + HUCRE // 2), HUCRE // 2)
            else:
                pygame.draw.rect(ekran, yesil, (*parca, HUCRE, HUCRE))

        ekran.blit(font.render(f"Skor: {self.skor}", True, beyaz), (10, 10))
        ekran.blit(font.render(f"Kalan Süre: {int(self.sure_limit - gecen)}s", True, beyaz), (GENISLIK - 200, 10))

        if self.mesaj and time.time() - self.mesaj_zamani < 1.5:
            ekran.blit(font.render(self.mesaj, True, beyaz), (10, 50))

        pygame.display.flip()
        saat.tick(self.hiz)

# === Yardımcı Fonksiyonlar ===

def baslangic_ekrani():
    ekran.fill(arka_plan)
    yazi1 = font.render("Yılan Oyunu", True, beyaz)
    yazi2 = font.render("Başlamak için bir tuşa basın", True, beyaz)
    ekran.blit(yazi1, (GENISLIK//2 - yazi1.get_width()//2, 150))
    ekran.blit(yazi2, (GENISLIK//2 - yazi2.get_width()//2, 200))
    pygame.display.flip()

    bekle = True
    while bekle:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                bekle = False

def bitis_ekrani(skor):
    ekran.fill(arka_plan)
    yazi1 = font.render(f"Oyun Bitti! Skorun: {skor}", True, beyaz)
    yazi2 = font.render("Çıkmak için ESC - Tekrar için ENTER", True, beyaz)
    ekran.blit(yazi1, (GENISLIK//2 - yazi1.get_width()//2, 150))
    ekran.blit(yazi2, (GENISLIK//2 - yazi2.get_width()//2, 200))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_RETURN:
                    return

# === Ana Oyun Döngüsü ===

while True:
    baslangic_ekrani()
    oyun = Oyun()
    skor = oyun.calistir()
    bitis_ekrani(skor)


