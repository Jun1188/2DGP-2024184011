from pico2d import *



def drawCall(x,y):

    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
        
    delay(0.02)

def interpolate_draw(x1, y1, x_target, y_target):
    
    # 상대 변위 벡터 추출
    dx = x_target - x1
    dy = y_target - y1
    t = 10
    # 선형 보간 처리
    for i in range(t):
        interp_x = x1 + (1/t) * dx
        interp_y = y1 + (1/t) * dy
        drawCall(interp_x, interp_y)
    
    return interp_x, interp_y
        
    
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
center = {x:400, y:300}
interpolate_draw(x, y, center[x], center[y])
for i in range(loop):
    CircleMove()


    #pass #아무것도 하지 않고 통과함

close_canvas()

