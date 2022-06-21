import pygame

pygame.init()

# Основная функция прогарммы
def main():
    win = pygame.display.set_mode((500, 500)) # размеры X и Y
    pygame.display.set_caption("Название игры")

    run = True
    while(run):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ( (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT) ):
                run = False


main()

pygame.quit()
