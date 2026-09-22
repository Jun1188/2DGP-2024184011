from pico2d import *



class Circle:
    def __init__(self, x = 400, y = 300, r = 100):
        self.x = x
        self.y = y
        self.r = r

delayTime = 0.02

def drawCall(x,y, deltatime = 1):

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
    t = 10
    interp_x =x1
    interp_y = y1
    # 선형 보간 처리
    for i in range(t):
        interp_x = interp_x + (1/t) * dx
        interp_y = interp_y + (1/t) * dy
        drawCall(interp_x, interp_y, (1/t)*2)
    
    return interp_x, interp_y
        
    
def RectMove(x, y, side):#정사각형으로 가정
    
    delta = 10
    fixedX = x
    fixedY = y
    while x < fixedX + side:
        x += delta
        drawCall(x, y, 1/4)
    fixedX = x
    while y < fixedY + side:
        y += delta  
        drawCall(x, y, 1/4)
    fixedY = y
    while x > fixedX - side:
        x -= delta
        drawCall(x, y, 1/4)

    while y > fixedY - side:
        y -= delta
        drawCall(x, y, 1/4)
    
    return x, y
def CircleMove(x, y, r):
    
    degree = 0
    delta = 5
    while degree < 360:
        degree += delta
        radian = math.radians(degree)
        x = 400 + r * math.cos(radian)
        y = 300 + r * math.sin(radian)
        drawCall(x, y, delta/(delta + 2))
    return x, y
def TriangleMove(x, y, side):#정삼각형임을 가정
    delta = 10
    startX = x
    while x < startX + side:
        x += delta
        drawCall(x, y, (1 / delta) * 6)
    x, y = interpolate_draw(x, y, x - side/2, y + side/2)
    x, y = interpolate_draw(x, y, x - side/2, y - side/2)
    
    return x, y
    


open_canvas(800, 600)

# 여기를 채우시오.

character = load_image('character.png')
grass = load_image('grass.png')
clear_canvas()

loop = 3
x, y = 0, 90
sideR = 300
for i in range(loop):
    x, y = RectMove(x, y, sideR)
    sideR -= 100/loop
center = Circle(400, 300, 100)
x, y = interpolate_draw(x, y, center.x + center.r, center.y)
for i in range(loop):
    x, y = CircleMove(x, y, center.r)
    center.r -= 100/loop
side = 400
x, y = interpolate_draw(x, y, x - sideR, y)
for i in range(loop):
    x, y = TriangleMove(x, y, side)
    side -= 100/loop

    #pass #아무것도 하지 않고 통과함

close_canvas()

