from enum import Enum
from typing import Optional, List, Tuple
from .map import MapModel
from .roadlist import RoadListModel, NormalRoadListModel, AdminRoadListModel
from .roadcell import RoadCellModel
from .Road import RoadType

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

# 关卡预设：每个元组为 (地图布局, 道路数量配置, 难度)
# 地图布局：一个 4x4 字符串列表，'S'起点, 'E'终点, 'O'障碍, ' '空地
LEVEL_CONFIGS = {
    1: {
        "map": [
            ['S', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', 'O'],
            [' ', ' ', ' ', 'E']
        ],
        "roads": (10, 6, 3, 1),  # 直道, 弯道, T型, 十字
        "difficulty": Difficulty.EASY
    },
    2: {
        "map": [
            ['S', ' ', 'O', ' '],
            [' ', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "roads": (8, 4, 2, 0),
        "difficulty": Difficulty.EASY
    },
    3: {
        "map": [
            ['S', ' ', ' ', 'O'],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['O', ' ', ' ', 'E']
        ],
        "roads": (6, 4, 2, 1),
        "difficulty": Difficulty.MEDIUM
    },
    4: {
        "map": [
            ['S', 'O', ' ', ' '],
            [' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'E']
        ],
        "roads": (4, 4, 2, 0),
        "difficulty": Difficulty.HARD
    }
}

class GameLevelModel:
    def __init__(self,
                 level_id: int = 1,
                 player_road_list: Optional[RoadListModel] = None,
                 difficulty: Difficulty = Difficulty.EASY,
                 initial_score: int = 0) -> None:
        self.level_id = level_id
        self.map = MapModel(rows=4, cols=4)
        self.player_road_list = player_road_list if player_road_list else NormalRoadListModel(10, 6, 3, 1)
        self.admin_road_list: Optional[AdminRoadListModel] = None
        self.difficulty = difficulty
        self.score = initial_score
        self.is_complete = False
        # 如果提供了关卡 ID，则加载预设
        if level_id in LEVEL_CONFIGS:
            self.load_level(level_id)

    def load_level(self, level_id: int):
        config = LEVEL_CONFIGS[level_id]
        self.difficulty = config["difficulty"]
        layout = config["map"]
        roads_cfg = config["roads"]
        # 根据布局填充 map
        for r in range(4):
            for c in range(4):
                cell_type = None
                char = layout[r][c]
                if char == 'S':
                    cell_type = RoadType.START_ROAD
                elif char == 'E':
                    cell_type = RoadType.END_ROAD
                elif char == 'O':
                    cell_type = RoadType.OBSTACLE_ROAD
                if cell_type is not None:
                    cell = RoadCellModel(r, c, cell_type)
                    self.map.set_cell(r, c, cell)
        # 重新设置玩家可用道路（重置数量）
        self.player_road_list = NormalRoadListModel(*roads_cfg)
        self.score = 0
        self.is_complete = False

    def set_admin_mode(self, enabled: bool = True) -> None:
        if enabled:
            self.admin_road_list = AdminRoadListModel()
        else:
            self.admin_road_list = None

    def add_score(self, points: int) -> None:
        self.score += points

    def check_completion(self) -> bool:
        self.is_complete = self.map.is_path_connected()
        return self.is_complete

    def get_path(self) -> List[Tuple[int, int]]:
        return self.map.get_path()

    def reset(self) -> None:
        # 重置到关卡初始状态
        self.load_level(self.level_id)