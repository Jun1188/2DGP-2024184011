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
        self.x, self.y = 0, 90
        self.frame = random.randint(0, 6)
        self.max_frame = 8
        self.deltaPerFrame = 100
        self.dirX = random.randint(1, 10)
        self.img = load_image("run_animation.png")
    def update(self):
        self.frame = (self.frame + 1) % self.max_frame
        self.x += self.dirX
    def draw(self):
        self.img.clip_draw(self.frame*self.deltaPerFrame, 0, self.deltaPerFrame, self.deltaPerFrame, self.x, self.y)

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
def update_world(boys, grass):
    grass.update()
    for d in boys:
        d.update()

def render_world(boys, grass):
    clear_canvas()
    for d in boys:
        d.draw()
    grass.draw()
    update_canvas()



open_canvas()
grass = Grass()
numBoy = 10
boys = [Boy() for i in range(numBoy)]

reset_world()
while running:
    handle_events()
    update_world(boys, grass)
    render_world(boys, grass)
    delay(0.05)
close_canvas()
