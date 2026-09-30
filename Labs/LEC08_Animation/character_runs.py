from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')



frame = 100
curFrame = frame
maxFrame = 800
frameType = 100
runToLeft = 0
runToRight = 1

# run to Right
for x in range(0, 800, 5):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * runToRight,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.05)

curFrame = frame
#run to Left
for x in range(800, 0, -5):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        curFrame, frameType * runToLeft,
        100, 100, x, 90
    )
    
    update_canvas()

    curFrame = (curFrame + frame) % maxFrame
    delay(0.05)
close_canvas()

