from pygame import *

# TODO: когда сделаем уровни, заинъектить сюда текущий уровень через какой-нибудь менеджер
class Camera(object):
    def __init__(self, width, height, winWidth, winHeight):
        self.state = Rect(0, 0, width, height)
        self.winWidth = winWidth
        self.winHeight = winHeight

    def transformSprite(self, sprite: sprite.Sprite) -> Rect: # перемещаем спрайт по координатам отоносительно камеры
        return sprite.rect.move(self.state.topleft)

    def centerCamera(self, target: Rect): # устанавливаем камеру по центру персонажа
        l, t, _, _ = target
        l, t = -l + self.winWidth / 2, -t + self.winHeight / 2

        l = min(0, l)                                       # Не движемся дальше левой границы
        l = max(- (self.state.width - self.winWidth), l)    # Не движемся дальше правой границы
        t = max(- (self.state.height - self.winHeight), t)  # Не движемся дальше нижней границы
        t = min(0, t)                                       # Не движемся дальше верхней границы

        self.state = Rect(l, t, self.state.width, self.state.height)
