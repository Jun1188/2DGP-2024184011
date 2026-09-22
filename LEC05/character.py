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
    
        delay(0.01)
    
    while y < 600:
        y += delta  
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.01)
    while x > 0:
        x -= delta
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.01)
    while y > 90:
        y -= delta
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
    
        delay(0.01)
def CircleMove():
    x = 400
    y = 300
    r = 100
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
    
        delay(0.01)


open_canvas(800, 600)

# 여기를 채우시오.

character = load_image('character.png')
grass = load_image('grass.png')
clear_canvas()

loop = 3
while loop > 0:
   
    RectMove()
    CircleMove()
    loop -= 1

    #pass #아무것도 하지 않고 통과함

close_canvas()

