"""@package arrows

Arrow class.
"""

import pyglet

# Path constants.
IMAGE_PATH = "data/images/"


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
        
    def update(self, dt):
        
        self.y -= self.v * dt
        
    def updateState(self, state):
        
        self.state = state
        self.image = self.spriteSheet[(self.state, self.orientation)]
