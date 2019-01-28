from misc import *
from tkinter import *
from bodies import *

def init_window():
	pygame.init()
	pywindow = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Graph')
	pywindow.fill(BLACK)
	return pywindow


def no_graphic_main():
	pass


def main():
	pywindow = init_window()
	celestial_bodies = []
	adjusted = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				debug("event detected")
				mouse_pos = Vector2D(pygame.mouse.get_pos())
				if event.button == 1:
					debug("event mouse left")
					celestial_bodies.append(body(mouse_pos))

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		first = False
		for c in celestial_bodies:
			if not first:
				first = True
				if not adjusted:
					c._color = (255,0,0)
					c._mass *= 1000
					c._radius += 1.5
					adjusted = True
				continue
			c.set_new_position(celestial_bodies)

		refresh(pywindow,celestial_bodies)






if __name__ == "__main__":
    main()
