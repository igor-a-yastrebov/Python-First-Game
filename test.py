import pygame

pygame.init()

# Основная функция прогарммы
def main():
    win = pygame.display.set_mode((500, 500)) # размеры X и Y
    pygame.display.set_caption("Название игры")

    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__== "__main__":
  main()

pygame.quit()
