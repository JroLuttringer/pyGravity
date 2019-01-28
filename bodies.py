from misc import *

class body:
	def __init__(self, pos, density=0.001):
		self._mass = density*4.0*math.pi*(1.5**3.0)/3.0
		self._density = density
		self._pos = pos
		self._radius = 1.5
		self._vel = Vector2D((0.0,3.0))
		self._color = WHITE
		debug("new bodies")

	def acceleration(self, all_bodies, alt_ref=None):
		ax = 0.0
		ay = 0.0
		pos = self._pos
		if alt_ref is not None:
			pos=alt_ref
		for b in all_bodies:
			if b is self:
				continue
			r = distance(pos, b._pos)
			force = newt_uni_attraction(self._mass, b._mass, r)
			ax += force*(b._pos._x - pos._x)/r
			ay += force*(b._pos._y - pos._y)/r
		return Vector2D((ax, ay))


	def first_k(self, bodies):
		a = self.acceleration(bodies)
		return Koefficient(self._vel._x, self._vel._y, a._x, a._y)

	def next_k(self, koef, t, dt, bodies):
		x = self._pos._x + koef._dx * dt
		y = self._pos._y + koef._dy * dt
		vx = self._vel._x + koef._dvx * dt
		vy = self._vel._y + koef._dvy * dt
		a = self.acceleration(bodies, alt_ref = Vector2D((x,y)))
		return Koefficient(vx, vy, a._x, a._y)

	def set_new_position(self, bodies):
		k1 = self.first_k(bodies)
		k2 = self.next_k(k1, t, dt*0.5, bodies)
		k3 = self.next_k(k2, t, dt*0.5, bodies)
		k4 = self.next_k(k3, t, dt, bodies)
		add_x = 1.0/6.0 * (k1._dx + 2.0*(k2._dx + k3._dx) + k4._dx)
		add_y = 1.0/6.0 * (k1._dy + 2.0*(k2._dy + k3._dy) + k4._dy)
		add_vx = 1.0/6.0 * (k1._dvx + 2.0 * (k2._dvx + k3._dvx) + k4._dvx)
		add_vy = 1.0/6.0 * (k1._dvy + 2.0 * (k2._dvy + k3._dvy) + k4._dvy)
		self._pos._x += add_x*dt
		self._pos._y += add_y*dt
		self._vel._x += add_vx*dt
		self._vel._y += add_vy*dt




	def draw(self, pywindow):
		pygame.draw.circle(pywindow, self._color, (int(self._pos._x), int(self._pos._y)), int(self._radius*10), int(self._radius*10))
