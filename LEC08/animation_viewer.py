"""각 캐릭터의 5종 동작을 5회씩 재생하고 1초 정지한 뒤 무한 반복한다."""

from math import pi, sin
from pathlib import Path
from time import perf_counter

from pico2d import *

RESOURCE_DIR = Path(__file__).resolve().parent

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GROUND_Y = 150
DISPLAY_HEIGHT = CANVAS_HEIGHT / 2
DISPLAY_MAX_WIDTH = 430
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
BODY_GAP = 10
ROLL_REACH = 80

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

SOLDIER_SHOOT = (
    (41, 243, 19, 18), (141, 243, 17, 18),
    (241, 243, 17, 19), (341, 243, 17, 18),
    (441, 243, 22, 18), (541, 243, 21, 17),
    (641, 243, 20, 17), (741, 243, 36, 18),
    (841, 242, 23, 19),
)

# Sonic 시트는 행마다 프레임 폭과 높이가 달라 개별 좌표를 사용한다.
SONIC_IDLE = (
    (1, 447, 29, 39), (31, 447, 26, 38),
    (118, 447, 30, 38), (150, 447, 30, 38),
)

SONIC_RUN = (
    (8, 408, 26, 37), (37, 408, 27, 37),
    (65, 407, 31, 38), (97, 408, 37, 37),
    (135, 410, 32, 35), (170, 408, 32, 38),
    (206, 408, 26, 38), (238, 408, 24, 37),
)

SONIC_JUMP = (
    (1, 361, 33, 40), (39, 362, 35, 39),
    (89, 362, 35, 38), (130, 362, 34, 42),
    (181, 362, 34, 41), (228, 363, 33, 40),
)

SONIC_ROLL = (
    (1, 326, 29, 30), (35, 327, 29, 31),
    (67, 327, 30, 29), (98, 327, 31, 29),
    (131, 327, 29, 30), (162, 326, 29, 31),
    (193, 326, 30, 29), (230, 326, 31, 29),
    (268, 325, 30, 30),
)

SONIC_SPIN = (
    (1, 251, 29, 35), (36, 251, 30, 35),
    (74, 251, 31, 35), (111, 251, 31, 36),
    (149, 251, 30, 35), (186, 251, 31, 36),
)

# (프레임들, 장면 길이를 정하는 기준 초당 프레임 수)
ANIMATIONS = {
    "soldier_idle": (SOLDIER_IDLE, 6),
    "soldier_walk": (SOLDIER_WALK, 9),
    "soldier_attack": (SOLDIER_ATTACK, 12),
    "soldier_hurt": (SOLDIER_HURT, 8),
    "soldier_shoot": (SOLDIER_SHOOT, 12),
    "sonic_idle": (SONIC_IDLE, 6),
    "sonic_run": (SONIC_RUN, 12),
    "sonic_jump": (SONIC_JUMP, 9),
    "sonic_roll": (SONIC_ROLL, 12),
    "sonic_spin": (SONIC_SPIN, 10),
}

def displayed_size(frame):
    _, _, width, height = frame
    # 두 캐릭터의 높이를 일정하게 유지하고 넓은 공격 효과만 가로로 제한한다.
    draw_width = min(width * DISPLAY_HEIGHT / height, DISPLAY_MAX_WIDTH)
    return draw_width, DISPLAY_HEIGHT


def hit_box(frame, x, foot_y):
    width, height = displayed_size(frame)
    return (x - width / 2, foot_y, x + width / 2, foot_y + height)


def boxes_overlap(first, second):
    return (first[0] < second[2] and first[2] > second[0]
            and first[1] < second[3] and first[3] > second[1])


