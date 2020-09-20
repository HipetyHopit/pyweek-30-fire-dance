"""@package run

Run the game.
"""

import pyglet
from gameWindow import GameWindow

if (__name__ == "__main__"):
    
    eventLoop = pyglet.app.EventLoop()
    window = GameWindow(eventLoop)
    
    eventLoop.run()
