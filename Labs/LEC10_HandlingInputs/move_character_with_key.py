import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from pico2d import *

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('animation_sheet.png')
running = True
x = 400
frame = 0
dir = 0
facing = 1
pressed_keys = set()

def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in (SDLK_LEFT, SDLK_RIGHT):
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)

while running:
    handle_events()
    if not running:
        break
    dir = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    x = max(50, min(750, x + dir * 5))
    if dir:
        facing = dir
        frame = (frame + 1) % 8
    else:
        frame = 0
    # 아래에서부터: 왼쪽 달리기, 오른쪽 달리기, 왼쪽 대기, 오른쪽 대기.
    row = (1 if facing > 0 else 0) if dir else (3 if facing > 0 else 2)
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, row * 100, 100, 100, x, 90)
    update_canvas()
    delay(0.05)
close_canvas()
