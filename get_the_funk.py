#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import pygame


class BeamerToLight:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 80*16, 80*9
        self.fullscreen = False

    def display_window(self):
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption("c't Beamer to Light")

    def display_fullscreen(self):
        self._display_surf = pygame.display.set_mode((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

    def init(self):
        pygame.init()
        self.display_window()
        return True

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.VIDEORESIZE:
            self.size = self.width, self.height = event.size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.display_fullscreen()
                else:
                    self.display_window()
            else:
                print(event)

    def loop(self):
        pass

    def render(self):
        pass

    def cleanup(self):
        pygame.quit()

    def execute(self):
        self._running = self.init()

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        self.cleanup()


if __name__ == "__main__":
    application = BeamerToLight()
    application.execute()
