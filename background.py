"""@package background

The background image.
"""

import pyglet
from constants import *

class Background(pyglet.sprite.Sprite):
    """ Background class. """
    
    def __init__(self):
        """ Constuctor. """
        
        # Load resources
        image = pyglet.image.load(IMAGE_PATH + "island.png")
        grid = pyglet.image.ImageGrid(image, 1, 4)
        spriteSheet = pyglet.image.TextureGrid(grid)
        animation = pyglet.image.Animation.from_image_sequence(spriteSheet, 
                                                       duration = 0.3, 
                                                       loop = True)
        
        super(Background, self).__init__(animation)
        
        # Colour.
        self.color = BLACK[:3]
        self.newColour = BLACK[:3]
        self.oldColour = BLACK[:3]
        self.fade = 1.
        
    def update(self, dt):
        """ Update background. """
        
        if (self.fade < 1.):
            self.fade += FADE_RATE*dt
            if (self.fade > 1.):
                self.fade = 1
            R = int(self.newColour[0]*self.fade+self.oldColour[0]*(1-self.fade))
            G = int(self.newColour[1]*self.fade+self.oldColour[1]*(1-self.fade))
            B = int(self.newColour[2]*self.fade+self.oldColour[2]*(1-self.fade))
            self.color = (R, G, B)
        else:
            #self.color = self.newColour
            self.fade = 1.
            
    def setFade(self, colour):
        """
        Set colour to fade to.
        
        Keyword arguments:
        colour -- RGB colour tupple.
        """
        
        self.oldColour = self.color
        self.newColour = colour
        self.fade = 0.
