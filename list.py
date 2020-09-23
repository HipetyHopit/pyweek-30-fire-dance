"""@package labelList

List class.
"""

import pyglet
from constants import *

class LabelList:
    
    def __init__(self, labels, x, y, spacing = 30, 
                 font_name = "Times New Roman", font_size = 36, 
                 anchor_x = "left", anchor_y = "center"):
        
        self.x = x
        self.y = y
        
        self.labesl = []
        for i in range(len(labels)):
            
            if (anchor_y == "center"):
                temp_y = y - (len(labels)-1)*spacing/2
            else:
                temp_y = y
                
            temp_y += i*spacing
            
            self.labels += pyglet.text.Label(labels[i], x, y_temp, 
                                             anchor_x = anchor_x, 
                                             anchor_y = anchor_y, 
                                             font_name = font_name, 
                                             font_size = font_size)
            
    def draw(self):
        """ Draw labels. """
        
        for l in self.labels:
            l.draw()
