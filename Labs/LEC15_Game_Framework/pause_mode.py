from pico2d import *
import game_framework
import game_world
import play_mode
import title_mode


def init():
    pass


def finish():
    pass


def handle_events():
    resume_requested = False
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not play_mode.pause_key_down:
                play_mode.pause_key_down = True
                resume_requested = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_p:
                play_mode.pause_key_down = False
            elif event.key == SDLK_m:
                play_mode.item_key_down = False
            elif event.key in (SDLK_LEFT, SDLK_RIGHT):
                play_mode.boy.pressed_keys.discard(event.key)
    if resume_requested:
        game_framework.pop_mode()


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    # 추가 이미지 없이 화면 중앙에 일시정지 기호를 표시한다.
    draw_rectangle(370, 270, 390, 330)
    draw_rectangle(410, 270, 430, 330)
    update_canvas()
