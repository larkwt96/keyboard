from .keyboard import *
from .music import *
from .player import *

with open(os.devnull, 'w') as devnull:
    sys.stdout = devnull
    sys.stderr = devnull
    import pygame
    pygame.mixer.pre_init(frequency=44100)
    pygame.init()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

