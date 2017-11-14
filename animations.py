#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from pygame.gfxdraw import aacircle, filled_circle
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
