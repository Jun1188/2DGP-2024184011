"""두 캐릭터가 정해진 순서로 만나는 애니메이션 뷰어."""

from math import pi, sin
from pathlib import Path
from time import perf_counter

from pico2d import *

RESOURCE_DIR = Path(__file__).resolve().parent

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GROUND_Y = 85
DISPLAY_HEIGHT = 300  # 실제 캐릭터의 높이를 화면 높이의 절반으로 표시한다.
DISPLAY_MAX_WIDTH = 430
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0

# 각 항목은 원본 시트의 (왼쪽, 아래, 너비, 높이)이다.
SOLDIER_IDLE = (
    (41, 643, 15, 18), (141, 643, 15, 18),
    (241, 643, 15, 19), (341, 643, 15, 19),
    (441, 643, 15, 18), (541, 643, 15, 18),
)

SOLDIER_WALK = (
    (41, 543, 15, 18), (141, 544, 15, 18),
    (241, 543, 15, 18), (341, 543, 15, 17),
    (441, 543, 15, 18), (541, 544, 15, 18),
    (641, 543, 15, 18), (741, 543, 15, 17),
)

SOLDIER_ATTACK = (
    (41, 343, 15, 18), (141, 347, 19, 22),
    (243, 348, 18, 20), (342, 341, 28, 23),
    (442, 341, 28, 17), (542, 341, 28, 18),
)

SOLDIER_HURT = (
    (40, 143, 16, 18), (140, 143, 16, 18),
    (240, 143, 16, 18), (340, 143, 16, 18),
)

# Sonic 시트는 행마다 프레임 폭과 높이가 달라 개별 좌표를 사용한다.
SONIC_IDLE = (
    (1, 447, 29, 39), (31, 447, 29, 38),
    (60, 447, 30, 39), (90, 447, 26, 38),
)

SONIC_RUN = (
    (8, 408, 26, 37), (37, 407, 32, 38),
    (70, 408, 31, 37), (102, 410, 32, 35),
    (135, 410, 32, 35), (170, 408, 32, 38),
    (206, 408, 26, 38), (238, 408, 27, 37),
)

SONIC_JUMP = (
    (1, 361, 33, 40), (39, 362, 35, 39),
    (89, 362, 35, 38), (130, 362, 34, 42),
    (181, 362, 34, 41), (228, 363, 33, 40),
)

SONIC_ROLL = (
    (1, 326, 29, 30), (35, 327, 29, 31),
    (67, 327, 30, 29), (99, 327, 30, 29),
    (131, 327, 29, 30), (162, 326, 29, 31),
    (193, 326, 30, 29), (230, 326, 31, 29),
    (268, 325, 30, 30),
)

# (프레임들, 초당 프레임 수)
ANIMATIONS = {
    "soldier_idle": (SOLDIER_IDLE, 6),
    "soldier_walk": (SOLDIER_WALK, 9),
    "soldier_attack": (SOLDIER_ATTACK, 12),
    "soldier_hurt": (SOLDIER_HURT, 8),
    "sonic_idle": (SONIC_IDLE, 6),
    "sonic_run": (SONIC_RUN, 12),
    "sonic_jump": (SONIC_JUMP, 9),
    "sonic_roll": (SONIC_ROLL, 12),
}

def draw_character(image, frame, x, foot_y, direction):
    left, bottom, width, height = frame
    scale = min(DISPLAY_HEIGHT / height, DISPLAY_MAX_WIDTH / width)
    draw_width = width * scale
    draw_height = height * scale
    flip = "h" if direction == "left" else ""
    image.clip_composite_draw(
        left, bottom, width, height, 0, flip,
        x, foot_y + draw_height / 2, draw_width, draw_height,
    )

def draw_scene(grass, soldier, sonic, soldier_frame, sonic_frame,
               soldier_x, sonic_x, soldier_direction, sonic_direction,
               sonic_jump_height):
    clear_canvas()
    grass.draw(CANVAS_WIDTH / 2, 31)
    draw_character(soldier, soldier_frame, soldier_x, GROUND_Y,
                   soldier_direction)
    draw_character(sonic, sonic_frame, sonic_x,
                   GROUND_Y + sonic_jump_height, sonic_direction)
    update_canvas()

# 각 캐릭터 값: (애니메이션, 시작 x, 끝 x, 바라보는 방향)
APPROACH = {
    "soldier": ("soldier_walk", 130, 330, "right"),
    "sonic": ("sonic_run", 670, 470, "left"),
}
STANDOFF = {
    "soldier": ("soldier_idle", 330, 330, "right"),
    "sonic": ("sonic_idle", 470, 470, "left"),
}

STRIKE = {
    "soldier": ("soldier_attack", 330, 330, "right"),
    "sonic": ("sonic_jump", 470, 250, "left"),
    "jump": True,
}

COUNTER = {
    "soldier": ("soldier_hurt", 330, 390, "right"),
    "sonic": ("sonic_roll", 250, 340, "right"),
}
