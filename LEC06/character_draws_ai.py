import math

from pico2d import *


DELAY_TIME = 0.02
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def draw_call(x, y, time_scale=1):
    clear_canvas()
    grass.draw(WINDOW_WIDTH // 2, 30)
    character.draw(x, y)
    update_canvas()
    delay(DELAY_TIME * time_scale)


def interpolate_draw(x, y, target_x, target_y):
    steps = 30
    dx = (target_x - x) / steps
    dy = (target_y - y) / steps

    for _ in range(steps):
        x += dx
        y += dy
        draw_call(x, y, 0.5)

    return x, y


def rect_move(x, y, side):
    steps = 100
    distance = side / steps

    for _ in range(steps):
        x += distance
        draw_call(x, y, 0.25)
    for _ in range(steps):
        y += distance
        draw_call(x, y, 0.25)
    for _ in range(steps):
        x -= distance
        draw_call(x, y, 0.25)
    for _ in range(steps):
        y -= distance
        draw_call(x, y, 0.25)

    return x, y


def circle_move(center_x, center_y, radius):
    steps = 72

    for step in range(1, steps + 1):
        angle = 2 * math.pi * step / steps
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        draw_call(x, y, 0.5)

    return x, y


def triangle_move(x, y, side):
    top_x = x + side / 2
    top_y = y + side * math.sqrt(3) / 2

    x, y = interpolate_draw(x, y, x + side, y)
    x, y = interpolate_draw(x, y, top_x, top_y)
    x, y = interpolate_draw(x, y, x - side / 2, y - side * math.sqrt(3) / 2)

    return x, y


open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

character = load_image('character.png')
grass = load_image('grass.png')

rect_start = (100, 100)
rect_side = 250
circle_center = (400, 320)
circle_radius = 140
triangle_start = (150, 100)
triangle_side = 300

x, y = rect_start

while True:
    x, y = rect_move(x, y, rect_side)

    circle_start = (circle_center[0] + circle_radius, circle_center[1])
    x, y = interpolate_draw(x, y, *circle_start)
    x, y = circle_move(*circle_center, circle_radius)

    x, y = interpolate_draw(x, y, *triangle_start)
    x, y = triangle_move(x, y, triangle_side)

    x, y = interpolate_draw(x, y, *rect_start)
