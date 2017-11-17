#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import pygame
import animations
import effects
from moods import *
from time import time


class BeamerToLight:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 60*16, 60*9
        self.fullscreen = False
        self.animation_pos = 0.0
        self.effect_animation_pos = 0.0
        self.current_mood = gray
        self.beat = [5.0]
        self.beat_valid = False
        self.last_beat_pressed_time = None
        self.last_beat = time()
        self.last_frame_time = time()
        self.animation = animations.point_circle
        self.animation_direction = 1

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
        elif event.type == pygame.VIDEORESIZE:
            self.size = self.width, self.height = event.size
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.display_fullscreen()
                else:
                    self.size = self.width, self.height = 60*16, 60*9
                    self.display_window()
            elif event.key == pygame.K_F5:
                if self.fullscreen:
                    self.display_fullscreen()
                else:
                    self.display_window()
            elif event.key == pygame.K_RETURN:
                if self.last_beat_pressed_time:
                    if not self.beat_valid:
                        print("Now i have a new delta so i'm deleting the previous times.")
                        self.beat = []
                    self.beat.append(time() - self.last_beat_pressed_time)
                    self.beat_valid = True
                else:
                    self.beat_valid = False
                    print("Now i have a now time but no delta.")
                self.last_beat_pressed_time = time()
                print(self.beat_valid)
                print(self.beat)
            elif event.scancode == 24:
                self.current_mood = gray
            elif event.scancode == 25:
                self.current_mood = fire
            elif event.scancode == 26:
                self.current_mood = water
            elif event.scancode == 38:
                self.animation = animations.single_circle
            elif event.scancode == 39:
                self.animation = animations.horizontal_line
            elif event.scancode == 40:
                self.animation = animations.vertical_line
            elif event.scancode == 41:
                self.animation = animations.double_wave
            elif event.scancode == 42:
                self.animation = animations.bony_horizontal_line
            elif event.scancode == 43:
                self.animation = animations.point_circle
            elif event.scancode == 44:
                self.animation = animations.point_circle_10
            elif event.scancode == 45:
                self.animation = animations.rotating_bone_1
            else:
                print(event)
        #else:
        #    print(event)

    def loop(self):
        now = time()
        elapsed_time = now - self.last_frame_time
        beat = sum(self.beat) / len(self.beat)
        if self.last_beat_pressed_time and self.beat_valid and now > self.last_beat_pressed_time + 2 * beat:
            print("Invalidated Beat")
            self.last_beat_pressed_time = None
        if now >= self.last_beat + beat:
            self.last_beat += beat
            self.animation_direction *= -1
        self.animation_pos = (self.animation_pos + self.animation_direction * elapsed_time / beat) % 1
        self.effect_animation_pos = (self.effect_animation_pos + elapsed_time / (beat * 4)) % 1
        self.last_frame_time = now

    def render(self):
        surface = pygame.display.get_surface()
        surface.fill((0, 0, 0))
        self.animation(surface, self.animation_pos, self.current_mood)
        self.apply_effects(surface)
        pygame.display.flip()

    def apply_effects(self, surface):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            effects.flash(surface, self.effect_animation_pos)
        elif keys[252]:
            effects.wave(surface, self.effect_animation_pos)

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
