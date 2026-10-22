import math
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

from pico2d import *

delayTime = 0.02
windowH = 600
windowW = 800


class Circle:
    def __init__(self, x = 400, y = 300, r = 100):
        self.x = x
        self.y = y
        self.r = r


def drawCall(x,y, deltatime = 1):
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            raise SystemExit


    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
    #print(f"{x}, {y}")
    delay(delayTime * deltatime)

def interpolate_draw(x1, y1, x_target, y_target):
    
    # 상대 변위 벡터 추출
    dx = x_target - x1
    dy = y_target - y1
    t = 100
    interp_x =x1
    interp_y = y1
    # 선형 보간 처리
    for i in range(t):
        interp_x = interp_x + (1/t) * dx
        interp_y = interp_y + (1/t) * dy
        drawCall(interp_x, interp_y, 1/4)
    
    return x_target, y_target
        
    
def RectMove(x, y, side):
    start_x, start_y = x, y
    x, y = interpolate_draw(x, y, start_x + side, start_y)
    x, y = interpolate_draw(x, y, start_x + side, start_y + side)
    x, y = interpolate_draw(x, y, start_x, start_y + side)
    x, y = interpolate_draw(x, y, start_x, start_y)
    return x, y

def CircleMove(center_x, center_y, r):
    x, y = center_x + r, center_y
    for degree in range(10, 361, 10):
        radian = math.radians(degree)
        x = center_x + r * math.cos(radian)
        y = center_y + r * math.sin(radian)
        drawCall(x, y, 10 / 12)
    return x, y

def TriangleMove(x, y, side):
    start_x, start_y = x, y
    height = side * math.sqrt(3) / 2
    x, y = interpolate_draw(x, y, start_x + side, start_y)
    x, y = interpolate_draw(x, y, start_x + side / 2, start_y + height)
    x, y = interpolate_draw(x, y, start_x, start_y)
    return x, y

open_canvas(windowW, windowH)


character = load_image('character.png')
grass = load_image('grass.png')
clear_canvas()

loop = 3
x, y = 0, 90
sideR = windowH /2 
for i in range(loop):
    x, y = RectMove(x, y, sideR)
    sideR -= 100/loop
center = Circle(windowW/2, windowH/2, windowH/4)
x, y = interpolate_draw(x, y, center.x + center.r, center.y)
for i in range(loop):
    x, y = interpolate_draw(x, y, center.x + center.r, center.y)
    x, y = CircleMove(center.x, center.y, center.r)
    center.r -= 100/loop
side = 400
x, y = interpolate_draw(x, y, 150, 90)
for i in range(loop):
    x, y = TriangleMove(x, y, side)
    side -= 100/loop

    #pass #아무것도 하지 않고 통과함

close_canvas()

