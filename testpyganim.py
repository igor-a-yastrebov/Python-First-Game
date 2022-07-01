import pygame
from pygame.locals import *
import pyganim

pygame.init()
windowSurface = pygame.display.set_mode((320, 240), 0, 32)
pygame.display.set_caption('Pyganim Basic Demo')

boltAnim = pyganim.PygAnimation([('bolt_strike_0001.png', 100),
                                 ('bolt_strike_0002.png', 100),
                                 ('bolt_strike_0003.png', 100),
                                 ('bolt_strike_0004.png', 100),
                                 ('bolt_strike_0005.png', 100),
                                 ('bolt_strike_0006.png', 100),
                                 ('bolt_strike_0007.png', 100),
                                 ('bolt_strike_0008.png', 100),
                                 ('bolt_strike_0009.png', 100),
                                 ('bolt_strike_0010.png', 100)])
boltAnim.play()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    windowSurface.fill((100, 50, 50))
    boltAnim.blit(windowSurface, (100, 50))
    pygame.display.update()
    