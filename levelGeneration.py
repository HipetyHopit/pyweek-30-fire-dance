"""@package levelGeneration

Functions for level generation.
"""

import pyglet
from numpy.random import poisson
from beatTracking import getMoves
from arrows import Arrow
from constants import *

def getRandomMoves(duration, interval = 0.5):
    """
    Generate move times according to a Markov process.
    
    Keyword arguments:
    duration -- the song duration (s).
    interval -- the expected interval between moves. (default = 0.5)
    
    Returns:
    moves -- an array of move positions in time (s).
    """
    
    moves = [0.]
    
    t = 0
    while (True):
        dt = poisson(interval*POISSON_SCALING)/POISSON_SCALING
        t += dt
        
        if (t < duration):
            moves += [t]
        else:
            break
    
    return moves

def mapMovesToArrows(moves, speed, offset = TOP_POS):
    
    arrows = []
    
    startOffset = 0.
    lastDirection = 0
    
    for m in moves:
        
        dy = OFFSET_BUFFER + offset + m*speed   # Distance to travel.
        y = offset - dy  # Start position.
        
        # TODO use a more coherent method to generate arrow  
        # directions, like a HMM.
    
        direction = poisson(1) % 4
        lastDirection = direction
        
        arrows += [Arrow(LEFT_POS + direction * SPACING, y, direction, 
                         state = 0, v = speed)]
        
        if (startOffset == 0.):
            startOffset = dy/speed
        
    return arrows, startOffset
