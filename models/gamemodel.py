from enum import Enum
from typing import Optional, List, Tuple
import pygame as pg
from .map import MapModel
from .roadlist import RoadListModel, NormalRoadListModel, AdminRoadListModel
from .roadcell import RoadCellModel
from .Road import RoadType
from control.gamelevel import GameLevelController


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

LEVEL_CONFIGS = {
    1: {
        "map": [
            ['S', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "roataion":[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ],
        "roads": (10, 6, 3, 1),
    },
    2: {
        "map": [
            ['S', ' ', 'O', ' '],
            [' ', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "rotation":[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ],
        "roads": (8, 4, 2, 0),
    },
    3: {
        "map": [
            ['S', ' ', ' ', 'O'],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['O', ' ', ' ', 'E']
        ],
        "rotation":[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ],
        "roads": (6, 4, 2, 1),
    },
    4: {
        "map": [
            ['S', 'O', ' ', ' '],
            [' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'E']
        ],
        "rotation":[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ],
        "roads": (4, 4, 2, 0),
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
        self.difficulty = difficulty
        self.score = initial_score
        self.is_complete = False

        self.player_road_list = player_road_list if player_road_list else NormalRoadListModel(10, 6, 3, 1)
        self.admin_road_list: Optional[AdminRoadListModel] = None

        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

        self.load_level(level_id)

    def load_level(self, level_id: int):
        """
        优先从文件加载关卡，如果文件不存在则使用硬编码配置
        保持方法签名不变，但内部逻辑改为优先文件加载
        """
        # 尝试从文件加载
        file_data = GameLevelController.load_from_file(level_id)
    
        if file_data:
            # 使用文件数据
            layout = file_data.map
            base_roads = file_data.roads
            rotation=file_data.rotation
            print(f"Loaded level {level_id} from file")
        elif level_id in LEVEL_CONFIGS:
            # 回退到硬编码配置
            config_data = LEVEL_CONFIGS[level_id]
            layout = config_data["map"]
            base_roads = config_data["roads"]
            rotation=config_data["rotation"]
            print(f"Loaded level {level_id} from built-in config")
        else:
            # 默认配置
            layout = [
                ['S', ' ', ' ', ' '],
                [' ', 'O', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'E']
            ]
            base_roads = (10, 6, 3, 1)
            rotation=[
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]
            ]
            print(f"No config found for level {level_id}, using default")

        # 应用难度系数（这部分逻辑保持不变）
        if self.difficulty == Difficulty.EASY:
            factor = 1.5
        elif self.difficulty == Difficulty.HARD:
            factor = 0.7
        else:
            factor = 1.0
        roads_cfg = tuple(max(0, int(x * factor)) for x in base_roads)

        # 重置地图并填充（这部分逻辑保持不变）
        self.map.reset()
        for r in range(4):
            for c in range(4):
                cell_type = None
                char = layout[r][c]
                rotate=rotation[r][c]
                if char == 'S':
                    cell_type = RoadType.START_ROAD
                elif char == 'E':
                    cell_type = RoadType.END_ROAD
                elif char == 'O':
                    cell_type = RoadType.OBSTACLE_ROAD
                if cell_type is not None:
                    cell = RoadCellModel(r, c, cell_type)
                    for _ in range(rotate):
                        cell.rotate()
                        
                    self.map.set_cell(r, c, cell)

        # 设置道路列表
        self.player_road_list = NormalRoadListModel(*roads_cfg)
    
        # 重置游戏状态
        self.score = 0
        self.is_complete = False
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

    def set_admin_mode(self, enabled: bool = True) -> None:
        if enabled:
            self.admin_road_list = AdminRoadListModel()
        else:
            self.admin_road_list = None

    def add_score(self, points: int) -> None:
        self.score += points
    def start_timer(self):
        if not self.active:
            self.start_time = pg.time.get_ticks()
            self.active = True

    def update_time(self):
        if self.active and not self.is_complete:
            self.elapsed_time = pg.time.get_ticks() - self.start_time

    def get_elapsed_seconds(self) -> float:
        return self.elapsed_time / 1000.0

    def calculate_final_score(self):
        seconds = self.get_elapsed_seconds()
        base = max(0, 1000 - int(seconds * 10))
        multiplier = 1.0
        if self.difficulty == Difficulty.MEDIUM:
            multiplier = 1.5
        elif self.difficulty == Difficulty.HARD:
            multiplier = 2.0
        self.score = int(base * multiplier)

    def check_completion(self) -> bool:
        connected = self.map.is_path_connected()
        if connected and not self.is_complete:
            self.is_complete = True
            self.calculate_final_score()
        return self.is_complete

    def get_path(self) -> List[Tuple[int, int]]:
        return self.map.get_path()

    def reset(self) -> None:
        self.load_level(self.level_id)