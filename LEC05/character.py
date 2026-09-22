from pico2d import *

def RectMove():
    x = 0
    y = 90
    delta = 20
    while x < 800:
        x += delta
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.02)
    
    while y < 600:
        y += delta  
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.02)
    while x > 0:
        x -= delta
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.02)
    while y > 90:
        y -= delta
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.02)
def CircleMove():
    x = 400
    y = 300
    r = 200
    degree = 0
    delta = 10
    while degree < 360:
        degree += delta
        radian = math.radians(degree)
        x = 400 + r * math.cos(radian)
        y = 300 + r * math.sin(radian)
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.02)


open_canvas(800, 600)

# 여기를 채우시오.

character = load_image('character.png')
grass = load_image('grass.png')
clear_canvas()

loop = 2
for i in range(loop):
    RectMove()
for i in range(loop):
    CircleMove()


    #pass #아무것도 하지 않고 통과함

close_canvas()

