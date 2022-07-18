from pickle import FALSE
import pygame
from pygame import *
from eventhandler import EventHandler
from monsters import *
from hero import *
from blocks import *
from camera import *

#Объявляем переменные
WIN_WIDTH = 1000 # Ширина создаваемого окна
WIN_HEIGHT = 700 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

def main() -> None:
    entities = pygame.sprite.Group() # Все объекты
    monsters = pygame.sprite.Group() # Все передвигающиеся монстры
    platforms = [] # то, во что мы будем врезаться или опираться

    hero = Hero(55,55)
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

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    camera = Camera(total_level_width, total_level_height, WIN_WIDTH, WIN_HEIGHT)
    eventHandler = EventHandler(hero)

    quit = False
    timer = pygame.time.Clock()
    while(not quit): # Основной цикл программы
        timer.tick(60)
        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 

        if eventHandler.handleEvents() == QUIT:
            pygame.display.flip()
            quit = True

        if (hero.winner):
            quit = True # прошли уровень - выходим

        monsters.update(platforms) # передвигаем всех монстров
        hero.update(platforms)   # передвижение персонажа

        camera.centerCamera(hero.rect) # центрируем камеру относительно персонажа
        for e in entities:
            e.draw(screen, camera)

        pygame.display.update()     # обновление и вывод всех изменений на экран

if __name__ == "__main__":
    main()