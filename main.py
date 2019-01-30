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

    pause = False
    max_mass = None

    while True:
        added_bodies = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                debug("event detected")
                mouse_pos = Vector2D(pygame.mouse.get_pos())
                if event.button == 1:
                    debug("event mouse left")
                    if len(celestial_bodies) == 0:
                        celestial_bodies.append(body(mouse_pos, type=SUN))
                    else:
                        celestial_bodies.append(body(mouse_pos))
                elif event.button == 3:
                    debug("event mouse right")
                    celestial_bodies.append(body(mouse_pos, type = SUN))
                added_bodies = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    debug("SPACE __ PAUSED")
                    pause = not pause

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not pause:
            for c in celestial_bodies:
                c.set_new_position(celestial_bodies, max_mass)
            for c in celestial_bodies:
                collision = c.check_collision(celestial_bodies)
                if collision:
                    added_bodies = True

        if added_bodies:
            new_mass = update_center(celestial_bodies, max_mass)
            if new_mass is not None:
                debug("max mass changed " + str(new_mass))
                max_mass = new_mass
                center_window(pywindow, celestial_bodies, max_mass, pause)


        refresh(pywindow, celestial_bodies, pause)


if __name__ == "__main__":
    main()
