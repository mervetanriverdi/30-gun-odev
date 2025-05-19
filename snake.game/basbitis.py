import pygame
import sys

def baslangic_ekrani():
    ekran = pygame.display.set_mode((600, 400))
    pygame.display.set_caption(\"Yılan Oyunu\")
    font = pygame.font.SysFont(None, 48)
    yazi = font.render(\"Başlamak için bir tuşa basın\", True, (255, 255, 255))
    dikdortgen = yazi.get_rect(center=(300, 200))

    ekran.fill((0, 0, 0))
    ekran.blit(yazi, dikdortgen)
    pygame.display.flip()

    while True:
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.KEYDOWN:
                return

def bitis_ekrani(skor):
    ekran = pygame.display.set_mode((600, 400))
    pygame.display.set_caption(\"Oyun Bitti\")
    font = pygame.font.SysFont(None, 48)
    yazi = font.render(f\"Skor: {skor} - Yeniden başlamak için tuşa bas\", True, (255, 255, 255))
    dikdortgen = yazi.get_rect(center=(300, 200))

    ekran.fill((0, 0, 0))
    ekran.blit(yazi, dikdortgen)
    pygame.display.flip()

    while True:
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.KEYDOWN:
                return
