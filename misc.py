import pygame
import random
import math

WHITE = (255,255,255)
BLACK = (0,0,0)
LEFT = 1
DEBUG = True

WIDTH = 2000
HEIGHT = 2000
G = 1.e4
t = 0.0
dt = 0.1

def debug(str):
	if DEBUG:
		print(str)

def random_color(thresh_red=(0,255), thresh_green=(0,255), thresh_blue=(0,255)):
	r = random.randint(thresh_red[0], thresh_red[1])
	g = random.randint(thresh_green[0], thresh_green[1])
	b = random.randint(thresh_blue[0], thresh_blue[1])
	return (r,g,b)

def refresh(pywindow, bodies):
	for b in bodies:
		b.draw(pywindow)
	pygame.display.update()

def distance(pos_a, pos_b):
	dx = pos_b._x - pos_a._x
	dy = pos_b._y - pos_a._y
	sqd = dx*dx + dy*dy
	return math.sqrt(sqd)

def newt_uni_attraction(m1, m2, r):
	return (G*m1*m2)/(r*r)



class Vector2D:
	def __init__(self, pos):
		self._x = pos[0]
		self._y = pos[1]

class Koefficient:
	def __init__(self, dx, dy, dvx, dvy):
			self._dx = dx
			self._dy = dy
			self._dvx = dvx
			self._dvy = dvy
