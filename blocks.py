from pygame import *
import os
import pyganim
from camera import Camera

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
BKGRND_COLOR = "#004400"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % ICON_DIR, 200),
            ('%s/blocks/portal1.png' % ICON_DIR, 200)]

ANIMATION_PRINCESS = [
            ('%s/blocks/princess_l.png' % ICON_DIR, 800),
            ('%s/blocks/princess_r.png' % ICON_DIR, 800)]

class BlockStatic(sprite.Sprite):
    def __init__(self, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = Surface((width, height))
        self.rect = Rect(x, y, width, height)
    def draw(self, screen: Surface, camera: Camera):
        screen.blit(self.image, camera.transformSprite(self))

class Platform(BlockStatic):
    def __init__(self, x, y):
        BlockStatic.__init__(self, x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)

class BlockDie(BlockStatic):
    def __init__(self, x, y):
        BlockStatic.__init__(self, x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)

class BlockAnimated(BlockStatic):
    def __init__(self, x, y, width, height, animation):
        BlockStatic.__init__(self, x, y, width, height)
        self.boltAnim = pyganim.PygAnimation(animation)
        self.boltAnim.play()

    def draw(self, screen: Surface, camera: Camera):
        self.image.fill(Color(BKGRND_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
        BlockStatic.draw(self, screen, camera)

class BlockTeleport(BlockAnimated):
    def __init__(self, x, y, goX,goY):
        BlockAnimated.__init__(self, x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, ANIMATION_BLOCKTELEPORT)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения

class Princess(BlockAnimated):
    def __init__(self, x, y):
        BlockAnimated.__init__(self, x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, ANIMATION_PRINCESS)
