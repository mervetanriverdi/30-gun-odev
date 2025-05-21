import pygame
import sys
from oyun import Oyun
from basbitis import baslangic_ekrani, bitis_ekrani

pygame.init()
ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Yılan Oyunu")
font = pygame.font.SysFont(None, 48)

while True:
    baslangic_ekrani(ekran, font)
    oyun = Oyun(ekran)
    skor = oyun.calistir()
    bitis_ekrani(ekran, font, skor)
