import game_framework
from pico2d import *
import logo_mode


open_canvas()
try:
    game_framework.run(logo_mode)
finally:
    close_canvas()
