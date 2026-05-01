from enum import Enum
from typing import Optional, List, Tuple
import pygame as pg  # 仅用于计时 get_ticks，不影响主循环
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
            [' ', ' ', 'O', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "roads": (10, 6, 3, 1),  # 直道, 弯道, T型, 十字
    },
    2: {
        "map": [
            ['S', ' ', 'O', ' '],
            [' ', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', 'E']
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
        "roads": (6, 4, 2, 1),
    },
    4: {
        "map": [
            ['S', 'O', ' ', ' '],
            [' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'E']
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

        # 玩家道路列表（后面 load_level 会重新创建）
        self.player_road_list = player_road_list if player_road_list else NormalRoadListModel(10, 6, 3, 1)
        self.admin_road_list: Optional[AdminRoadListModel] = None

        # 计时相关
        self.start_time = 0          # 单位：毫秒
        self.elapsed_time = 0        # 单位：毫秒
        self.active = False          # 是否已开始计时

        if level_id in LEVEL_CONFIGS:
            self.load_level(level_id)

    def load_level(self, level_id: int):
        config = LEVEL_CONFIGS[level_id]
        layout = config["map"]
        base_roads = config["roads"]  # (直道, 弯道, T形, 十字)

        # 根据当前难度调整道路数量
        if self.difficulty == Difficulty.EASY:
            factor = 1.5
        elif self.difficulty == Difficulty.HARD:
            factor = 0.7
        else:
            factor = 1.0
        roads_cfg = tuple(max(0, int(x * factor)) for x in base_roads)

        # 清空地图
        self.map.reset()

        # 放置起点/终点/障碍（旋转逻辑保持不变）
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
                    if cell_type == RoadType.START_ROAD:
                        cell.rotate()          # 起点朝右
                    if cell_type == RoadType.END_ROAD:
                        if level_id == 3:      # 第三关终点朝左
                            cell.rotate()
                            cell.rotate()
                            cell.rotate()
                    self.map.set_cell(r, c, cell)

        # 重新创建玩家道路列表（数量已调整）
        self.player_road_list = NormalRoadListModel(*roads_cfg)
        self.score = 0
        self.is_complete = False

        # 重置计时器
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

    # ---------- 计时器操作 ----------
    def start_timer(self):
        """开始计时（第一次操作时调用）"""
        if not self.active:
            self.start_time = pg.time.get_ticks()
            self.active = True

    def update_time(self):
        """每帧调用，更新已用时间"""
        if self.active and not self.is_complete:
            self.elapsed_time = pg.time.get_ticks() - self.start_time

    def get_elapsed_seconds(self) -> float:
        return self.elapsed_time / 1000.0

    def calculate_final_score(self):
        """通关时根据时间和难度算分，数值可根据喜好调整"""
        seconds = self.get_elapsed_seconds()
        base = max(0, 1000 - int(seconds * 10))   # 每秒扣 10 分，最低 0
        multiplier = 1.0
        if self.difficulty == Difficulty.MEDIUM:
            multiplier = 1.5
        elif self.difficulty == Difficulty.HARD:
            multiplier = 2.0
        self.score = int(base * multiplier)

    # ---------- 胜利检测 ----------
    def check_completion(self) -> bool:
        connected = self.map.is_path_connected()
        if connected and not self.is_complete:
            self.is_complete = True
            self.calculate_final_score()
        return self.is_complete

    def get_path(self) -> List[Tuple[int, int]]:
        return self.map.get_path()

    def reset(self) -> None:
        # 重置到关卡初始状态
        self.load_level(self.level_id)