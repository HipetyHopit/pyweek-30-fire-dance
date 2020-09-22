"""@package arrows

Arrow class.
"""

import pyglet
from constants import *

class Arrow(pyglet.sprite.Sprite):
    """ Arrow class. """
    
    def __init__(self, x, y, orientation, state = 0, v = 0.):
        
        # Load resources
        image = pyglet.image.load(IMAGE_PATH + "arrows.png")
        self.spriteSheet = pyglet.image.ImageGrid(image, 3, 4)
        
        super(Arrow, self).__init__(self.spriteSheet[(state, orientation)])
        
        self.v = v
        self.x = x
        self.y = y
        self.state = state
        self.orientation = orientation
        self.active = True
        
    def update(self, dt):
        """ Update the arrow. """
        
        self.y += self.v * dt
        
    def draw(self):
        """ Draw the arrow. """
        
        if (self.active):
            pyglet.sprite.Sprite.draw(self)
        
    def updateState(self, state):
        """
        Set the arrow's state.
        
        Keyword arguments:
        state -- the new state.
        """
        
        self.state = state
        self.image = self.spriteSheet[(self.state, self.orientation)]
        
    def getCollide(self, target):
        """
        Check if the arrow collides with another arrow.
        
        Keyword arguments:
        target -- the arrow to check collision with.
        """
        
        # Arrows should only collide on the same track.
        if (self.x == target.x and target.active):
            if (abs(self.y - target.y) < self.height):
                return True
            
        return False
    
    def deactivate(self):
        """ Deactivate the arrow. """
        
        self.active = False
