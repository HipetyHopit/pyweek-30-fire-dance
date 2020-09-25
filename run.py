"""@package run

Run the game.
"""

import pyglet
from gameWindow import GameWindow

__version__ = "0.1"

if (__name__ == "__main__"):
    
    eventLoop = pyglet.app.EventLoop()
    window = GameWindow(eventLoop)
    
    eventLoop.run()
