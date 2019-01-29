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
G = 1.e4
t = 0.0
dt = 3

SUN = 0
PLANET = 1
MAX_TRAIL = 100


def debug(str):
    if DEBUG:
        print(str)


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


def refresh(pywindow, bodies):
    pywindow.fill(BLACK)
    for b in bodies:
        b.draw(pywindow, bodies)
    pygame.display.update()


def distance(pos_a, pos_b):
    dx = pos_b._x - pos_a._x
    dy = pos_b._y - pos_a._y
    sqd = dx * dx + dy * dy
    return math.sqrt(sqd)


def newt_uni_attraction(m1, m2, r):
    return (G * m1 * m2) / (r * r)

def merge_color(colora, colorb, weight):
    r = (colora[0]*weight + colorb[0])/2
    g = (colora[1]*weight + colorb[1])/2
    b = (colora[2]*weight + colorb[2])/2
    r = min(r,255)
    g = min(g,255)
    b = min(b,255)
    colorc = (int(r),int(g),int(b))
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
