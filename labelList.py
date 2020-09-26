"""@package labelList

List class.
"""

import pyglet
from constants import *

class LabelList:
    
    def __init__(self, labels, x = 0, y = 0, spacing = LARGE_SPACING, 
                 font_name = DEFAULT_FONT, font_size = LARGE_FONT, 
                 anchor_x = "left", anchor_y = "center", selected = None, 
                 focused = True, maxLabels = None):
        """
        Constructor.
        
        Keyword arguments:
        labels -- a list of labels.
        x -- x position. (default = 0)
        y -- y position. (default = 0)
        spacing -- spacing between items. (default  = LARGE_SPACING)
        font_name -- the font name. (default  = DEFAULT_FONT)
        font_size -- the font size. (default  = LARGE_FONT)
        anchor_x -- the x anchor. (default  = "left")
        anchor_y -- the y anchor. (default  = "center")
        selected -- the selected item. (default  = None)
        focused -- wheteher the list is in focus. (default  = True)
        maxLabels -- the maximum items to display. (default  = None)
        """
        
        self.x = x
        self.y = y
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.spacing = spacing
        self.selected = selected
        self.focused = True
        self.page = 0
        if (maxLabels == None):
            self.maxLabels = len(labels)
        else:
            self.maxLabels = maxLabels
        
        self.labels = []
        for i in range(len(labels)):
            
            if (anchor_y == "center"):
                temp_y = (y - (len(labels)-1)*spacing/2 + 
                          (i%self.maxLabels)*spacing)
                j = -1-i
            elif (anchor_y == "baseline"):
                temp_y = y + (i%self.maxLabels)*spacing
                j = -1-i
            else:
                temp_y = y - (i%self.maxLabels)*spacing
                j = i
            
            self.labels += [pyglet.text.Label(labels[j], x = x, y = temp_y, 
                                              anchor_x = anchor_x, 
                                              anchor_y = anchor_y, 
                                              font_name = font_name, 
                                              font_size = font_size)]
        
        if (self.selected != None):
            
            self.selected = self.selected % len(self.labels)
            if (focused):
                self.labels[self.selected].color = BLACK
            else:
                self.labels[self.selected].color = GREY
                
    def setSelect(self, n):
        """
        Set selected item.
        
        Keyword arguments:
        n -- the index of the selected item.
        """
        
        self.labels[self.selected].color = WHITE
        self.selected = n % len(self.labels)
        if (self.focused):
            self.labels[self.selected].color = BLACK
        else:
            self.labels[self.selected].color = GREY
            
        self.page = self.selected // self.maxLabels
        
    def incSelect(self):
        """ Increase the selection. """
        
        self.setSelect(self.selected + 1)
        
    def decSelect(self):
        """ Decrease the selection. """
        
        self.setSelect(self.selected - 1)
        
    def setFocused(self, focused):
        """
        Set wheteher the list is in focus.
        
        Keyword arguments:
        focused -- whether the list is in focus.
        """
    
        self.focused = focused
    
        if (self.focused):
            self.labels[self.selected].color = BLACK
        else:
            self.labels[self.selected].color = GREY
         
    def setPos(self, x, y):
        """
        Set the list's position.
        
        Keyword arguments:
        focused -- whether the list is in focus.
        x -- x position.
        y -- y position.
        """
        
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
        
        page0 = self.page*self.maxLabels
        page1 = (self.page + 1)*self.maxLabels
        if (page1 > len(self.labels)):
            page1 = len(self.labels)
        
        for i in range(page0, page1):
            self.labels[i].draw()
