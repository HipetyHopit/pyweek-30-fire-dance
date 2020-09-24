"""@package constants

Game and module constants.
"""

from pyglet.window import key

# Game constants.
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
GAME_TITLE = "Untitled"

ARROW_KEYS = [key.LEFT, key.UP, key.DOWN, key.RIGHT]

# Window constants.
LEFT_POS = 256
TOP_POS = WINDOW_HEIGHT - 96
SPACING = 96

# Menu constants.
MAX_ITEM_LEN = 24
DEFAULT_FONT = "Papyrus"
LARGE_FONT = 36
MEDIUM_FONT = 20
LARGE_SPACING = 70
MEDIUM_SPACING = 30
DIFFICULTY_LABELS = ["Random chaos", "Easy", "Medium", "Hard", "Expert"]

# Sprite constants.
SPRITE_SCALING = 2
GRAVITY = 98 # px/s^2
GROUNDLEVEL = 128

# Level constants.
OFFSET_BUFFER = 100
POISSON_SCALING = 100

# Colour constants.
NIGHT = (47, 15, 84, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
GREY = (128, 128, 128, 255)

# Intro constants.
INTRO_TEXT = ["Dave has been stranded for so long;",
              "a castaway on a desolate island.",
              "He has long ago given up counting days.",
              "His mind is starting to slip...",
              "The coconut has developed a personality.",
              "And at night the fire requires the strange",
              "ritual of DANCE to keep the darkness at bay."]

# Beat tracking constants
GAMMA = 100
N = 1024
H = 512
K = 4096

# Path constants.
SONGS_PATH = "songs/"
SPRITE_PATH = "data/images/sprites/"
IMAGE_PATH = "data/images/"
SCREENSHOTS_PATH = "data/screenshots/"
