from pico2d import *

delayTime = 0.02
windowH = 600
windowW = 800

frame = 100
maxFrame = frame * 8
frameType = 100

open_canvas(windowW, windowH)

# 여기를 채우시오.

character = load_image('Soldier.png')
grass = load_image('grass.png')
clear_canvas()


die = frameType * 0
angry = frameType * 1
attack_charge = frameType * 2

