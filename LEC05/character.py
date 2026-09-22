from pico2d import *



def drawCall(x,y):

    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
        
    delay(0.02)

def lagrange_interpolation(t_points, x_points, y_points, target_t):
    """
    매개변수 t를 기준으로 x와 y 변수를 동시에 라그랑주 보간합니다.
    :param t_points: 매개변수(예: 시간, 0~1 사이의 비율 등) 리스트
    :param x_points: 각 t점에 대응하는 x 좌표 리스트
    :param y_points: 각 t점에 대응하는 y 좌표 리스트
    :param target_t: 보정된 값을 얻고자 하는 현재 시점 t
    :return: 보정된 (interpolated_x, interpolated_y) 튜플
    """
    n = len(t_points)
    interpolated_x = 0.0
    interpolated_y = 0.0

    for i in range(n):
        # 기저 다항식 L_i(t) 계산
        term_t = 1.0
        for j in range(n):
            if i != j:
                term_t *= (target_t - t_points[j]) / (t_points[i] - t_points[j])
        
        # x와 y 성분에 각각 가중치(기저 다항식)를 곱해 누적 합산
        interpolated_x += x_points[i] * term_t
        interpolated_y += y_points[i] * term_t
        drawCall(interpolated_x, interpolated_y)

    return interpolated_x, interpolated_y


        
    
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

