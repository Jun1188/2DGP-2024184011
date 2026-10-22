import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from pico2d import *

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('character.png')
clear_canvas()
grass.draw(400, 30)
character.draw(400, 90)
update_canvas()
delay(2)
close_canvas()
