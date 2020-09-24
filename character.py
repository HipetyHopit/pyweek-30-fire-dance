"""@package character

Character class.
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key
from constants import *

# OpenGl
glEnable(GL_TEXTURE_2D)

class Character(pyglet.sprite.Sprite):
    """ Character class. """
    
    def __init__(self, name, numStates = 1, x = 0, y = GROUNDLEVEL):
        
        # Load resources
        image = pyglet.image.load(SPRITE_PATH + name + ".png")
        self.spriteSheet = pyglet.image.TextureGrid(
            pyglet.image.ImageGrid(image, 4, numStates))
        
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST) 
        for i in range(len(self.spriteSheet)):
            self.spriteSheet[i].width *= SPRITE_SCALING
            self.spriteSheet[i].height *= SPRITE_SCALING
            
        self.animations = []
        for i in range(4):
            animation = pyglet.image.Animation.from_image_sequence(
                self.spriteSheet[i*numStates:(i+1)*numStates], duration = 0.2, 
                loop = True)
            self.animations += [animation]
        
        super(Character, self).__init__(self.animations[3])
        
        # Attributes.
        self.x = x
        self.y = y
        self.v_x = 0.0
        self.v_y = 0.0
        self.direction = 3
        self.state = 0
        
    def update(self, dt):
         
        self.x += self.v_x*dt
        self.y += self.v_y*dt
        
        self.v_y -= GRAVITY*dt
        
        if (self.v_y > 0 and self.direction != 1):
            self.setDirection(1)
        elif (self.v_y < -50. and self.direction != 2):
            self.setDirection(2)
        
        if (self.y < GROUNDLEVEL):
            self.v_y = 0.
            self.y = GROUNDLEVEL
        
    def set_v(self, v_x, v_y):
        
        self.v_x = v_x
        if (self.y == GROUNDLEVEL):
            self.v_y = v_y
        
    def setDirection(self, direction):
        
        self.direction = direction % 4
        self.image = self.animations[self.direction]
