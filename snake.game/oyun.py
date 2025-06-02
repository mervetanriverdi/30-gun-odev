import pygame
import random
import sys

class Oyun:
    def __init__(self, ekran, hiz=10):
        self.genislik, self.yukseklik = 600, 400
        self.ekran = ekran
        self.saat = pygame.time.Clock()
        self.hiz = hiz
        self.yilan_pos = [[100, 50]]
        self.yon = 'RIGHT'
        self.elma = self.yeni_elma()
        self.skor = 0
        self.son_skor_artisi = 0
        self.font = pygame.font.SysFont(None, 36)
        self.arka_plan_rengi = (0, 0, 0)
        self.duraklatildi = False

    def yeni_elma(self):
        while True:
            elma = [random.randrange(0, self.genislik, 10), random.randrange(0, self.yukseklik, 10)]
            if elma not in self.yilan_pos:
                return elma

    def rastgele_arka_plan_rengi(self):
        self.arka_plan_rengi = (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )

    def ciz(self):
        self.ekran.fill(self.arka_plan_rengi)
        for segment in self.yilan_pos:
            pygame.draw.rect(self.ekran, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))
        pygame.draw.rect(self.ekran, (255, 0, 0), pygame.Rect(self.elma[0], self.elma[1], 10, 10))

        skor_yazi = self.font.render(f"Skor: {self.skor}", True, (255, 255, 255))
        self.ekran.blit(skor_yazi, (self.genislik - skor_yazi.get_width() - 10, 10))

        if self.duraklatildi:
            durdu_yazi = self.font.render("DURDURULDU - 'P' ile devam et", True, (255, 255, 0))
            self.ekran.blit(durdu_yazi, ((self.genislik - durdu_yazi.get_width()) // 2, self.yukseklik // 2))

        pygame.display.flip()

    def hareket_et(self):
        yeni_bas = self.yilan_pos[0][:]
        if self.yon == 'UP':
            yeni_bas[1] -= 10
        elif self.yon == 'DOWN':
            yeni_bas[1] += 10
        elif self.yon == 'LEFT':
            yeni_bas[0] -= 10
        elif self.yon == 'RIGHT':
            yeni_bas[0] += 10
        self.yilan_pos.insert(0, yeni_bas)

        if yeni_bas == self.elma:
            self.skor += 1
            self.elma = self.yeni_elma()
            self.rastgele_arka_plan_rengi()

            if self.skor % 5 == 0 and self.skor != self.son_skor_artisi:
                self.hiz += 2
                self.son_skor_artisi = self.skor
        else:
            self.yilan_pos.pop()

    def carpisma_kontrol(self):
        bas = self.yilan_pos[0]
        return (
            bas in self.yilan_pos[1:] or
            bas[0] < 0 or bas[0] >= self.genislik or
            bas[1] < 0 or bas[1] >= self.yukseklik
        )

    def tus_kontrol(self):
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif etkinlik.type == pygame.KEYDOWN:
                if etkinlik.key == pygame.K_p:
                    self.duraklatildi = not self.duraklatildi
                elif not self.duraklatildi:
                    if etkinlik.key == pygame.K_UP and self.yon != 'DOWN':
                        self.yon = 'UP'
                    elif etkinlik.key == pygame.K_DOWN and self.yon != 'UP':
                        self.yon = 'DOWN'
                    elif etkinlik.key == pygame.K_LEFT and self.yon != 'RIGHT':
                        self.yon = 'LEFT'
                    elif etkinlik.key == pygame.K_RIGHT and self.yon != 'LEFT':
                        self.yon = 'RIGHT'

    def oyun_bitti_ekrani(self):
        oyun_bitti_yazi = self.font.render("Game Over!", True, (255, 0, 0))
        skor_yazi = self.font.render(f"Skorunuz: {self.skor}", True, (255, 255, 255))
        tekrar_yazi = self.font.render("Y: Yeniden Başla | Q: Çık", True, (255, 255, 0))

        self.ekran.fill((0, 0, 0))
        self.ekran.blit(oyun_bitti_yazi, ((self.genislik - oyun_bitti_yazi.get_width()) // 2, self.yukseklik // 2 - 50))
        self.ekran.blit(skor_yazi, ((self.genislik - skor_yazi.get_width()) // 2, self.yukseklik // 2 - 10))
        self.ekran.blit(tekrar_yazi, ((self.genislik - tekrar_yazi.get_width()) // 2, self.yukseklik // 2 + 30))
        pygame.display.flip()

        while True:
            for etkinlik in pygame.event.get():
                if etkinlik.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif etkinlik.type == pygame.KEYDOWN:
                    if etkinlik.key == pygame.K_y:
                        return True
                    elif etkinlik.key == pygame.K_q:
                        return False

    def calistir(self):
        while True:
            # Oyun başlangıç değerleri
            self.yilan_pos = [[100, 50]]
            self.yon = 'RIGHT'
            self.elma = self.yeni_elma()
            self.skor = 0
            self.son_skor_artisi = 0
            self.hiz = 10
            self.arka_plan_rengi = (0, 0, 0)
            self.duraklatildi = False

            oyun_devam = True
            while oyun_devam:
                self.tus_kontrol()
                if not self.duraklatildi:
                    self.hareket_et()
                    if self.carpisma_kontrol():
                        oyun_devam = False
                self.ciz()
                self.saat.tick(self.hiz)

            yeniden = self.oyun_bitti_ekrani()
            if not yeniden:
                break

