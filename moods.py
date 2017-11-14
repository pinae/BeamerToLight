#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals


class Mood:
    def __init__(self, color1=(255, 255, 255), color2=(128, 128, 128)):
        self.primary_color = color1
        self.secondary_color = color2


fire = Mood((255, 0, 0), (255, 210, 0))
water = Mood((0, 0, 255), (0, 234, 255))
gray = Mood((255, 255, 255), (128, 128, 128))
