from pygame import *
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
BKGRND_COLOR = "#004400"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % ICON_DIR),
            ('%s/blocks/portal1.png' % ICON_DIR)]

ANIMATION_PRINCESS = [
            ('%s/blocks/princess_l.png' % ICON_DIR),
            ('%s/blocks/princess_r.png' % ICON_DIR)]

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)

class BlockTeleport(Platform):
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 300))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BKGRND_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 800))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BKGRND_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
