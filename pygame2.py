# Импортируем библиотеку pygame
from pickle import FALSE
import pygame
from pygame import *
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

def main():
    hero = Player(55,55) # создаем героя по (x,y) координатам
    left = right = up = False    # по умолчанию — стоим
    entities = pygame.sprite.Group() # Все объекты
    animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
    platforms = [] # то, во что мы будем врезаться или опираться
    entities.add(hero)
    # единственный телепорт на карте
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
        "-                                -",
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
    timer = pygame.time.Clock()

    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

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

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля       

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    working = True
    running = False
    while(working): # Основной цикл программы
        timer.tick(60)

        for e in pygame.event.get(): # Обрабатываем события
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                    running = True
            if e.type == KEYUP and e.key == K_LSHIFT:
                    running = False

            if e.type == QUIT:
                pygame.display.flip()
                working = False
        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 

        hero.update(left, right, up, running, platforms)   # передвижение

        camera.update(hero) # центризируем камеру относительно персонажа
        # entities.draw(screen) # отображение всего
        for e in entities:
           screen.blit(e.image, camera.apply(e))

        animatedEntities.update() # показываем анимацию
        pygame.display.update()     # обновление и вывод всех изменений на экран

if __name__ == "__main__":
    main()