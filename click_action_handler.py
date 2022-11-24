from components.board import Grid
from components.cell import CellStates, Cube

# placeholder to remember the current pressed button
curr_pressed_place_holder: CellStates = CellStates.EMPTY


def set_pressed_place_holder(s: CellStates):
    global curr_pressed_place_holder
    curr_pressed_place_holder = s


def get_curr_dropper_state_place_holder() -> CellStates:
    global curr_pressed_place_holder
    return curr_pressed_place_holder


player: Cube = None  # placeholder to manage only single agent/player


def handle_click(board: Grid):
    global curr_pressed_place_holder, player
    cell_clicked: Cube = board.click()
    if cell_clicked is not None:
        if curr_pressed_place_holder == CellStates.AGENT:
            board.set_player(cell_clicked)
        cell_clicked.change_state(curr_pressed_place_holder)
        board.update_modifiers()
        board.draw()  # blit the board surface onto the WIN