def keep_apart(soldier_frame, soldier_x, sonic_frame, sonic_x,
               sonic_foot_y):
    soldier_box = hit_box(soldier_frame, soldier_x, GROUND_Y)
    sonic_box = hit_box(sonic_frame, sonic_x, sonic_foot_y)
    # 점프로 두 박스의 높이가 분리되면 Sonic이 위로 지나갈 수 있다.
    if sonic_box[1] >= soldier_box[3] or sonic_box[3] <= soldier_box[1]:
        return sonic_x
    if sonic_box[0] >= soldier_box[2] + BODY_GAP:
        return sonic_x
    if sonic_box[2] <= soldier_box[0] - BODY_GAP:
        return sonic_x

    sonic_width, _ = displayed_size(sonic_frame)
    if sonic_x >= soldier_x:
        return soldier_box[2] + BODY_GAP + sonic_width / 2
    return soldier_box[0] - BODY_GAP - sonic_width / 2


def roll_attack_box(sonic_box, direction):
    if direction == "left":
        return (sonic_box[0] - ROLL_REACH, sonic_box[1],
                sonic_box[0], sonic_box[3])
    return (sonic_box[2], sonic_box[1],
            sonic_box[2] + ROLL_REACH, sonic_box[3])


def draw_character(image, frame, x, foot_y, direction):
    left, bottom, width, height = frame
    draw_width, draw_height = displayed_size(frame)
    flip = "h" if direction == "left" else ""
    image.clip_composite_draw(
        left, bottom, width, height, 0, flip,
        x, foot_y + draw_height / 2, draw_width, draw_height,
    )

def draw_scene(soldier, sonic, soldier_frame, sonic_frame,
               soldier_x, sonic_x, soldier_direction, sonic_direction,
               sonic_jump_height):
    clear_canvas()
    draw_character(soldier, soldier_frame, soldier_x, GROUND_Y,
                   soldier_direction)
    draw_character(sonic, sonic_frame, sonic_x,
                   GROUND_Y + sonic_jump_height, sonic_direction)
    update_canvas()

# 각 캐릭터 값: (애니메이션, 시작 x, 끝 x, 바라보는 방향)
APPROACH = {
    "soldier": ("soldier_walk", 130, 225, "right"),
    "sonic": ("sonic_run", 650, 610, "left"),
}
STANDOFF = {
    "soldier": ("soldier_idle", 225, 225, "right"),
    "sonic": ("sonic_idle", 610, 610, "left"),
}

RANGED = {
    "soldier": ("soldier_shoot", 225, 225, "right"),
    "sonic": ("sonic_spin", 610, 650, "left"),
}

STRIKE = {
    "soldier": ("soldier_attack", 225, 225, "right"),
    "sonic": ("sonic_jump", 650, 620, "left"),
    "jump": True,
}

COUNTER = {
    "soldier": ("soldier_hurt", 225, 180, "right"),
    "sonic": ("sonic_roll", 620, 480, "left"),
    "counter": True,
}

RETURN = {
    "soldier": ("soldier_walk", 180, 130, "left"),
    "sonic": ("sonic_run", 480, 650, "right"),
}
# 양쪽 캐릭터는 각 장면에서 자신의 동작을 5회 재생한다.
# 장면 끝의 정지 시간은 PAUSE_SECONDS이며, 마지막 장면 뒤에는 처음으로 돌아간다.
PHASES = (APPROACH, STANDOFF, RANGED, STRIKE, COUNTER, RETURN)

def frame_at(animation_name, elapsed, duration):
    frames, _ = ANIMATIONS[animation_name]
    total_frames = len(frames) * REPEAT_COUNT
    frame_number = min(int(elapsed / duration * total_frames), total_frames - 1)
    return frames[frame_number % len(frames)]


def phase_duration(phase, hit_at=None):
    soldier_name = phase["soldier"][0]
    sonic_name = phase["sonic"][0]
    soldier_frames, soldier_fps = ANIMATIONS[soldier_name]
    sonic_frames, sonic_fps = ANIMATIONS[sonic_name]
    soldier_duration = len(soldier_frames) / soldier_fps * REPEAT_COUNT
    sonic_duration = len(sonic_frames) / sonic_fps * REPEAT_COUNT
    duration = max(soldier_duration, sonic_duration)
    if phase.get("counter"):
        if hit_at is None:
            return sonic_duration + duration  # 접촉을 기다리는 동안 종료하지 않는다.
        return hit_at + duration
    return duration

