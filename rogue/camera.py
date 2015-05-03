from collections import namedtuple
from rect import Rect
from debug import debug

class Camera(object):
    """ Draws the current view to the main game screen.

    Attributes:
    view -- Rect containing the current view of the camera
    """

    def __init__(self, x=0, y=0, width=51, height=15):
        self.view = Rect(x, y, width, height)

    def draw(self, window, world):
        """ Render world tiles and then entities to window.

        Keyword arguments:
        window -- current curses window (or screen) object
        world -- current game World object
        """

        for x in range(self.view.width):
            for y in range(self.view.height):
                window.addch(y, x, ord(world.get_tile(x+self.view.x, y+self.view.y)))

        for entity in world.entities:
            if self.is_visible(entity):
                pos = self.world_to_screen(entity.x, entity.y)
                window.addch(pos.y, pos.x, ord(str(entity)))

    def world_to_screen(self, x, y):
        """ Transform world coordinates to screen coordinates.

        Returns a namedtuple Point (x, y) where x and y are the
        screen coordinates. """
        Point = namedtuple("Point", ['x', 'y'])
        return Point(x - self.view.x, y - self.view.y)

    def screen_to_world(self, x, y):
        """ Transform screen coordinates to world coordinates.

        Returns a namedtuple Point (x, y) where x and y are the
        screen coordinates. """
        Point = namedtuple("Point", ['x', 'y'])
        return Point(x + self.view.x, y + self.view.y)

    def center_on(self, entity):
        """ Center camera view on entity object. """
        self.view.x = entity.x - int(self.view.width/2)
        self.view.y = entity.y - int(self.view.height/2)

    def is_visible(self, entity):
        """ True if entity is onscreen. """
        if (self.view.x < entity.x < self.view.x + self.view.width or
            self.view.y < entity.y < self.view.y + self.view.height):
            return True
        else:
            return False
