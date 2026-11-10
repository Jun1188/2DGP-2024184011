from pico2d import *
import game_framework
import game_world
import title_mode
import pause_mode
import item_mode
from boy import Boy
from grass import Grass

boy = None
pause_started_at = 0.0
pause_key_down = False
item_key_down = False
world_paused = False


def handle_events():
    global pause_key_down, item_key_down, world_paused
    requested_mode = None
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not pause_key_down:
                pause_key_down = True
                requested_mode = pause_mode
        elif event.type == SDL_KEYUP and event.key == SDLK_p:
            pause_key_down = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m:
            if not item_key_down:
                item_key_down = True
                requested_mode = item_mode
        elif event.type == SDL_KEYUP and event.key == SDLK_m:
            item_key_down = False
        else:
            boy.handle_event(event)
    if requested_mode is not None:
        world_paused = requested_mode is pause_mode
        game_framework.push_mode(requested_mode)


def init():
    global boy, pause_key_down, item_key_down, world_paused
    pause_key_down = False
    item_key_down = False
    world_paused = False
    boy = Boy()
    game_world.add_oject(boy)
    game_world.add_oject(Grass(), 0)


def finish():
    global boy
    game_world.clear()
    boy = None


def pause():
    global pause_started_at
    if world_paused:
        pause_started_at = get_time()


def resume():
    # 일시정지 시간은 수면 대기 시간에서 제외한다.
    if world_paused:
        boy.idle_started_at += get_time() - pause_started_at
    direction = (int(SDLK_RIGHT in boy.pressed_keys) -
                 int(SDLK_LEFT in boy.pressed_keys))
    if boy.state == 'RUN':
        boy.dir = direction
        if direction == 0:
            boy.stop_run()
        else:
            boy.face_dir = direction


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
