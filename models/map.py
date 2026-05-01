from typing import List, Tuple
from .roadcell import RoadCellModel
from .Road import RoadType, Direction

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
        """ For debugging, print out the road types in the grid. """
        for row in self.grid:
            print([cell.get_type().name for cell in row])

    def is_path_connected(self) -> bool:
        """
        Check if there is a valid connected path from START_ROAD to END_ROAD
        according to the passable directions of the roads.

        Returns:
            bool: True if start and end are connected, False otherwise
        """
        # Find the positions of start and end roads
        start_pos = None
        end_pos = None
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell and cell.get_type() == RoadType.START_ROAD:
                    start_pos = (row, col)
                if cell and cell.get_type() == RoadType.END_ROAD:
                    end_pos = (row, col)

        # Return false if start or end is missing
        if not start_pos or not end_pos:
            return False

        # Use DFS to check path connectivity
        visited = set()
        return self._dfs(start_pos[0], start_pos[1], end_pos, visited)

    def _dfs(self, row: int, col: int, end_pos: Tuple[int, int], visited: set) -> bool:
        """
        Private helper method: Depth-First Search to explore the path.
        """
        # Check grid boundaries
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        # Skip visited cells
        if (row, col) in visited:
            return False

        current_cell = self.grid[row][col]
        # Skip empty or obstacle cells
        if not current_cell or not current_cell.is_road():
            return False

        # Reach the end point
        if (row, col) == end_pos:
            return True

        visited.add((row, col))
        # Get all passable directions of current road
        directions = current_cell.get_passable_directions()

        # Explore all possible directions
        for direction in directions:
            next_r, next_c = row, col
            if direction == Direction.UP:
                next_r -= 1
            elif direction == Direction.DOWN:
                next_r += 1
            elif direction == Direction.LEFT:
                next_c -= 1
            elif direction == Direction.RIGHT:
                next_c += 1

            if self._dfs(next_r, next_c, end_pos, visited):
                return True

        visited.remove((row, col))
        return False