"""Game level controller module.

Provides utilities to load level data from save files and convert it to the
runtime format expected by the game. The main class, `GameLevelController`,
encapsulates the level grid, available road counts, locked cells, and rotation
information.
"""

import config
from typing import List, Tuple, Optional
from models.Road import RoadType


class GameLevelController:
    """Container for temporary level data matching the hard-coded config
    structure.

    Attributes:
        map (List[List[str]]): 4x4 character grid containing 'S' (start), 'E'
            (end), 'O' (obstacle), or ' ' (empty).
        roads (Tuple[int,int,int,int]): Available road counts (straight, bend,
            T, cross).
        locked (List[List[bool]]): Lock state for each cell.
        rotation (List[List[int]]): Rotation counts (0-3) for each cell.
    """
    def __init__(self):
        self.map: List[List[str]] = []  # 4x4 grid containing 'S', 'E', 'O', ' '
        self.roads: Tuple[int, int, int, int] = (0, 0, 0, 0)  # (straight, bend, t_junction, cross)
        self.locked: List[List[bool]] = [[False]*4 for _ in range(4)]  # lock state
        self.rotation: List[List[int]] = [[0]*4 for _ in range(4)]  # rotation state (0-3) corresponding to (0,90,180,270) degrees

    @classmethod
    def load_from_file(cls, level_id: int) -> Optional['GameLevelController']:
        """Load level data from a file and convert it to the format matching
        the hard-coded configuration.
        """
        try:
            level_id = max(1, level_id)
            file_path = config.saves_path + "level" + str(level_id)+".txt"
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            if not lines:
                return None
                
            # Parse the first line: rows and cols
            rows, cols = map(int, lines[0].strip().split())
            data = cls()
            
            # Read the road type matrix
            current_line = 1
            road_types = []
            for _ in range(rows):
                if current_line >= len(lines):
                    break
                row = list(map(int, lines[current_line].strip().split()))
                road_types.append(row)
                current_line += 1
            
            # Read locked state
            data.locked = []
            for _ in range(rows):
                if current_line >= len(lines):
                    break
                row = list(map(int, lines[current_line].strip().split()))
                data.locked.append([bool(x) for x in row])
                current_line += 1
            
            # Read rotation state
            data.rotation = []
            for _ in range(rows):
                if current_line >= len(lines):
                    break
                row = list(map(int, lines[current_line].strip().split()))
                data.rotation.append(row)
                current_line += 1
            
            # Read available road counts
            if current_line < len(lines):
                available_roads = list(map(int, lines[current_line].strip().split()))
                # 确保有4个值，与硬编码配置匹配
                if len(available_roads) >= 4:
                    data.roads = tuple(available_roads[:4]) # type: ignore
            
            # Convert the road type matrix to the hard-coded config format
            # 5=START_ROAD -> 'S', 6=END_ROAD -> 'E', 0=OBSTACLE_ROAD -> 'O', 7=EMPTY -> ' '
            data.map = []
            for r in range(min(rows, 4)):  # 限制为4x4
                row_data = []
                for c in range(min(cols, 4)):
                    if r < len(road_types) and c < len(road_types[r]):
                        road_num = road_types[r][c]
                        if road_num == 5:
                            row_data.append('S')
                        elif road_num == 6:
                            row_data.append('E')
                        elif road_num == 0:
                            row_data.append('O')
                        else:  # 7 or other
                            row_data.append(' ')
                    else:
                        row_data.append(' ')
                data.map.append(row_data)
            
            # Ensure the map is 4x4
            while len(data.map) < 4:
                data.map.append([' '] * 4)
            for i in range(4):
                while len(data.map[i]) < 4:
                    data.map[i].append(' ')
            
            return data
            
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error loading level {level_id} from file: {e}")
            return None