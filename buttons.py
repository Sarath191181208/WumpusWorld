import pygame
import pygame_gui
from components.button import Button
from components.board import Grid


def createbuttons(name_action_dict: dict, WIN: pygame.Surface, board: Grid, manager: pygame_gui.UIManager) -> int:
    """ 
        Returns:
        ---- 
         y: int 
            The y co-ordinate where the button tray ends
    """
    row_items = ((WIN.get_width()-board.width)-10)//60
    row_gap = 15
    col_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    start = board.width
    y = 20
    n = 1
    y_count = 0

    # creating buttons
    for name, func in name_action_dict.items():
        Button(relative_rect=pygame.Rect(
            (start+n*row_gap, y + y_count*col_gap),
            (60, 45)),
            text=name,
            manager=manager,
            tool_tip_text=None,
            func=func)

        # updating so the buttons will go next to each other
        start += 50
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 45

    return y
