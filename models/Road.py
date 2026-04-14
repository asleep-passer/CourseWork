from enum import Enum
import pygame as pg

class Direction(Enum):
    UP=(0,1)
    DOWN=(0,-1)
    RIGHT=(1,0)
    LEFT=(-1,0)


class Road:
    class RoadType(Enum):
        STRAIGHT_ROAD=(Direction.UP,Direction.DOWN)#上下可通行
        BEND_ROAD=    (Direction.UP,Direction.RIGHT)#上右可通行
        T_SHAPED_ROAD=(Direction.UP,Direction.RIGHT,Direction.LEFT)#上右左可通行
        CROSS_ROAD=   (Direction.UP,Direction.DOWN,Direction.RIGHT,Direction.LEFT)#上下右左可通行

    def __init__(self,road_type:'Road.RoadType') -> None:
        self.passable_direction=road_type.value
        self.rotated=1
        self.position=pg.Vector2(0,0)
        print("A Road is created.")
        
