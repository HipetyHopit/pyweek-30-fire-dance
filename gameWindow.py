"""@package GameWindow

Main game class.
"""

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

# States
INTRO = 0
MENU = 1
GAME = 2

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
        #self.set_mouse_visible(False)
        self.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_caption(GAME_TITLE)
        
        self.loopHandle = eventLoop
        
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        
        pyglet.clock.schedule_interval(self.update, 1./60.)     
        
        # Game object setup.
        coconut = Character("coconut", x = 680)
        self.characters = [coconut]
        
        self.arrows = []
        for i in range(4):
            self.arrows += [Arrow(LEFT_POS + i * SPACING, 
                                  TOP_POS, i, state = 1)]
        
        self.background = backgroundSprite
        self.background.color = (47, 15, 84)
        self.background.color = (255, 255, 255)
        
        self.score = Score(x = LEFT_POS + 5*SPACING, y = TOP_POS)
        
        # Music player.
        self.player = pyglet.media.Player()
        self.player.pause()

        # Events.
        class CoconutJump(MarkovEvent):
            """ Make the coconut jump every now and then. """
            
            def execute(self, dt):
                MarkovEvent.execute(self, dt)
                coconut.set_v(0., 70.)
                
        self.events = [CoconutJump(5.)]
        
        # Start game
        
        self.state = GAME   # Temp
        self.startGame()
        
    def startGame(self, song = "disco.00000.wav", difficulty = 2):
        """
        Start a new game level.
        
        Keyword arguments:
        song -- the song name for the level.
        difficulty -- the level difficulty. (defualt = 2)
        """
        
        # TODO add song.
        # TODO add difficulty.
        
        self.arrows = self.arrows[:4]
        
        # Temp
        moves = getRandomMoves(30)
        arrows, trackStartOffset = mapMovesToArrows(moves, 200)
        self.arrows += arrows
        
        # Queue song.
        source = pyglet.media.load(SONGS_PATH + song)
        self.player.queue(source)
        pyglet.clock.schedule_once(self.playSong, trackStartOffset)
        
    def playSong(self, dt):
        """ Music player scheduled callback. """
        
        self.player.play()
        
    def update(self, dt):
        """ Update game objects. """
        
        if (self.state == MENU or self.state == GAME):
            self.background.update()
            for c in self.characters:
                c.update(dt) 
        
        if (self.state == GAME):
            for a in self.arrows:
                a.update(dt)
            self.score.checkFN(self.arrows)

    def on_draw(self):
        """ Handle draw events. """
        
        self.clear()
        
        self.background.draw()
        
        if (self.state == MENU or self.state == GAME):
            for c in self.characters:
                c.draw() 
        
        if (self.state == GAME):
            for a in self.arrows[4:]:
                a.draw() 
            for a in self.arrows[:4]:
                a.draw() 
            self.score.draw()
        
    def on_key_press(self, symbol, modifiers):
        """ Handle key press events. """
        
        if (self.state == GAME):
            
            # Test arrows.
            for i in range(4):
                if (symbol == ARROW_KEYS[i]):
                    self.arrows[i].updateState(2)
                    self.score.checkTP(self.arrows, i)
                
        if (symbol == key.F2):
            screenshot = pyglet.image.get_buffer_manager().get_color_buffer()
            shotTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot.save(SCREENSHOTS_PATH + shotTime + ".png")
            
    def on_key_release(self, symbol, modifiers):
        """ Handle key release events. """
        
        if (symbol == key.ESCAPE):
            self.on_close()
        
        # Test arrows.
        for i in range(4):
            if (symbol == ARROW_KEYS[i]):
                self.arrows[i].updateState(1)
            
    def on_close(self):
        """ Handle close event. """
        
        self.player.delete()
        self.loopHandle.exit()
