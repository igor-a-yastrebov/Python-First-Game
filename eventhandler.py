#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame
from player import *

class EventHandler(object):
    def __init__(self, hero):
        self.up = self.left = self.right = self.running = False
        self.hero = hero

    def handleEvents(self, platforms) -> int:
        for e in pygame.event.get(): # Обрабатываем события друг за другом
            if self.handleEvent(e) == QUIT:
                return QUIT
        self.dispatchEvents(platforms)

    def handleEvent(self, e) -> int:
        # сделал криво, не разобрался. Сейчас логика обработки клавиатуры сохраняется тут,
        # а надо тупо перенаправлять события в нужные объекты, чтобы сами объекты себя маняли нужным образом
        # в конце можно вызвать update(), или придумать что-то более элегантное
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

        if e.type == QUIT:
            return QUIT

    def dispatchEvents(self, platforms) -> None:
        self.hero.update(self.left, self.right, self.up, self.running, platforms)   # передвижение персонажа