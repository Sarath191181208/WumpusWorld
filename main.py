import pygame
import pygame_gui
from buttons import createbuttons

from components.board import Grid
from components.cell import CellStates, Cube
from components.timer import Timer
from click_action_handler import handle_click, set_pressed_place_holder


SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wumpus World')
FPS = 60

board = Grid(WIN, rows=6, cols=6, width=400, height=400)
board.draw()

# timer used to manage the animation loop of solving of wumpus world
animation_timer = Timer(
    time=0.5, loop=True, func=lambda: solve_wumpus_game_loop(animation_timer))


def solve_wumpus_game_loop(animation_timer: Timer) -> None:
    should_stop = board.update_state()

    if should_stop:
        animation_timer.stop()
        animation_timer.start = False


manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()),
    #  os.path.join('themes','./themePygame_gui.json')
)


def handle_start_button_click(animation_timer: Timer):
    animation_timer.start_timer()
    print(f"{animation_timer.is_running=}")


name_action_dict = {
    "Wumpus": lambda: set_pressed_place_holder(CellStates.WUMPUS),
    "Pit": lambda: set_pressed_place_holder(CellStates.PIT),
    "Start": lambda: handle_start_button_click(animation_timer),
    "Gold": lambda: set_pressed_place_holder(CellStates.TREASURE),
    "Empty": lambda: set_pressed_place_holder(CellStates.EMPTY),
    "Player": lambda: set_pressed_place_holder(CellStates.AGENT),
}

y_tray_ending = createbuttons(
    name_action_dict,
    WIN=WIN,
    board=board,
    manager=manager
)


def main(animation_timer: Timer) -> None:
    run = True
    while run:
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                run = False

        is_click_left = pygame.mouse.get_pressed()[0]
        if is_click_left and not animation_timer.is_running:
            handle_click(board)

        board.update_surface()
        board.draw()

        time_delta = clock.tick(FPS)/1000.0
        manager.update(time_delta)
        manager.draw_ui(WIN)
        animation_timer.update()
        pygame.display.update()


if __name__ == "__main__":
    main(animation_timer=animation_timer)
