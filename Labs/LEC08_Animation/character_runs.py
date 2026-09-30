from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')



frame = 100
curFrame = 0
maxFrame = 800
frameType = 100

runToLeft = 0
runToRight = 1
walkToLeft = 2
walkToRight = 3

speed = 10

# run to Right
for x in range(0, 800, speed):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * runToRight,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.05)

curFrame = 0
#run to Left
for x in range(800, 0, -speed):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * runToLeft,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.05)

curFrame = 0
for x in range(0, 800, speed):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * walkToRight,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.1)

curFrame = 0
#run to Left
for x in range(800, 0, -speed):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * walkToLeft,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.1)
close_canvas()

