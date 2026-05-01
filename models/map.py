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

    # ----- 方向匹配辅助 -----
    def _can_move(self, from_r, from_c, to_r, to_c, direction: Direction) -> bool:
        """检查从 (from) 到 (to) 沿 direction 方向是否可通行"""
        if not (0 <= to_r < self.rows and 0 <= to_c < self.cols):
            return False
        from_cell = self.grid[from_r][from_c]
        to_cell = self.grid[to_r][to_c]
        if from_cell is None or to_cell is None:
            return False
        if not from_cell.is_road() or not to_cell.is_road():
            return False

        # 当前格子该方向可通行
        if direction not in from_cell.get_passable_directions():
            return False

        # 邻居格子必须具有相反方向的可通行性
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if opposite[direction] not in to_cell.get_passable_directions():
            return False

        return True

    # ----- 连通性检测（DFS，只返回 bool）-----
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
        return self._dfs_check(start_pos[0], start_pos[1], end_pos, visited)

    def _dfs_check(self, row, col, end_pos, visited) -> bool:
        if (row, col) == end_pos:
            return True
        visited.add((row, col))
        cell = self.grid[row][col]
        for d in cell.get_passable_directions():
            nr, nc = row, col
            if d == Direction.UP:    nr -= 1
            elif d == Direction.DOWN:  nr += 1
            elif d == Direction.LEFT:  nc -= 1
            elif d == Direction.RIGHT: nc += 1

            if (nr, nc) not in visited and self._can_move(row, col, nr, nc, d):
                if self._dfs_check(nr, nc, end_pos, visited):
                    return True
        return False

    # ----- 获取路径（返回格子序列）-----
    def get_path(self) -> List[Tuple[int, int]]:
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
        if self._dfs_path(start_pos[0], start_pos[1], end_pos, visited, path):
            return path
        return []

    def _dfs_path(self, row, col, end_pos, visited, path) -> bool:
        path.append((row, col))
        if (row, col) == end_pos:
            return True
        visited.add((row, col))
        cell = self.grid[row][col]
        for d in cell.get_passable_directions():
            nr, nc = row, col
            if d == Direction.UP:    nr -= 1
            elif d == Direction.DOWN:  nr += 1
            elif d == Direction.LEFT:  nc -= 1
            elif d == Direction.RIGHT: nc += 1

            if (nr, nc) not in visited and self._can_move(row, col, nr, nc, d):
                if self._dfs_path(nr, nc, end_pos, visited, path):
                    return True
        path.pop()
        return False