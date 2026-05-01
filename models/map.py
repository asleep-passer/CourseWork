from typing import List, Tuple
from .roadcell import RoadCellModel
from .Road import RoadType, Direction

class MapModel:
    def __init__(self, rows: int = 4, cols: int = 4) -> None:
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.lock_mask = [[False for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, row: int, col: int, road_cell: RoadCellModel) -> None:
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
        return self.grid[row][col]

    def is_locked(self, row: int, col: int) -> bool:
        return self.lock_mask[row][col]

    def reset(self) -> None:
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.lock_mask = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def is_path_connected(self) -> bool:
        path = self.get_path()
        return len(path) > 0

    def get_path(self) -> List[Tuple[int, int]]:
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
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if dfs(nr, nc):
                        return True
            path.pop()
            return False

        if dfs(start[0], start[1]):
            return path
        return []