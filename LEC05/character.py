from pico2d import *

def test_move(x, y):
    
    delta = 10

    x += delta
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
    delay(0.1)
    return x, y


def move_circle():
    print("circle")
    return
def move_rect():
    print("rectangle")
    return
def move_triangle():
    print("tirangle")
    return

open_canvas(800, 600)

# 여기를 채우시오.

character = load_image('character.png')
grass = load_image('grass.png')
clear_canvas()

loop = 10
x = 0
y = 90
while loop > 0:
    x, y = test_move(x, y)
    #move_circle()
    #move_rect()
    #move_triangle() 
    loop -= 1
    #코딩 고수는 함수를 만들고 나중에 호출한다 : pseudo code
    #pass #아무것도 하지 않고 통과함

close_canvas()

