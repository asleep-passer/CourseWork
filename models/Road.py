"""道路模型模块。

定义道路类型、方向枚举以及 `RoadModel` 类，负责表示单个道路单元的类型与旋转状态，
并计算当前可通行方向。
"""

from enum import Enum


class Direction(Enum):
    """表示道路可通行的方向。"""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RoadType(Enum):
    """道路类型枚举，用于区分不同形状与功能的道路单元。"""
    OBSTACLE_ROAD = 0
    STRAIGHT_ROAD = 1
    BEND_ROAD = 2
    T_SHAPED_ROAD = 3
    CROSS_ROAD = 4
    START_ROAD = 5
    END_ROAD = 6


class RoadModel:
    """表示单个道路单元的模型。

    保存道路类型与当前旋转状态，并能计算在当前旋转下的可通行方向。
    """

    def __init__(self, road_type: RoadType, rotated: int = 0):
        """创建 `RoadModel`。

        Args:
            road_type (RoadType): 道路类型。
            rotated (int): 初始旋转次数（0-3）。
        """
        self.road_type = road_type
        self._rotated = rotated

        base = {
            RoadType.OBSTACLE_ROAD: (),
            RoadType.STRAIGHT_ROAD: (Direction.UP, Direction.DOWN),
            RoadType.BEND_ROAD: (Direction.UP, Direction.RIGHT),
            RoadType.T_SHAPED_ROAD: (Direction.UP, Direction.RIGHT, Direction.LEFT),
            RoadType.CROSS_ROAD: (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT),
            RoadType.START_ROAD: (Direction.UP,),
            RoadType.END_ROAD: (Direction.UP,)
        }

        self._passable = base[road_type]

    def get_passable_direction(self):
        """返回在当前旋转状态下的可通行方向元组（Direction）。"""
        return tuple(
            Direction((d.value + self._rotated) % 4)
            for d in self._passable
        )

    def rotate(self):
        """将道路顺时针旋转 90 度（内部计数递增）。"""
        self._rotated = (self._rotated + 1) % 4

    def reset(self):
        """重置道路的旋转状态为初始方向（0）。"""
        self._rotated = 0