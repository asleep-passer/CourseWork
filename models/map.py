from typing import List
from .roadcell import RoadCellModel
from .road import RoadType

class MapModel:
    def __init__(self, rows: int = 4, cols: int = 4) -> None:
        """
        Initialize the 4x4 map grid with road cells.
        """
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    def set_cell(self, row: int, col: int, road_cell: RoadCellModel) -> None:
        """ Set the road model in the grid at a specific (row, col). """
        self.grid[row][col] = road_cell

    def get_cell(self, row: int, col: int) -> RoadCellModel:
        """ Get the road cell at a specific (row, col). """
        return self.grid[row][col]

    def reset(self) -> None:
        """ Reset the grid to its initial state. """
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def print_grid(self) -> None:
        """ For debugging, print out the grid with road types. """
        for row in self.grid:
            print([cell.get_type().name for cell in row])