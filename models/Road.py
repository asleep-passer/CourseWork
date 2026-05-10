"""Road Model Module.
Define the enumeration for road types and directions, as well as the `RoadModel` class, which is responsible for representing the type and rotation status of a single road segment,
and calculate the current accessible direction. 
"""

from enum import Enum


class Direction(Enum):
    #Indicates the direction in which the road is accessible.
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RoadType(Enum):
    """Road type enumeration,
    used to distinguish different shapes and functions of road units."""
    OBSTACLE_ROAD = 0
    STRAIGHT_ROAD = 1
    BEND_ROAD = 2
    T_SHAPED_ROAD = 3
    CROSS_ROAD = 4
    START_ROAD = 5
    END_ROAD = 6


class RoadModel:
    """Model representing a single road unit. 
       Save the road type and the current rotation status, and be able to calculate the passable directions under the current rotation.
    """

    def __init__(self, road_type: RoadType, rotated: int = 0):
        """create`RoadModel`。

        Args:
            road_type (RoadType): roads type。
            rotated (int): Initial rotation count（0-3）
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
        #Return the passable directions tuple (Direction) under the current rotation status.
        return tuple(
            Direction((d.value + self._rotated) % 4)
            for d in self._passable
        )

    def rotate(self):
        #Rotate the road clockwise by 90 degrees (with the internal count increasing).
        self._rotated = (self._rotated + 1) % 4

    def reset(self):
        #Reset the road's rotation status to the initial direction (0).
        self._rotated = 0