def position_at(character, elapsed, duration):
    _, start_x, end_x, _ = character
    progress = min(elapsed / duration, 1.0)
    return start_x + (end_x - start_x) * progress

def draw_phase(phase, elapsed, soldier, sonic, hit_at=None):
    duration = phase_duration(phase, hit_at)
    active_time = min(elapsed, duration)  # 남은 1초 동안 마지막 자세로 멈춘다.
    soldier_data = phase["soldier"]
    sonic_data = phase["sonic"]
    progress = active_time / duration
    jump_height = 90 * sin(pi * progress) if phase.get("jump") else 0
    soldier_x = position_at(soldier_data, active_time, duration)
    soldier_frame = frame_at(soldier_data[0], active_time, duration)
    sonic_frames, sonic_fps = ANIMATIONS[sonic_data[0]]
    sonic_duration = len(sonic_frames) / sonic_fps * REPEAT_COUNT
    sonic_x = position_at(sonic_data, active_time, sonic_duration)
    sonic_frame = frame_at(sonic_data[0], active_time, duration)

    if phase.get("counter"):
        if hit_at is None:
            soldier_x = soldier_data[1]
            soldier_frame = frame_at("soldier_idle", active_time, duration)
            sonic_frame = frame_at("sonic_run", active_time, sonic_duration)
        else:
            hurt_elapsed = active_time - hit_at
            reaction_duration = duration - hit_at
            soldier_x = position_at(soldier_data, hurt_elapsed,
                                    reaction_duration)
            soldier_frame = frame_at("soldier_hurt", hurt_elapsed,
                                     reaction_duration)
            sonic_frame = frame_at("sonic_roll", hurt_elapsed,
                                   reaction_duration)

    sonic_foot_y = GROUND_Y + jump_height
    sonic_x = keep_apart(soldier_frame, soldier_x, sonic_frame,
                         sonic_x, sonic_foot_y)
    if phase.get("counter") and hit_at is None:
        soldier_box = hit_box(soldier_frame, soldier_x, GROUND_Y)
        sonic_box = hit_box(sonic_frame, sonic_x, sonic_foot_y)
        if boxes_overlap(roll_attack_box(sonic_box, sonic_data[3]),
                         soldier_box):
            hit_at = active_time
            reaction_duration = phase_duration(phase, hit_at) - hit_at
            soldier_frame = frame_at("soldier_hurt", 0, reaction_duration)
            sonic_frame = frame_at("sonic_roll", 0, reaction_duration)
            sonic_x = keep_apart(soldier_frame, soldier_x, sonic_frame,
                                 sonic_x, sonic_foot_y)

    draw_scene(
        soldier, sonic,
        soldier_frame, sonic_frame,
        soldier_x, sonic_x,
        soldier_data[3], sonic_data[3], jump_height,
    )
    return hit_at

def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        soldier = load_image(str(RESOURCE_DIR / "Soldier.png"))
        sonic = load_image(str(RESOURCE_DIR / "sonic-sprite.png"))
        phase_index = 0
        phase_start = perf_counter()
        hit_at = None
        running = True

        while running:
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False
            if not running:
                break

            phase = PHASES[phase_index]
            elapsed = perf_counter() - phase_start
            if elapsed >= phase_duration(phase, hit_at) + PAUSE_SECONDS:
                phase_index = (phase_index + 1) % len(PHASES)
                phase_start = perf_counter()
                hit_at = None
                phase = PHASES[phase_index]
                elapsed = 0.0

            hit_at = draw_phase(phase, elapsed, soldier, sonic, hit_at)
            delay(1 / 60)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
