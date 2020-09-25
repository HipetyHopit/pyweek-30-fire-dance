"""@package GameWindow

Main game class.
"""

import os
import pyglet
from pyglet.window import key
from pyglet.gl import *
from datetime import datetime
from character import Character
from arrows import Arrow
from background import backgroundSprite
from events import MarkovEvent
from score import Score
from constants import *
from levelGeneration import *
from labelList import LabelList

# States
INTRO = 0
MENU = 1
GAME = 2
SCORE = 3

# Turn off image scaling interpolation.
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

class GameWindow(pyglet.window.Window):
    """ Main game class. """
    
    def __init__(self, eventLoop):
        """
        Constructor. 
        
        Keyword arguments:
        eventLoop -- a handle for the application event loop.
        """
        
        super(GameWindow, self).__init__()

        # Window setup.
        #self.set_exclusive_mouse()
        self.set_mouse_visible(False)
        self.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_caption(GAME_TITLE)
        
        self.loopHandle = eventLoop
        
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.updateSuppress = False
        
        pyglet.clock.schedule_interval(self.update, 1./60.)     
        
        # Game object setup.
        self.coconut = Character("coconut", x = 680)
        self.castaway = Character("castaway", x = 64, numStates = 3)
        self.fire = Character("fire", x = 720, numStates = 3)
        self.characters = [self.coconut, self.castaway, self.fire]
        
        self.arrows = []
        for i in range(4):
            self.arrows += [Arrow(LEFT_POS + i * SPACING, 
                                  TOP_POS, i, state = 1)]
        
        self.background = backgroundSprite
        self.background.color = WHITE[:3]
        
        self.score = Score(x = LEFT_POS + 5*SPACING, y = TOP_POS)
        self.results = self.score.getResults()
        
        # Intro setup.
        self.intro = LabelList(INTRO_TEXT, x = 64, y = WINDOW_HEIGHT - 64, 
                               spacing = MEDIUM_SPACING, anchor_x = "left", 
                               anchor_y = "top", font_size = MEDIUM_FONT)
        self.prompt = pyglet.text.Label(PROMPT_TEXT, x = WINDOW_WIDTH - 64, 
                                        y = 64, anchor_x = "right", 
                                        anchor_y = "baseline", 
                                        font_size = MEDIUM_FONT, 
                                        font_name = DEFAULT_FONT)
        self.fire.setDirection(2)
        
        # Menu setup.
        self.songOptions = []
        menuItems = []
        for f in os.listdir(SONGS_PATH):
            if (f.endswith(".wav")):
                self.songOptions += [f]
                menuItem = f[:-4]
                if (len(menuItem) > MAX_ITEM_LEN):
                    menuItem = menuItem[:MAX_ITEM_LEN] + "..."
                menuItems += [menuItem]
        self.songMenu = LabelList(menuItems, x = 64, y = WINDOW_HEIGHT - 128, 
                                  spacing = MEDIUM_SPACING, anchor_x = "left", 
                                  anchor_y = "top", font_size = MEDIUM_FONT, 
                                  selected = 0, maxLabels = 10)
        
        singHeading = pyglet.text.Label("Song:", x = 64, y = WINDOW_HEIGHT - 64, 
                                        anchor_x = "left", anchor_y = "top", 
                                        font_size = LARGE_FONT, 
                                        font_name = DEFAULT_FONT)
        
        self.difficultyMenu = LabelList(DIFFICULTY_LABELS, x = 512, 
                                        y = WINDOW_HEIGHT - 128, 
                                        anchor_y = "top", 
                                        font_size = MEDIUM_FONT, selected = 2, 
                                        focused = False, 
                                        spacing = MEDIUM_SPACING)
        
        difficultyHeading = pyglet.text.Label("Difficulty:", x = 512, 
                                              y = WINDOW_HEIGHT - 64, 
                                              anchor_x = "left", 
                                              anchor_y = "top", 
                                              font_size = LARGE_FONT, 
                                              font_name = DEFAULT_FONT)
        
        self.menu = [singHeading, self.songMenu, difficultyHeading, 
                     self.difficultyMenu]
        
        # Music player.
        self.player = pyglet.media.Player()
        self.player.pause()
        self.player.volume = 1.

        # Events.
        windowHandle = self
        
        class CoconutJump(MarkovEvent):
            """ Make the coconut jump every now and then. """
            
            def execute(self, dt):
                MarkovEvent.execute(self, dt)
                windowHandle.coconut.set_v(0., 70.)
                
        self.events = [CoconutJump(5.)]
        
        # Start.
        self.state = INTRO
        
    def startGame(self, dt):
        """ Start a new game level. """
        
        if (self.state == GAME):
            return
        
        self.state = GAME
        self.arrows = self.arrows[:4]
        self.score.reset()
        song = self.songOptions[self.songMenu.selected]
        
        # Generate level.
        self.updateSuppress = True
        arrows, trackStartOffset = getLevel(song, self.difficultyMenu.selected)
        self.arrows += arrows
        
        # Queue song.
        source = pyglet.media.load(SONGS_PATH + song)
        self.player.queue(source)
        pyglet.clock.schedule_once(self.playSong, trackStartOffset)
        
    def playSong(self, dt):
        """ Music player scheduled callback. """
        
        self.player.play()
        
        @self.player.event
        def on_player_eos():
            
            self.state = SCORE
            self.prompt.text = PROMPT_TEXT
            self.results = self.score.getResults()
            self.results[0].setPos(128, WINDOW_HEIGHT/2)
            self.results[1].setPos(WINDOW_WIDTH - 128, WINDOW_HEIGHT/2)
        
    def update(self, dt):
        """ Update game objects. """
        
        if (self.updateSuppress):
            self.updateSuppress = False
            return
        
        if (self.state == MENU or self.state == GAME or self.state == SCORE):
            self.background.update()
            for c in self.characters:
                c.update(dt) 
        
        if (self.state == GAME):
            for a in self.arrows:
                a.update(dt)
            self.score.checkFN(self.arrows)
            fireState = int(self.score.total/25.)
            if (self.fire.direction != fireState):
                self.fire.setDirection(fireState)

    def on_draw(self):
        """ Handle draw events. """
        
        self.clear()
        
        if (self.state == INTRO):
            self.intro.draw()
            self.fire.draw()
        
        if (self.state == MENU or self.state == GAME or self.state == SCORE):
            self.background.draw()
            
            for c in self.characters:
                c.draw() 
                
        if (self.state == MENU):
            for m in self.menu:
                m.draw()
        
        if (self.state == GAME):
            for a in self.arrows[4:]:
                a.draw() 
            for a in self.arrows[:4]:
                a.draw() 
            self.score.draw()
            
        if (self.state == SCORE):
            self.results[0].draw()
            self.results[1].draw()
            
        if (self.state != GAME):
            self.prompt.draw()
        
    def on_key_press(self, symbol, modifiers):
        """ Handle key press events. """
           
        # Test arrows.
        if (self.state == GAME):
            for i in range(4):
                if (symbol == ARROW_KEYS[i]):
                    self.castaway.setDirection(i)
                    self.arrows[i].updateState(2)
                    self.score.checkTP(self.arrows, i)
            
        # Screenshot.
        if (symbol == key.F2):
            screenshot = pyglet.image.get_buffer_manager().get_color_buffer()
            shotTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot.save(SCREENSHOTS_PATH + shotTime + ".png")
            
        # Volume control. 
        # NOTE Weird rounding method seems necissary to prevent
        # invalid volumes.
        if (symbol == key.F3 and self.player.volume > 0.):
            self.player.volume = (int(self.player.volume*10) - 1)/10.
        if (symbol == key.F4 and self.player.volume < 1.):
            self.player.volume = (int(self.player.volume*10) + 1)/10.
            
    def on_key_release(self, symbol, modifiers):
        """ Handle key release events. """
        
        if (symbol == key.ESCAPE):
            
            if (self.state == GAME or self.state == SCORE):
                self.player.pause()
                self.player.next_source()
                pyglet.clock.unschedule(self.playSong)
                self.state = MENU
                self.prompt.text = START_TEXT
            else:
                self.on_close()
            
        if (symbol == key.ENTER):
            
            if (self.state == INTRO):
                self.state = MENU
                self.prompt.text = START_TEXT
            elif (self.state == MENU):
                self.prompt.text = LOAD_TEXT
                pyglet.clock.schedule_once(self.startGame, 0.5)
            elif (self.state == SCORE):
                self.state = MENU
                self.prompt.text = START_TEXT
        
        # Test arrows.
        if (self.state == MENU):
            if (symbol == ARROW_KEYS[1]):
                if (self.songMenu.focused):
                    self.songMenu.decSelect()
                else:
                    self.difficultyMenu.decSelect()
            if (symbol == ARROW_KEYS[2]):
                if (self.songMenu.focused):
                    self.songMenu.incSelect()
                else:
                    self.difficultyMenu.incSelect()
            if (symbol == ARROW_KEYS[0] or symbol == ARROW_KEYS[3]):
                if (self.songMenu.focused):
                    self.songMenu.setFocused(False)
                    self.difficultyMenu.setFocused(True)
                else:
                    self.songMenu.setFocused(True)
                    self.difficultyMenu.setFocused(False)
        elif (self.state == GAME):
            for i in range(4):
                if (symbol == ARROW_KEYS[i]):
                    self.arrows[i].updateState(1)
            
    def on_close(self):
        """ Handle close event. """
        
        self.player.delete()
        self.loopHandle.exit()
