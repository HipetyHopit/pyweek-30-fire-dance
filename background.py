"""@package background

The background image.
"""

import pyglet
from arrows import IMAGE_PATH

image = pyglet.image.load(IMAGE_PATH + "island.png")
spriteSheet = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 1, 1))
animation = pyglet.image.Animation.from_image_sequence(spriteSheet, 
                                                       duration = 0.1, 
                                                       loop = True)
backgroundSprite = pyglet.sprite.Sprite(animation)
