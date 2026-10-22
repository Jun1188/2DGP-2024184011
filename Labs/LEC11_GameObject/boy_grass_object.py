import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from pico2d import *
import random


# Game object class here

running = True



class Grass:
    def __init__(self):
        self.img = load_image("grass.png")
        self.grassY = 30
        self.grassX = 400
    def draw(self):
        self.img.draw(self.grassX, self.grassY)
    def update(self):
        pass
    def drawAt(self, x, y):
        self.img.draw(x, y)




class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0,7)
        self.max_frame = 8
        self.deltaPerFrame = 100
        self.dirX = random.randint(1, 10)
        self.img = load_image("run_animation.png")
    def update(self):
        self.frame = (self.frame + 1) % self.max_frame
        self.x += self.dirX
    def draw(self):
        self.img.clip_draw(self.frame*self.deltaPerFrame, 0, self.deltaPerFrame, self.deltaPerFrame, self.x, self.y)


class Zombie:
    def __init__(self):
        self.x, self.y = 100, 170
        self.frame = 0
        self.image = load_image('zombie_run_animation.png')
    def update(self):   
        self.frame = (self.frame + 1) % 10
        self.x += 5
    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h
        self.image.clip_draw(self.frame * frame_width, 0, frame_width, frame_height,
        self.x, self.y, frame_width // 2, frame_height // 2)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running
    running = True


    # 객체들을 담는 world list
    global world
    world = []

    grass = Grass()
    world.append(grass)

    team = [Boy() for i in range(10)]
    world.extend(team)

    zombie = Zombie()
    world.append(zombie)

def update_world():

    for d in world:
        d.update()


def render_world():
    clear_canvas()
    for d in world:
        d.draw()

    update_canvas()



open_canvas()


reset_world()
while running:
    handle_events()
    if not running:
        break
    update_world()
    render_world()
    delay(0.05)
close_canvas()
