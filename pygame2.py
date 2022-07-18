from pickle import FALSE
import pygame
from pygame import *
from eventhandler import EventHandler
from monsters import *
from player import *
from blocks import *
from camera import *

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

#Объявляем переменные
WIN_WIDTH = 1000 #Ширина создаваемого окна
WIN_HEIGHT = 700 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

def main() -> None:
    entities = pygame.sprite.Group() # Все объекты
    animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя и монстров
    monsters = pygame.sprite.Group() # Все передвигающиеся монстры
    platforms = [] # то, во что мы будем врезаться или опираться

    hero = Player(55,55)
    entities.add(hero)

    # единственный монстр
    mn = Monster(190,200,2,3,150,105)
    entities.add(mn)
    platforms.append(mn)
    monsters.add(mn)

    # единственный телепорт
    tp = BlockTeleport(128,512,800,32)
    entities.add(tp)
    platforms.append(tp)
    animatedEntities.add(tp)
    level = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-        *                       -",
        "-                                -",
        "-            --                  -",
        "--                               -",
        "-                             P  -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-            *                   -",
        "-                            --- -",
        "-                                -",
        "-                                -",
        "-  *   ---                  *    -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-           ***                  -",
        "-                                -",
        "----------------------------------"]

    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    # парсим уровень, создаем блоки
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-": # простой блок
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*": # блок с шипами - смерть
                bd = BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    eventHandler = EventHandler(hero)

    quit = False
    timer = pygame.time.Clock()
    while(not quit): # Основной цикл программы
        timer.tick(60)
        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
        # pygame.display.update()     # обновление и вывод всех изменений на экран

        if eventHandler.handleEvents(platforms) == QUIT:
            pygame.display.flip()
            quit = True

        # hero.update(left, right, up, running, platforms)   # передвижение
        if (hero.winner):
            quit = True # прошли уровень - выходим

        camera.update(hero) # центризируем камеру относительно персонажа
        # pygame.display.update()     # обновление и вывод всех изменений на экран
        for e in entities:
            screen.blit(e.image, camera.apply(e))
            # pygame.display.update()     # обновление и вывод всех изменений на экран

        animatedEntities.update() # показываем анимацию
        # pygame.display.update()     # обновление и вывод всех изменений на экран
        monsters.update(platforms) # передвигаем всех монстров

        pygame.display.update()     # обновление и вывод всех изменений на экран

if __name__ == "__main__":
    main()