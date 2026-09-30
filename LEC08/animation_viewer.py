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
