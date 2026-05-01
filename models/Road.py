from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RoadType(Enum):
    OBSTACLE_ROAD = 0
    STRAIGHT_ROAD = 1
    BEND_ROAD = 2
    T_SHAPED_ROAD = 3
    CROSS_ROAD = 4
    START_ROAD = 5
    END_ROAD = 6


class RoadModel:
    def __init__(self, road_type: RoadType, rotated: int = 0):
        self.road_type = road_type
        self._rotated = rotated

        base = {
            RoadType.OBSTACLE_ROAD: (),
            RoadType.STRAIGHT_ROAD: (Direction.UP, Direction.DOWN),
            RoadType.BEND_ROAD: (Direction.UP, Direction.RIGHT),
            RoadType.T_SHAPED_ROAD: (Direction.UP, Direction.RIGHT, Direction.LEFT),
            RoadType.CROSS_ROAD: (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT),
            RoadType.START_ROAD: (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT),
            RoadType.END_ROAD: (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT),
        }

        self._passable = base.get(road_type, (Direction.UP,))

    def get_passable_direction(self):
        return tuple(
            Direction((d.value + self._rotated) % 4)
            for d in self._passable
        )

    def rotate(self):
        self._rotated = (self._rotated + 1) % 4

    def reset(self):
        self._rotated = 0