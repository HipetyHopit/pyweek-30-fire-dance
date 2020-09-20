"""@package character

Character class.
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key

# Game constants.
SPRITE_SCALING = 4
GRAVITY = 0

# Path constants.
SPRITE_PATH = "data/images/sprites/"

# OpenGl
glEnable(GL_TEXTURE_2D)

class Character(pyglet.sprite.Sprite):
    """ Character class. """
    
    def __init__(self, name):
        
        # Load resources
        image = pyglet.image.load(SPRITE_PATH + name + ".png")
        spriteSheet = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 2, 1))
        
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST) 
        spriteSheet[0].width *= SPRITE_SCALING
        spriteSheet[0].height *= SPRITE_SCALING
        
        super(Character, self).__init__(spriteSheet[0])
        
        # Attributes.
        self.MOVE_SPEED = 200 # px/s
        self.ACCELERATION = 200 # px/s^2
        self.v_x = 0.0
        self.v_y = 0.0
        
    def update(self, dt, gameState):
        
        if (gameState["keys"][key.UP]):
            self.v_y += self.ACCELERATION*dt
        if (gameState["keys"][key.DOWN]):
            self.v_y -= self.ACCELERATION*dt
        if (gameState["keys"][key.LEFT]):
            self.v_x -= self.ACCELERATION*dt
        if (gameState["keys"][key.RIGHT]):
            self.v_x += self.ACCELERATION*dt
         
        if (abs(self.v_x) > self.MOVE_SPEED):
            self.v_x *= self.MOVE_SPEED/abs(self.v_x)
         
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        
