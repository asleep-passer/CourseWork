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
        start_pos = None
        end_pos = None
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell and cell.get_type() == RoadType.START_ROAD:
                    start_pos = (row, col)
                if cell and cell.get_type() == RoadType.END_ROAD:
                    end_pos = (row, col)
        if not start_pos or not end_pos:
            return False
        visited = set()
        return self._dfs(start_pos[0], start_pos[1], end_pos, visited)

    def _dfs(self, row: int, col: int, end_pos: Tuple[int, int], visited: set) -> bool:
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in visited:
            return False
        current_cell = self.grid[row][col]
        if not current_cell or not current_cell.is_road():
            return False
        if (row, col) == end_pos:
            return True
        visited.add((row, col))
        for direction in current_cell.get_passable_directions():
            nr, nc = row, col
            if direction == Direction.UP:    nr -= 1
            elif direction == Direction.DOWN:  nr += 1
            elif direction == Direction.LEFT:  nc -= 1
            elif direction == Direction.RIGHT: nc += 1
            if self._dfs(nr, nc, end_pos, visited):
                return True
        # 不移除 visited
        return False

    def get_path(self) -> List[Tuple[int, int]]:
        """返回从起点到终点的路径（格子坐标列表），用于小车动画"""
        start_pos = None
        end_pos = None
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell and cell.get_type() == RoadType.START_ROAD:
                    start_pos = (row, col)
                if cell and cell.get_type() == RoadType.END_ROAD:
                    end_pos = (row, col)
        if not start_pos or not end_pos:
            return []
        path = []
        visited = set()
        if self._dfs_find_path(start_pos[0], start_pos[1], end_pos, visited, path):
            return path
        return []

    def _dfs_find_path(self, row, col, end_pos, visited, path) -> bool:
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in visited:
            return False
        cell = self.grid[row][col]
        if not cell or not cell.is_road():
            return False
        path.append((row, col))
        visited.add((row, col))
        if (row, col) == end_pos:
            return True
        for direction in cell.get_passable_directions():
            nr, nc = row, col
            if direction == Direction.UP:    nr -= 1
            elif direction == Direction.DOWN:  nr += 1
            elif direction == Direction.LEFT:  nc -= 1
            elif direction == Direction.RIGHT: nc += 1
            if self._dfs_find_path(nr, nc, end_pos, visited, path):
                return True
        path.pop()
        return False