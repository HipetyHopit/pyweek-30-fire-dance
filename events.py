"""@package events

Schedule events.
"""

import pyglet
from numpy.random import poisson

class MarkovEvent:
    """ An event that occurs according to a Markov process. """
    
    def __init__(self, intervalExpectation):
        """
        Initialize.
        
        Keyword arguments:
        intervalExpectation -- the expected interval between event 
            occurences (s).
        """
        
        self.intervalExpectation = intervalExpectation
        T = poisson(self.intervalExpectation)
        pyglet.clock.schedule_once(self.execute, T)
        
    def execute(self, dt):
        """ Callback function for scheduled event. """
        
        T = poisson(self.intervalExpectation)
        pyglet.clock.schedule_once(self.execute, T)
