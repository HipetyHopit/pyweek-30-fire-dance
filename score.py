"""@package score

Score class.
"""

import pyglet
from constants import *

class Score(pyglet.text.Label):
    """ Score class. """
    
    def __init__(self, x, y):
        """
        Constructor. 
        
        Keyword arguments:
        x -- x position.
        y -- y position.
        """
        
        super(Score, self).__init__("50%", font_name = "Papyrus", font_size = 36, 
                                    x = x, y = y)
        
        self.tp = 0.
        self.fp = 0
        self.fn = 0
        self.accuracy = 0.
        
    def reset(self):
        """ Reset the score. """
        
        self.tp = 0.
        self.fp = 0
        self.fn = 0
        self.accuracy = 0.
        
    def updateScore(self):
        """ Update the score. """
        
        if (self.tp > 0 or self.fp > 0):
            precision = self.tp/(self.tp + self.fp)
        else:
            precision = 0.5
            
        if (self.tp > 0 or self.fn > 0):
            recall = self.tp/(self.tp + self.fn)
        else:
            recall  = 0.5
            
        f1 = 2*precision*recall/(precision + recall)
        
        if (self.tp > 0):
            score = (self.accuracy/self.tp + f1)*100./2.
            self.text = str(score)+"%"  #("%.2f%" % score)
        
        print (precision, recall, f1)
        
    def checkTP(self, arrows, direction):
        """
        Update the score for true positives and false positives. 
        
        Keyword arguments:
        arrows -- an array of arrow elements in the game. The first 
            4 elements should be the target buttons.
        direction -- the direction of the arrow that was pressed.
        """
        
        collide = False
          
        for i in range(4, len(arrows)):
            if (arrows[direction].getCollide(arrows[i])):
                self.accuracy += (abs(arrows[i].y - arrows[direction].y)/
                                  arrows[direction].height)
                arrows[i].deactivate()
                self.tp += 1
                collide = True
                
        if (not collide):
           self.fp += 1
           
        self.updateScore()
        
    def checkFN(self, arrows):
        """
        Update the score for false negatives. 
        
        Keyword arguments:
        arrows -- an array of arrow elements in the game. The first 
            4 elements should be the target buttons.
        """
        
        change = False
          
        for i in range(4, len(arrows)):
            if (not arrows[i].active):
                continue
            
            if (arrows[i].y > WINDOW_HEIGHT + arrows[i].height):
                
                self.fn += 1
                arrows[i].deactivate()
                
                change = True
                
        if (change):
           self.updateScore()
