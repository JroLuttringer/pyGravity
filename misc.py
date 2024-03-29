import pygame
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LEFT = 1
DEBUG = True

WIDTH = 3000
HEIGHT = 2000
G = 8e3
t = 0.0
dt = 3

SUN = 0
PLANET = 1
MAX_TRAIL = 100

def sign(a):
    if a < 0:
        return -1
    elif a > 0:
        return 1
    else:
        return 0

def update_center(bodies, max_mass):
    i = 0
    if max_mass is None:
        return bodies[0]

    #debug('current max mass ' + str(bodies[max_mass]._mass))
    for b in bodies:
        debug(b._mass)
        if b._mass > max_mass._mass:
            return b
        i += 1
    return None

def center_window(pywindow, bodies, center, pause):
    mid_x = int(WIDTH/2)
    mid_y = int(HEIGHT/2)
    while abs(center._pos._x - mid_x) > 10 or abs(center._pos._y - mid_y) > 10:
        x_shift = sign(mid_x - center._pos._x)
        y_shift = sign(mid_y - center._pos._y)
        for b in bodies:
            b._pos._x += x_shift*9
            b._pos._y += y_shift*9
        refresh(pywindow,bodies,True)




def debug(str):
    if DEBUG:
        print(str)

def draw_pause_symbol(pywindow):
    pygame.draw.rect(pywindow, WHITE, [10,10,80,200])
    pygame.draw.rect(pywindow, WHITE, [110,10,85,200])


def compute_radius(mass, density):
    return (3.0 * mass / (density * 4.0 * math.pi)) ** (0.3333)


def compute_mass(radius, density):
    return density * 4.0 * math.pi * (radius**3.0) / 3.0


def random_color(thresh_red=(0, 255), thresh_green=(0, 255), thresh_blue=(0, 255)):
    r = random.randint(thresh_red[0], thresh_red[1])
    g = random.randint(thresh_green[0], thresh_green[1])
    b = random.randint(thresh_blue[0], thresh_blue[1])
    return (r, g, b)


def draw_grid(pywindow):
    for x in range(0, WIDTH, 100):
        pygame.draw.line(pywindow, WHITE, (x, HEIGHT), (x, 0), 1)

    for y in range(0, HEIGHT, 100):
        pygame.draw.line(pywindow, WHITE, (0, y), (WIDTH, y), 1)


def refresh(pywindow, bodies, pause):
    pywindow.fill(BLACK)
    for b in bodies:
        b.draw(pywindow, bodies, pause)
    if pause:
        draw_pause_symbol(pywindow)
    pygame.display.update()


def distance(pos_a, pos_b):
    dx = pos_b._x - pos_a._x
    dy = pos_b._y - pos_a._y
    sqd = dx * dx + dy * dy
    return math.sqrt(sqd)


def newt_uni_attraction(m1, m2, r):
    return (G * m1 * m2) / (r * r)


def merge_color(colora, colorb, weight):
    r = (colora[0] * weight + colorb[0]) / 2
    g = (colora[1] * weight + colorb[1]) / 2
    b = (colora[2] * weight + colorb[2]) / 2
    r = min(r, 255)
    g = min(g, 255)
    b = min(b, 255)
    colorc = (int(r), int(g), int(b))
    print("{} {} {}".format(colora, colorb, colorc))
    return colorc


class Vector2D:
    def __init__(self, pos):
        self._x = pos[0]
        self._y = pos[1]

    def to_tuple(self):
        return (self._x, self._y)

    def __str__(self):
        return "" + self._x + ";" + self._y


class Koefficient:
    def __init__(self, dx, dy, dvx, dvy):
        self._dx = dx
        self._dy = dy
        self._dvx = dvx
        self._dvy = dvy
