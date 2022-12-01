from typing import Union
import pygame
from enum import Enum
from .colors import *


class CellStates(Enum):
    EMPTY = WHITE
    AGENT = PINK
    PIT = BLACK
    WUMPUS = GREEN
    TREASURE = YELLOW
    BREEZE = BLUE
    STENCH = VIOLET

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(str(txt), True, fontColour)


class Cube():
    def __init__(self, value: CellStates, row: int, col: int, width: float, height: float, win: pygame.Surface):
        self.state: CellStates = value
        # left, top, width, height
        self.rect = pygame.Rect(col*width, row*height, width, height)
        self.win = win

        self.row, self.col = row, col
        self._cell_height, self._cell_width = height, width
        self.modifiers = set()
        
        self._prob_score:float() = 1

    def _get_rects(self) -> list[tuple[CellStates, pygame.Rect]]:
        cell_w, cell_h = self._cell_height, self._cell_height
        r, c = self.row, self.col
        half_w, half_h = cell_w//2, cell_h//2
        x, y = c*cell_w, r*cell_h
        modifiers = list(self.modifiers)
        len_modifiers = len(modifiers)

        if len_modifiers == 0 or self.state == CellStates.AGENT:
            return [
                (self.state, self.rect)
            ]

        if len_modifiers == 1:  # split the whole space into half
            if self.state == CellStates.EMPTY:
                return [(modifiers[0], pygame.Rect(x, y, cell_w, cell_h))]
            return [
                (modifiers[0], pygame.Rect(x, y, half_w, cell_h)),
                (self.state,   pygame.Rect(x+half_w, y, half_w, cell_h)),
            ]

        if len_modifiers == 2:  # split the whole space into three sections
            if self.state == CellStates.EMPTY:
                return [
                    (modifiers[0], pygame.Rect(x, y, half_w, cell_h)),
                    (modifiers[1], pygame.Rect(x+half_w, y, half_w, cell_h)),
                ]
            return[
                (modifiers[0], pygame.Rect(x, y, half_w, half_h)),
                (modifiers[1], pygame.Rect(x+half_w, y, half_w, half_h)),
                (self.state,   pygame.Rect(x, y+half_h, cell_w, half_h)),
            ]

    def draw(self, win=None) -> None:
        win = self.win if win is None else win
        cell_w, cell_h = self._cell_height, self._cell_height
        r, c = self.row, self.col
        x, y = c*cell_w, r*cell_h
        for cell_state, rect in self._get_rects():
            pygame.draw.rect(win, cell_state.value, rect)
        
        text = PYtxt(round(self._prob_score, 2), 12)
        win.blit(text, (x + (cell_w/2 - text.get_width()/2),
                        y + (cell_h/2 - text.get_height()/2)))

    def add_modifier(self, state: CellStates) -> None:
        self.modifiers.add(state)

    def change_state(self, state: CellStates) -> None:
        self.state = state
    
    def is_dangerous(self) -> bool:
        def _helper_is_dangerous(s):
            if s in (CellStates.BREEZE, CellStates.STENCH):
                return True
        if _helper_is_dangerous(self.state): return True
        for mod in self.modifiers:
            if _helper_is_dangerous(mod): return True
        
        return False

    def __str__(self) -> str:
        return f"Cell(row: {self.row}, col: {self.col}, state: {self.state})"
