from pygame import *
import pyganim
import blocks
import monsters

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз

ANIMATION_DELAY = 100 # скорость смены кадров
ANIMATION_SUPER_SPEED_DELAY = 50 # скорость смены кадров при ускорении
ANIMATION_RIGHT = [('mario/r1.png'),
            ('mario/r2.png'),
            ('mario/r3.png'),
            ('mario/r4.png'),
            ('mario/r5.png')]
ANIMATION_LEFT = [('mario/l1.png'),
            ('mario/l2.png'),
            ('mario/l3.png'),
            ('mario/l4.png'),
            ('mario/l5.png')]
ANIMATION_JUMP_LEFT = [('mario/jl.png', 100)]
ANIMATION_JUMP_RIGHT = [('mario/jr.png', 100)]
ANIMATION_JUMP = [('mario/j.png', 100)]
ANIMATION_STAY = [('mario/0.png', 100)]
MOVE_EXTRA_SPEED = 2.5 # Ускорение
JUMP_EXTRA_POWER = 1 # дополнительная сила прыжка

class Hero(blocks.BlockStatic):
    def __init__(self, x=55, y=55): # TODO: инициализацию вынести на создание уровня
        blocks.BlockStatic.__init__(self, x, y, WIDTH, HEIGHT)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.winner = False # критерий выигрыша на уровне
        self.up = self.left = self.right = self.running = False

        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
#        Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
#        Анимация движения влево        
        boltAnim = []
        boltAnimSuperSpeed = [] 
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        # Анимация стою на месте
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим
                
        # Анимация прыжок на лево
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
                
        # Анимация прыжок на право
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
                
        # Анимация прыжок просто
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def handleEvent(self, e) -> None:
        if e.type == KEYDOWN and e.key == K_UP:
            self.up = True
        if e.type == KEYUP and e.key == K_UP:
            self.up = False

        if e.type == KEYDOWN and e.key == K_LEFT:
            self.left = True
        if e.type == KEYUP and e.key == K_LEFT:
            self.left = False

        if e.type == KEYDOWN and e.key == K_RIGHT:
            self.right = True
        if e.type == KEYUP and e.key == K_RIGHT:
            self.right = False

        if e.type == KEYDOWN and e.key == K_LSHIFT:
            self.running = True
        if e.type == KEYUP and e.key == K_LSHIFT:
            self.running = False

    def update(self, platforms):
        if self.up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if self.running and (self.left or self.right): # если есть ускорение и мы движемся
                        self.yvel -= JUMP_EXTRA_POWER # то прыгаем выше
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        if self.left:
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image.fill(Color(COLOR))
            if self.running: # если ускорение
                    self.xvel-=MOVE_EXTRA_SPEED # то передвигаемся быстрее
                    if not self.up: # и если не прыгаем
                        self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0)) # то отображаем быструю анимацию
            else: # если не бежим
                if not self.up: # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0)) # отображаем анимацию движения 
            if self.up: # если же прыгаем
                    self.boltAnimJumpLeft.blit(self.image, (0, 0)) # отображаем анимацию прыжка

        if self.right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            if self.running:
                self.xvel+=MOVE_EXTRA_SPEED
                if not self.up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not self.up:
                    self.boltAnimRight.blit(self.image, (0, 0)) 
            if self.up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not(self.left or self.right): # стоим, когда нет указаний идти
            self.xvel = 0
            if not self.up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False; # Мы не знаем, когда мы на земле((   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster): # если пересакаемый блок - blocks.BlockDie или Монстр
                    self.die() # умираем
                elif isinstance(p, blocks.BlockTeleport): # портал
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.Princess): # если коснулись принцессы
                    self.winner = True # победили!!!
                else:
                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0                 # и энергия прыжка пропадает

                    
    def die(self):
            time.wait(1000)
            self.teleporting(self.startX, self.startY) # перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
            self.rect.x = goX
            self.rect.y = goY
