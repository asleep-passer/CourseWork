"""Map model module.

`MapModel` manages a grid (default 4x4) for placing `RoadCellModel` instances
and provides pathfinding and lock-checking utilities.
"""

from typing import List, Tuple
from .roadcell import RoadCellModel
from .Road import RoadType, Direction


class MapModel:
    """Represents the map grid and operations related to road cells.

    Provides methods to set/get cells, check locks, and search for paths.
    """

    def __init__(self, rows: int = 4, cols: int = 4) -> None:
        """Initialize the map grid.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.lock_mask = [[False for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, row: int, col: int, road_cell: RoadCellModel) -> None:
        """Set a `RoadCellModel` at the specified position and update the
        lock mask according to the cell type.

        If `road_cell` is None, the lock for that position is cleared.

        Args:
            row (int): Row index.
            col (int): Column index.
            road_cell (RoadCellModel): The road cell to set, or None.
        """
        self.grid[row][col] = road_cell
        if road_cell is None:
            self.lock_mask[row][col] = False
            return
        road_type = road_cell.get_type()
        if road_type in [RoadType.START_ROAD, RoadType.END_ROAD, RoadType.OBSTACLE_ROAD]:
            self.lock_mask[row][col] = True
        else:
            self.lock_mask[row][col] = False

    def get_cell(self, row: int, col: int) -> RoadCellModel:
        """Return the `RoadCellModel` at the given position (may be None)."""
        return self.grid[row][col]

    def is_locked(self, row: int, col: int) -> bool:
        """Return whether the specified cell is locked (not movable)."""
        return self.lock_mask[row][col]

    def reset(self) -> None:
        """Reset the map by clearing all cells and unlocking all positions."""
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.lock_mask = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def _can_move(self, from_r, from_c, to_r, to_c, direction: Direction) -> bool:
        """Determine whether movement is possible from one cell to another in
        a given direction.

        Core checks include bounds, presence of road cells, and mutual
        passable directions between the two cells.
        """
        if not (0 <= to_r < self.rows and 0 <= to_c < self.cols):
            return False
        a = self.grid[from_r][from_c]
        b = self.grid[to_r][to_c]
        if a is None or b is None:
            return False
        if not a.is_road() or not b.is_road():
            return False
        if direction not in a.get_passable_directions():
            return False
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if opposite[direction] not in b.get_passable_directions():
            return False
        return True

    def is_path_connected(self) -> bool:
        """Return True if there exists a valid path from start to end on the map."""
        return len(self.get_path()) > 0

    def get_path(self) -> List[Tuple[int, int]]:
        """Find and return the cell-coordinate path from start to end using
        depth-first search.

        The returned list contains coordinates in visitation order. Returns an
        empty list if no path exists.
        """
        start, end = None, None
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell:
                    if cell.get_type() == RoadType.START_ROAD:
                        start = (r, c)
                    elif cell.get_type() == RoadType.END_ROAD:
                        end = (r, c)
        if not start or not end:
            return []

        visited = set()
        path = []

        def dfs(r, c):
            if (r, c) in visited:
                return False
            cell = self.grid[r][c]
            if cell is None or cell.get_type() == RoadType.OBSTACLE_ROAD:
                return False
            visited.add((r, c))
            path.append((r, c))
            if (r, c) == end:
                return True

            for d in cell.get_passable_directions():
                nr, nc = r, c
                if d == Direction.UP:      nr -= 1
                elif d == Direction.DOWN:  nr += 1
                elif d == Direction.LEFT:  nc -= 1
                elif d == Direction.RIGHT: nc += 1

                if self._can_move(r, c, nr, nc, d):
                    if dfs(nr, nc):
                        return True

            path.pop()
            visited.remove((r, c))
            return False

        if dfs(start[0], start[1]):
            return path
        return []

    def get_physical_path(self) -> List[Tuple[int, int]]:
        """Find a path from start to end by considering physical adjacency
        (up/down/left/right) only.

        Unlike `get_path`, which uses road exit directions to determine
        connectivity, `get_physical_path` searches using simple adjacency.
        """
        start = None
        end = None
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell:
                    if cell.get_type() == RoadType.START_ROAD:
                        start = (r, c)
                    elif cell.get_type() == RoadType.END_ROAD:
                        end = (r, c)
        if not start or not end:
            return []

        visited = set()
        path = []

        def dfs(r, c):
            if (r, c) in visited:
                return False
            cell = self.grid[r][c]
            if cell is None or cell.get_type() == RoadType.OBSTACLE_ROAD:
                return False
            visited.add((r, c))
            path.append((r, c))
            if (r, c) == end:
                return True
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if dfs(nr, nc):
                        return True
            path.pop()
            return False

        if dfs(start[0], start[1]):
            return path
        return []