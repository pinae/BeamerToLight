#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import pygame
import animations
import effects
from moods import *
from time import time


class BeamerAsLight:
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
        self.unknown_keys_dict = {}

    def display_window(self):
        self._display_surf = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption("c't Beamer as Light")

    def display_fullscreen(self):
        modes = pygame.display.list_modes()
        modes.sort(key=lambda x: x[0]+x[1])
        self._display_surf = pygame.display.set_mode(modes[-1], pygame.FULLSCREEN)
        self.size = self.width, self.height = modes[-1]

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
                        print("New time and new delta: Deleting the previous times.")
                        self.beat = []
                    self.beat.append(time() - self.last_beat_pressed_time)
                    self.beat_valid = True
                else:
                    self.beat_valid = False
                    print("New time but no delta.")
                self.last_beat_pressed_time = time()
                print(self.beat_valid)
                print(self.beat)
            elif event.key == 9:
                self.animation_direction = -1 * self.animation_direction
            elif event.scancode == 20:
                self.beat = [2 * b for b in self.beat]
            elif event.scancode == 61:
                self.beat = [0.5 * b for b in self.beat]
            elif event.scancode == 24:
                self.current_mood = gray
            elif event.scancode == 25:
                self.current_mood = fire
            elif event.scancode == 26:
                self.current_mood = water
            elif event.scancode == 27:
                self.current_mood = green
            elif event.scancode == 28:
                self.current_mood = yellow
            elif event.scancode == 29:
                self.current_mood = pink
            elif event.scancode == 30:
                self.current_mood = red
            elif event.scancode == 31:
                self.current_mood = bluered
            elif event.scancode == 32:
                self.current_mood = yellowpink
            elif event.scancode == 33:
                self.current_mood = brown
            elif event.scancode == 34:
                self.current_mood = cyan
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
            elif event.scancode == 46:
                self.animation = animations.rotating_bones
            elif event.scancode == 47:
                self.animation = animations.rotating_bone_circle
            elif event.scancode == 48:
                self.animation = animations.snow
            elif event.scancode == 51:
                pass
            else:
                if event.scancode not in self.unknown_keys_dict:
                    self.unknown_keys_dict[event.scancode] = event.key

    def loop(self):
        now = time()
        elapsed_time = now - self.last_frame_time
        beat = sum(self.beat) / len(self.beat)
        keys = pygame.key.get_pressed()
        if keys[313] or keys[301]:
            beat = 2*beat
        if keys[304]:
            beat = beat/2
        if keys[306]:
            beat = beat/4
        if self.last_beat_pressed_time and self.beat_valid and now > self.last_beat_pressed_time + 2 * beat:
            print("Invalidated Beat")
            self.last_beat_pressed_time = None
        if now >= self.last_beat + beat:
            self.last_beat += beat
            self.animation_direction *= -1
        if not keys[308]:
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
        elif 52 in self.unknown_keys_dict and keys[self.unknown_keys_dict[52]]:
            surface.fill((0, 0, 0))
            effects.wave(surface, self.effect_animation_pos)
        elif 53 in self.unknown_keys_dict and keys[self.unknown_keys_dict[53]]:
            effects.wave(surface, self.effect_animation_pos)
        elif 54 in self.unknown_keys_dict and keys[self.unknown_keys_dict[54]]:
            surface.fill((0, 0, 0))
            effects.snowflakes(surface, self.effect_animation_pos)
        elif 55 in self.unknown_keys_dict and keys[self.unknown_keys_dict[55]]:
            effects.snowflakes(surface, self.effect_animation_pos)

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
    application = BeamerAsLight()
    application.execute()
