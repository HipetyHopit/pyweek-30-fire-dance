"""@package GameWindow

Main game class.
"""

import pyglet
from pyglet.window import key
from pyglet.gl import *
from character import Character

# Turn off image scaling interpolation.
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

# Game constants.
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GAME_TITLE = "Untitled"

class GameWindow(pyglet.window.Window):
    """ Main game class. """
    
    def __init__(self, eventLoop):
        """
        Constructor. 
        
        Keyword arguments:
        eventLoop -- a handle for the application event loop.
        """
        
        super(GameWindow, self).__init__()

        # Window setup.
        #self.set_exclusive_mouse()
        self.set_mouse_visible(False)
        self.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_caption(GAME_TITLE)
        
        self.loopHandle = eventLoop
        
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        
        # Game setup.
        self.characters = [Character("coconut")]
        
        pyglet.clock.schedule_interval(self.update, 1./60.)
        
        self.gameState = {"keys": self.keys,
                          "characters": self.characters}
        
    def update(self, dt):
        """ Update game objects. """
        
        for c in self.characters:
           c.update(dt, self.gameState) 

    def on_draw(self):
        """ Handle draw events. """
        
        self.clear()
        
        # Draw characters.
        for c in self.characters:
           c.draw() 
        
    def on_key_press(self, symbol, modifiers):
        """ Handle key press events. """
        
        pass
            
    def on_key_release(self, symbol, modifiers):
        """ Handle key release events. """
        
        if (symbol == key.ESCAPE):
            self.loopHandle.exit()
            
    def on_close(self):
        """ Handle close event. """
        
        self.loopHandle.exit()
