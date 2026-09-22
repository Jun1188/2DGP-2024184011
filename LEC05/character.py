from pico2d import *

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

loop = 5
while loop > 0:
    move_circle()
    move_rect()
    move_triangle() 
    loop -= 1
    #코딩 고수는 함수를 만들고 나중에 호출한다 : pseudo code
    pass #아무것도 하지 않고 통과함

close_canvas()

