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
    def drawAt(self, x, y):
        self.img.draw(x, y)
    def update(self): pass

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
def update_world(data):
    pass
def render_world():
    clear_canvas()
    for d in data:
        d.draw()
    update_canvas()



open_canvas()
grass = Grass()
data = [grass]
reset_world()
while running:
    handle_events()
    update_world(data)
    render_world()
    delay(0.05)
close_canvas()
