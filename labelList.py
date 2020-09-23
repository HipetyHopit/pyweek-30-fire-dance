"""@package labelList

List class.
"""

import pyglet
from constants import *

class LabelList:
    
    def __init__(self, labels, x = 0, y = 0, spacing = 70, 
                 font_name = "Papyrus", font_size = 36, 
                 anchor_x = "left", anchor_y = "center"):
        
        self.x = x
        self.y = y
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.spacing = spacing
        
        self.labels = []
        for i in range(len(labels)):
            
            if (anchor_y == "center"):
                temp_y = y - (len(labels)-1)*spacing/2 + i*spacing
                j = -1-i
            elif (anchor_y == "baseline"):
                temp_y = y + i*spacing
                j = -1-i
            else:
                temp_y = y - i*spacing
                j = i
            
            self.labels += [pyglet.text.Label(labels[j], x = x, y = temp_y, 
                                              anchor_x = anchor_x, 
                                              anchor_y = anchor_y, 
                                              font_name = font_name, 
                                              font_size = font_size)]
            
    def setPos(self, x, y):
        
        self.x = x
        self.y = y
        
        for i in range(len(self.labels)):
            
            if (self.anchor_y == "center"):
                temp_y = y - (len(self.labels)-1)*self.spacing/2
            else:
                temp_y = y
                
            temp_y += i*self.spacing
            
            self.labels[i].x = x
            self.labels[i].y = temp_y
            
    def draw(self):
        """ Draw labels. """
        
        for l in self.labels:
            l.draw()
