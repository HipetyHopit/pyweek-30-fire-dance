"""@package score

Score class.
"""

import pyglet
from labelList import LabelList
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
        
        super(Score, self).__init__("0.00%", font_name = DEFAULT_FONT, 
                                    font_size = LARGE_FONT, x = x, y = y)
        
        self.tp = 0.
        self.fp = 0
        self.fn = 0
        self.precision = 1.
        self.recall = 1.
        self.accuracy = 0.
        self.total = 0.
        
        self.text = ("%.2f%%" % self.total)
        
    def reset(self):
        """ Reset the score. """
        
        self.tp = 0.
        self.fp = 0
        self.fn = 0
        self.precision = 1.
        self.recall = 1.
        self.accuracy = 0.
        self.total = 0.
        
        self.text = ("%.2f%%" % self.total)
        
    def updateScore(self):
        """ Update the score. """
        
        if (self.tp > 0 or self.fp > 0):
            self.precision = self.tp*100./(self.tp + self.fp)
            
        if (self.tp > 0 or self.fn > 0):
            self.recall = self.tp*100./(self.tp + self.fn)
        
        if (self.precision + self.recall > 0):
            f1 = 2*self.precision*self.recall/(self.precision + self.recall)
        else:
            f1 = 0
        
        #if (self.tp > 0):
            #self.total = (self.accuracy*100./self.tp + f1)/2.
        #else:
            #self.total = f1
          
        if (self.accuracy > 0):
            self.total = self.accuracy*f1/self.tp
        else:
            self.total = 0.
            
        self.text = ("%.2f%%" % self.total)
        
        #print (precision, recall, f1)
        
    def getResults(self):
        
        labels = []
        results = []
        
        labels += ["Hits:"]
        labels += ["Misses:"]
        labels += ["Precision:"]
        labels += ["Recall:"]
        labels += ["Accuracy:"]
        labels += ["Total:"]
        
        results += ["%d" % self.tp]
        results += ["%d" % (self.fp + self.fn)]
        results += ["%.2f%%" % self.precision]
        results += ["%.2f%%" % self.recall]
        if (self.accuracy > 0):
            results += ["%.2f%%" % (self.accuracy*100./self.tp)]
        else :
            results += ["0%"]
        results += ["%.2f%%" % self.total]
        
        return (LabelList(labels, self.x, self.y, anchor_x = "left"), 
                LabelList(results, self.x + 100, self.y, anchor_x = "right"))
        
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
                a = (1 - abs(arrows[i].y - arrows[direction].y)/
                     arrows[direction].height)
                self.accuracy += a
                arrows[i].deactivate()
                self.tp += 1
                collide = True
                
                break
                
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
