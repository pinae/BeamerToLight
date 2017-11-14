#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import pygame
from animations import single_circle
from moods import gray, fire, water
from time import time


class BeamerToLight:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 60*16, 60*9
        self.fullscreen = False
        self.animation_pos = 0.0
        self.current_mood = gray
        self.beat = 1.0
        self.last_frame_time = time()

    def display_window(self):
        self._display_surf = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption("c't Beamer to Light")

    def display_fullscreen(self):
        modes = pygame.display.list_modes()
        modes.sort(key=lambda x: x[0]+x[1], reverse=True)
        self._display_surf = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
        self.size = self.width, self.height = modes[0]

    def init(self):
        pygame.init()
        self.display_window()
        return True

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.VIDEORESIZE:
            self.size = self.width, self.height = event.size
            print(self.size)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.display_fullscreen()
                else:
                    self.size = self.width, self.height = 60*16, 60*9
                    self.display_window()
            else:
                print(event)

    def loop(self):
        now = time()
        elapsed_time = now - self.last_frame_time
        self.animation_pos = (self.animation_pos + elapsed_time / self.beat) % 1
        self.last_frame_time = now

    def render(self):
        surface = pygame.display.get_surface()
        surface.fill((0, 0, 0))
        single_circle(surface, self.animation_pos, self.current_mood)
        pygame.display.flip()

    @staticmethod
    def cleanup():
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
