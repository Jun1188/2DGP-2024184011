from pathlib import Path
from time import perf_counter

import pico2d

# 프레임 좌표: (left, top, width, height), 원점은 이미지 왼쪽 위.
IMAGE_WIDTH = 399
IMAGE_HEIGHT = 525
ACTIONS = [
    [
        (1, 39, 29, 38),
        (31, 40, 26, 38),
        (58, 39, 28, 38),
        (86, 40, 29, 38),
        (118, 40, 29, 38),
        (150, 40, 29, 38),
        (182, 40, 29, 38),
        (211, 39, 28, 37),
        (240, 39, 29, 37),
        (270, 45, 24, 31),
        (302, 51, 29, 25),
    ],
    [
        (8, 80, 26, 37),
        (37, 80, 25, 36),
        (63, 80, 33, 38),
        (97, 80, 37, 36),
        (135, 80, 32, 35),
        (170, 79, 32, 37),
        (206, 79, 26, 38),
        (238, 80, 24, 37),
        (263, 80, 30, 37),
        (295, 80, 35, 36),
        (334, 80, 32, 36),
        (370, 79, 29, 38),
    ],
    [
        (2, 124, 32, 39),
        (40, 124, 34, 38),
        (90, 125, 34, 37),
        (130, 123, 34, 39),
        (181, 123, 34, 40),
        (228, 123, 32, 38),
    ],
    [
        (1, 169, 29, 30),
        (35, 168, 29, 30),
        (67, 169, 30, 29),
        (98, 169, 31, 29),
        (131, 168, 29, 30),
        (162, 168, 29, 31),
        (193, 170, 30, 29),
        (230, 170, 31, 29),
        (268, 170, 30, 30),
    ],
    [
        (1, 206, 30, 27),
        (36, 206, 29, 27),
        (70, 206, 29, 27),
        (105, 206, 29, 27),
        (139, 206, 29, 27),
        (174, 206, 29, 27),
    ],
    [
        (1, 239, 29, 34),
        (36, 239, 30, 34),
        (75, 239, 30, 35),
        (111, 238, 31, 35),
        (149, 239, 30, 35),
        (186, 238, 31, 35),
    ],
    [
        (1, 283, 29, 34),
        (36, 283, 30, 34),
        (72, 286, 39, 31),
        (123, 285, 39, 32),
        (172, 286, 39, 31),
        (218, 285, 38, 32),
    ],
    [
        (1, 327, 24, 43),
        (31, 329, 29, 41),
        (65, 328, 20, 42),
        (90, 328, 25, 42),
        (119, 328, 25, 42),
        (149, 328, 20, 42),
        (184, 341, 39, 28),
        (232, 341, 38, 26),
    ],
    [
        (1, 379, 27, 37),
        (31, 379, 31, 36),
        (64, 379, 31, 36),
        (99, 377, 33, 38),
        (136, 379, 32, 35),
        (176, 379, 33, 36),
        (217, 379, 33, 36),
        (254, 378, 33, 36),
    ],
    [
        (6, 429, 34, 39),
        (49, 426, 34, 42),
        (96, 427, 23, 38),
        (125, 427, 23, 38),
    ],
]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCALE = 3
CENTER_X = 400
BASE_Y = 180
FRAME_DURATION = 0.1
LOOP_DELAY = 1.0 / 60.0
REPEAT_COUNT = 5
WAIT_DURATION = 1.0


def draw_frame(image, action_index, frame_index):
    left, top, width, height = ACTIONS[action_index][frame_index]
    bottom = IMAGE_HEIGHT - top - height
    draw_width = width * SCALE
    draw_height = height * SCALE
    image.clip_draw(left, bottom, width, height,
                    CENTER_X, BASE_Y + draw_height / 2,
                    draw_width, draw_height)


def main():
    image_path = Path(__file__).resolve().parent / "sonic-sprite.png"
    pico2d.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        try:
            if not image_path.is_file():
                raise FileNotFoundError("이미지 파일이 없습니다.")
            image = pico2d.load_image(str(image_path))
        except Exception as error:
            print(f"이미지 로드 실패: {image_path}\n{error}")
            return

        action_index = 0
        completed_repeats = 0
        waiting = False
        frame_index = 0
        elapsed = 0.0
        previous_time = perf_counter()
        running = True
        while running:
            for event in pico2d.get_events():
                if event.type == pico2d.SDL_QUIT:
                    running = False
                elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                    running = False
            if not running:
                break
            current_time = perf_counter()
            elapsed += current_time - previous_time
            previous_time = current_time
            # 대기 중에도 이벤트 처리와 화면 갱신을 계속한다.
            while True:
                duration = WAIT_DURATION if waiting else FRAME_DURATION
                if elapsed < duration:
                    break
                elapsed -= duration
                if waiting:
                    waiting = False
                    action_index = (action_index + 1) % len(ACTIONS)
                    completed_repeats = 0
                    frame_index = 0
                elif frame_index + 1 < len(ACTIONS[action_index]):
                    frame_index += 1
                else:
                    completed_repeats += 1
                    if completed_repeats == REPEAT_COUNT:
                        waiting = True
                    else:
                        frame_index = 0
            pico2d.clear_canvas()
            draw_frame(image, action_index, frame_index)
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    finally:
        pico2d.close_canvas()


if __name__ == "__main__":
    main()
