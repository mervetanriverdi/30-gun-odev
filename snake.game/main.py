import pygame
import sys
from oyun import Oyun
from ekranlar import baslangic_ekrani, bitis_ekrani

pygame.init()

# Ana oyun döngüsü
while True:
    baslangic_ekrani()
    oyun = Oyun()
    skor = oyun.calistir()
    bitis_ekrani(skor)

    
