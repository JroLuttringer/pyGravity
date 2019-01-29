from misc import *
from collections import deque

density = 0.001


class body:
    def __init__(self, pos, density=0.001, type=PLANET):
        self._density = density
        self._pos = pos
        self._radius = 1.5
        self._mass = compute_mass(self._radius, density)
        self._vel = Vector2D((0.0, 2.0))
        self._type = type
        self._old_pos = deque([self._pos])
        self._orbit_color = random_color()
        self._curs = 1
        if type == PLANET:
            self._color = WHITE
        elif type == SUN:
            self._color = RED
            self._mass *= 1000
            self._radius = compute_radius(self._mass, density)
        debug("new bodies")

    def acceleration(self, all_bodies, alt_ref=None):
        ax = 0.0
        ay = 0.0
        pos = self._pos
        if alt_ref is not None:
            pos = alt_ref
        for b in all_bodies:
            if b is self:
                continue
            r = distance(pos, b._pos)
            force = newt_uni_attraction(self._mass, b._mass, r)
            ax += force * (b._pos._x - pos._x) / r
            ay += force * (b._pos._y - pos._y) / r
        return Vector2D((ax, ay))

    def first_k(self, bodies):
        a = self.acceleration(bodies)
        return Koefficient(self._vel._x, self._vel._y, a._x, a._y)

    def next_k(self, koef, t, dt, bodies):
        x = self._pos._x + koef._dx * dt
        y = self._pos._y + koef._dy * dt
        vx = self._vel._x + koef._dvx * dt
        vy = self._vel._y + koef._dvy * dt
        a = self.acceleration(bodies, alt_ref=Vector2D((x, y)))
        return Koefficient(vx, vy, a._x, a._y)

    def set_new_position(self, bodies):
        if self._type == SUN:
            return
        k1 = self.first_k(bodies)
        k2 = self.next_k(k1, t, dt * 0.5, bodies)
        k3 = self.next_k(k2, t, dt * 0.5, bodies)
        k4 = self.next_k(k3, t, dt, bodies)
        add_x = 1.0 / 6.0 * (k1._dx + 2.0 * (k2._dx + k3._dx) + k4._dx)
        add_y = 1.0 / 6.0 * (k1._dy + 2.0 * (k2._dy + k3._dy) + k4._dy)
        add_vx = 1.0 / 6.0 * (k1._dvx + 2.0 * (k2._dvx + k3._dvx) + k4._dvx)
        add_vy = 1.0 / 6.0 * (k1._dvy + 2.0 * (k2._dvy + k3._dvy) + k4._dvy)
        #self._curs = (self._curs + 1) % MAX_TRAIL
        self._old_pos.append(Vector2D((self._pos._x, self._pos._y)))
        if len(self._old_pos) > MAX_TRAIL:
            # self._old_pos.rotate(1)
            self._old_pos.popleft()

        self._pos._x += add_x * dt
        self._pos._y += add_y * dt
        self._vel._x += add_vx * dt
        self._vel._y += add_vy * dt

    def touch(self, body):
        return distance(self._pos, body._pos) <= (self._radius * 10 + body._radius * 10)

    def merge(self, body, bodies):
        if self._mass >= body._mass:
            big_body = self
            small_body = body
        else:
            big_body = body
            small_body = smell
        vx = (big_body._vel._x * big_body._mass + small_body._vel._x *
              small_body._mass) / (small_body._mass + big_body._mass)
        vy = (big_body._vel._y * big_body._mass + small_body._vel._y *
              small_body._mass) / (small_body._mass + big_body._mass)
        big_body._mass += small_body._mass
        big_body._radius = compute_radius(big_body._mass, density)
        big_body._color = merge_color(big_body._color, small_body._color,
                                      big_body._mass / small_body._mass)
        big_body._orbit_color = merge_color(
            big_body._orbit_color, small_body._orbit_color, big_body._mass / small_body._mass)
        big_body._vel._x = vx
        big_body._vel._y = vy
        bodies.remove(small_body)

    def check_collision(self, bodies):
        for b in bodies:
            if b is self:
                continue
            if self.touch(b):
                self.merge(b, bodies)

    def draw(self, pywindow, bodies):
        if self._type == SUN:
            self._color = (self._color[0], (self._color[1] + 0.30) % 255, self._color[2])
            for b in bodies:
                pygame.draw.line(pywindow, b._orbit_color,
                                 self._pos.to_tuple(), b._pos.to_tuple(), 1)
        for i in range(len(self._old_pos) - 1, 0, -1):
            from_point = self._old_pos[i]
            to_point = self._old_pos[(i - 1)]
            if from_point is None:
                break
            if to_point is None:
                break
            pygame.draw.line(pywindow, self._orbit_color, from_point.to_tuple(),
                             to_point.to_tuple(), int(i / 5 * self._radius))
        pygame.draw.circle(pywindow, self._color, (int(self._pos._x), int(
            self._pos._y)), int(self._radius * 10), int(self._radius * 10))
