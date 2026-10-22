import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from pico2d import *

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('run_animation.png')
running = True
frame = 0
x = 0
while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False
    if not running:
        break
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    x = (x + 5) % 800
    delay(0.05)
close_canvas()
