import pygame

from .cell import Cube, CellStates


class Grid():

    def __init__(self, WIN, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows, self.cols = rows, cols

        cube_height = height/self.rows
        cube_width = width/self.cols

        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.cubes = [
            [Cube(value=CellStates.EMPTY, row=i, col=j, width=cube_width, height=cube_height, win=self.surface)
                for j in range(self.cols)]
            for i in range(self.rows)
        ]

        self.width, self.height = width, height

        self.win = WIN
        self.update_surface()
        self.draw() if self.win is not None else 0

        self.player: Cube = None

        self._wumpus_stack = list()
        self._visited = set()
        self._start = False

    def draw_grid(self, win=None) -> None:
        '''Draw the grid'''
        # win = win if win is not None else self.win
        win = self.surface
        thick = 1
        BLACK = (0, 0, 0)

        cube_height = self.height / self.rows
        cube_width = self.width / self.cols
        # horizontal lines -----
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*cube_height),
                             (self.width, cube_height*i), thick)
        # vertical lines |||
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*cube_width, 0),
                             (cube_width*i, self.height))

    def draw(self, win=None) -> None:
        """ Draws the boards canvas onto the screen"""
        win = self.win if win is None else win
        win.blit(self.surface, (0, 0))

    def update_surface(self):
        """ Recreates the whole surface """
        # Draw Cubes
        win = self.surface
        for row in self.cubes:
            for cube in row:
                cube.draw(win)

        # drawing grid
        self.draw_grid(win)

    def is_out_of_bounds(self, row: int, col: int) -> bool:
        return col >= self.cols or col < 0 or row >= self.rows or row < 0

    def click(self, pos=None) -> None or Cube:
        '''
            Returns the Cube object based on the pos of mouse or given pos
        '''

        # x,y mapping in pygame
        if pos is None:
            col, row = pygame.mouse.get_pos()

        cube_height = self.height/self.rows
        cube_width = self.width/self.cols

        col //= cube_width
        row //= cube_height
        # to remove the trailing zero
        col, row = int(col), int(row)

        if self.is_out_of_bounds(row, col):
            return None

        return self.get(row, col)

    def _get_adjacent_cells(self, row: int, col: int) -> list[Cube]:
        helper_arr = []
        for i, j in (
            (row-1, col),  # left
            (row+1, col),  # right
            (row, col-1),  # top
            (row, col+1)  # bottom
        ):
            if self.is_out_of_bounds(i, j):
                continue
            else:
                helper_arr.append(self.get(i, j))
        return helper_arr

    def update_modifiers(self) -> None:
        """updates all the cells with new modifiers"""
        for row in self.cubes:
            for cube in row:
                cube.modifiers.clear()

        for row in self.cubes:
            for cube in row:
                self.update_neighbours(cube)

        # update the surface
        self.update_surface()

    def update_neighbours(self, cell: Cube) -> None:
        row, col = cell.row, cell.col

        if cell.state == CellStates.WUMPUS:
            for cell in self._get_adjacent_cells(row, col):
                cell.add_modifier(CellStates.STENCH)

        elif cell.state == CellStates.PIT:
            for cell in self._get_adjacent_cells(row, col):
                cell.add_modifier(CellStates.BREEZE)

    def set_player(self, cell: Cube) -> None:
        if self.player is not None:
            self.player.state = CellStates.EMPTY
        cell.state = CellStates.AGENT
        self.player = cell

    def get(self, x: int, y: int) -> Cube:
        return self.cubes[x][y]

    def update_state(self) -> bool:
        if len(self._wumpus_stack) == 0 and self._start == False:
            self._wumpus_params_reset()
            self._start = True
        return self._update_next_board_state()

    def _wumpus_params_reset(self):
        self._wumpus_stack = [self.player]
        self._visited.clear()

    def _update_next_board_state(self) -> bool:
        player = self.player
        curr_row, curr_col = player.row, player.col
        if len(self._wumpus_stack) == 0:
            self._wumpus_params_reset()
            self._start = False
            return True

        cell = self._wumpus_stack.pop()
        if cell.state == CellStates.TREASURE:
            print("Way Found")
            self._start = False
            self._wumpus_params_reset()
            self.update_surface()
            self.draw()
            return True

        self.set_player(cell)
        adj_cells = self._get_adjacent_cells(curr_row, curr_col)

        def valid_cell(cell: Cube):
            if cell in self._visited:
                return False
            self._visited.add(cell)
            return cell.state == CellStates.EMPTY or cell.state == CellStates.TREASURE

        adj_cells = [cell for cell in adj_cells if valid_cell(cell)]
        n = len(adj_cells)
        if player.is_dangerous():
            for cell in adj_cells: cell._prob_score *= 1/n
            adj_cells.sort(key=lambda cell: cell._prob_score, reverse=True)
        self._wumpus_stack.extend(adj_cells)
        self.update_surface()
        self.draw()

        return False
