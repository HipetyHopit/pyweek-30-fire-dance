"""@package mainLoop

Event loop class.
"""

import pyglet
        
class MainLoop(pyglet.app.EventLoop):
    """ Main loop class. """
    
    def __init__(self):
        
        super(MainLoop, self).__init__()
        
    def on_window_close(window):
        print ("Exit")
        self.exit()
