from pico2d import *
import game_framework
import game_world
import play_mode
import title_mode

image = None


def init():
    global image
    image = load_image('item_select.png')
    boy = play_mode.boy
    boy.pressed_keys.clear()
    boy.dir = 0
    if boy.state == 'RUN':
        boy.stop_run()


def finish():
    global image
    image = None


def handle_events():
    resume_requested = False
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
                game_framework.change_mode(title_mode)
                return
            elif event.key == SDLK_m:
                if not play_mode.item_key_down:
                    play_mode.item_key_down = True
                    resume_requested = True
            elif event.key in (SDLK_0, SDLK_1, SDLK_2):
                play_mode.boy.ball_size = {
                    SDLK_0: 0, SDLK_1: 21, SDLK_2: 41
                }[event.key]
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_m:
                play_mode.item_key_down = False
            elif event.key == SDLK_p:
                play_mode.pause_key_down = False
    if resume_requested:
        game_framework.pop_mode()


def update():
    play_mode.update()


def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()
