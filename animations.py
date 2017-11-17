#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from pygame.gfxdraw import aacircle, filled_circle, bezier
from math import sqrt


def single_circle(surface, progress, mood):
    width, height = surface.get_size()
    r = int(progress*(sqrt((width/2)**2+(height/2)**2)+width//20))
    w = width//20
    aacircle(surface, width//2, height//2, r, mood.primary_color)
    filled_circle(surface, width//2, height//2, r, mood.primary_color)
    if r-w > 0:
        aacircle(surface, width//2, height//2, r-w, (0, 0, 0))
        filled_circle(surface, width//2, height//2, r-w, (0, 0, 0))


def horizontal_line(surface, progress, mood):
    width, height = surface.get_size()
    w = width // 20
    pos = int(progress*(height+2*w))
    surface.fill(mood.primary_color, (0, pos-w, width, min(pos, w)))


def vertical_line(surface, progress, mood):
    width, height = surface.get_size()
    w = width // 20
    pos = int(progress*(width+2*w))
    surface.fill(mood.primary_color, (pos-w, 0, min(pos, w), height))


def double_wave(surface, progress, mood):
    width, height = surface.get_size()
    w = width // 20
    for i in range(w):
        bezier(surface, [
            (int((-progress+0.25) % 1 * width), height // 2 + i),
            (int((-progress+0.25) % 1 * width + width / 2), i),
            (int((-progress+0.25) % 1 * width + width / 2), height + i),
            (int((-progress+0.25) % 1 * width + width), height // 2 + i)
        ], 16, mood.secondary_color)
        bezier(surface, [
            (int((-progress+0.25) % 1 * width - width), height // 2 + i),
            (int((-progress+0.25) % 1 * width - width / 2), i),
            (int((-progress+0.25) % 1 * width - width / 2), height + i),
            (int((-progress+0.25) % 1 * width), height // 2 + i)
        ], 16, mood.secondary_color)
    for i in range(w):
        bezier(surface, [
            (int(progress * width), height // 2 + i),
            (int(progress * width + width / 2), i),
            (int(progress * width + width / 2), height + i),
            (int(progress * width + width), height // 2 + i)
        ], 16, mood.primary_color)
        bezier(surface, [
            (int(progress * width - width), height // 2 + i),
            (int(progress * width - width / 2), i),
            (int(progress * width - width / 2), height + i),
            (int(progress * width), height // 2 + i)
        ], 16, mood.primary_color)
