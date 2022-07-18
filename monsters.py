#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

from blocks import BlockAnimated, BlockStatic

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_MONSTERHORYSONTAL = [ ('%s/monsters/fire1.png' % ICON_DIR, 300),
                                ('%s/monsters/fire2.png' % ICON_DIR, 300)]

class Monster(BlockAnimated):
    def __init__(self, x, y, left, up, maxLengthLeft,maxLengthUp):
        BlockAnimated.__init__(self, x, y, MONSTER_WIDTH, MONSTER_HEIGHT, ANIMATION_MONSTERHORYSONTAL)
        self.startX = x # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up # скорость движения по вертикали, 0 - не двигается

    def update(self, platforms): # по принципу героя

        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
               self.xvel = - self.xvel # то поворачиваем в обратную сторону
               self.yvel = - self.yvel
