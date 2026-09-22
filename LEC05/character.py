from pico2d import *

def MovefromTo(x1, y1, x2, y2):
    mx = x1
    my = y1
    delta = 5
    while x1 == x2 and y1 == y2:
        if mx + delta < x2:
            mx += delta
        elif mx + delta > x2:
            mx -= delta
            mx = x2
        if my + delta < y2:
                my += delta
        elif my + delta > y2:
                my -= delta
                my = y2
        clear_canvas()
        grass.draw(400, 30)
        character.draw(mx, my)
        update_canvas()
    return mx, my
    
def RectMove():
    x = 0
    y = 90
    delta = 10
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
    return x, y
def CircleMove():
    x = 400
    y = 300
    r = 200
    degree = 0
    delta = 5
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
    x, y = RectMove()
MovefromTo(x, y, 400, 300)
for i in range(loop):
    CircleMove()


    #pass #아무것도 하지 않고 통과함

close_canvas()

