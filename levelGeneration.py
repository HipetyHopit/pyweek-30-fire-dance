"""@package levelGeneration

Functions for level generation.
"""

import pyglet
from numpy.random import poisson, uniform
from scipy.io import wavfile
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
    lastDirection = int(uniform(0, 4))%4
    u = uniform(size = len(moves))
    
    for i in range(len(moves)):
        
        dy = OFFSET_BUFFER + offset + moves[i]*speed    # Distance to travel.
        y = offset - dy  # Start position.
        
        #direction = poisson(1) % 4
        #lastDirection = direction
        
        direction = 0
        x = 0
        while (True):
            x += TRANSITION_MATRIX[lastDirection][direction]
            if (x > u[i]):
                break
            direction += 1
        lastDirection = direction
        
        arrows += [Arrow(LEFT_POS + direction * SPACING, y, direction, 
                         state = 0, v = speed)]
        
        if (startOffset == 0.):
            startOffset = dy/speed
       
    return arrows, startOffset

def getLevel(song, difficulty):
    """
    Generate a new game level.
        
    Keyword arguments:
    song -- the song name for the level.
    difficulty -- the level difficulty. (defualt = 2)
    
    Returns:
    arrows -- an array of arrow objects.
    startOffset -- the time until the track should start playing (s).
    """

    if (difficulty == 1):
        moves = getMoves(track = song, levels = LEVELS_1, interval = INTERVAL_1)
        arrows, startOffset = mapMovesToArrows(moves, SPEED_1)
    elif (difficulty == 2):
        moves = getMoves(track = song, levels = LEVELS_2, interval = INTERVAL_2)
        arrows, startOffset = mapMovesToArrows(moves, SPEED_2)
    elif (difficulty == 3):
        moves = getMoves(track = song, levels = LEVELS_3, interval = INTERVAL_3)
        arrows, startOffset = mapMovesToArrows(moves, SPEED_3)
    elif (difficulty == 4):
        moves = getMoves(track = song, levels = LEVELS_4, interval = INTERVAL_4)
        arrows, startOffset = mapMovesToArrows(moves, SPEED_4)
    else:
        Fs, x = wavfile.read(SONGS_PATH + song)
        T = len(x)/Fs
        moves = getRandomMoves(T, INTERVAL_RANDOM)
        arrows, startOffset = mapMovesToArrows(moves, SPEED_RANDOM)
    
    return arrows, startOffset
