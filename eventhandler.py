#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame
from hero import *

class EventHandler(object):
    def __init__(self, hero):
        self.hero = hero

    def handleEvents(self) -> int:
        for e in pygame.event.get(): # Обрабатываем события друг за другом
            if self.handleEvent(e) == QUIT:
                return QUIT
    def handleEvent(self, e) -> int:
        if e.type == QUIT:
            return QUIT
        self.hero.handleEvent(e)
