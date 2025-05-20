import pygame
import random
import sys

class Oyun:
    def __init__(self):
        self.genislik, self.yukseklik = 600, 400
        self.ekran = pygame.display.set_mode((self.genislik, self.yukseklik))
        pygame.display.set_caption("Yılan Oyunu")
        self.saat = pygame.time.Clock()
        self.hiz = 10
        self.yilan_pos = [[100, 50]]
        self.yon = 'RIGHT'
        self.elma = self.yeni_elma()
        self.skor = 0

    def yeni_elma(self):
        return [random.randrange(0, self.genislik, 10), random.randrange(0, self.yukseklik, 10)]

    def ciz(self):
        self.ekran.fill((0, 0, 0))
        for parca in self.yilan_pos:
            pygame.draw.rect(self.ekran, (0, 255, 0), pygame.Rect(parca[0], parca[1], 10, 10))
        pygame.draw.rect(self.ekran, (255, 0, 0), pygame.Rect(self.elma[0], self.elma[1], 10, 10))
        pygame.display.flip()

    def hareket_et(self):
        bas = self.yilan_pos[0][:]
        if self.yon == 'UP':
            bas[1] -= 10
        elif self.yon == 'DOWN':
            bas[1] += 10
        elif self.yon == 'LEFT':
            bas[0] -= 10
        elif self.yon == 'RIGHT':
            bas[0] += 10
        self.yilan_pos.insert(0, bas)

        if bas == self.elma:
            self.skor += 1
            self.elma = self.yeni_elma()
        else:
            self.yilan_pos.pop()

    def carpisma_kontrol(self):
        bas = self.yilan_pos[0]
        return (bas in self.yilan_pos[1:] or
                bas[0] < 0 or bas[0] >= self.genislik or
                bas[1] < 0 or bas[1] >= self.yukseklik)

    def tus_kontrol(self):
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif etkinlik.type == pygame.KEYDOWN:
                if etkinlik.key == pygame.K_UP and self.yon != 'DOWN':
                    self.yon = 'UP'
                elif etkinlik.key == pygame.K_DOWN and self.yon != 'UP':
                    self.yon = 'DOWN'
                elif etkinlik.key == pygame.K_LEFT and self.yon != 'RIGHT':
                    self.yon = 'LEFT'
                elif etkinlik.key == pygame.K_RIGHT and self.yon != 'LEFT':
                    self.yon = 'RIGHT'

    def calistir(self):
        while True:
            self.tus_kontrol()
            self.hareket_et()
            if self.carpisma_kontrol():
                break
            self.ciz()
            self.saat.tick(self.hiz)
        pygame.quit()
        return self.skor

if __name__ == "__main__":
    pygame.init()
    oyun = Oyun()
    skor = oyun.calistir()
    print("Oyun Bitti. Skor:", skor)
