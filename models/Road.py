from enum import Enum

class Direction(Enum):
    UP=   0
    RIGHT=1
    DOWN= 2
    LEFT= 3

class RoadModel:
    class RoadType(Enum):
        OBSTACLE_ROAD=0
        STRAIGHT_ROAD=1
        BEND_ROAD=    2
        T_SHAPED_ROAD=3
        CROSS_ROAD=   4
        START_ROAD=   5
        END_ROAD=     6

    def __init__(self,road_type:RoadType) -> None:
        self.road_type=road_type
        
        if road_type==self.RoadType.OBSTACLE_ROAD:
            self.passable_direction=()
        elif road_type==self.RoadType.STRAIGHT_ROAD:
            self.passable_direction=(Direction.UP,Direction.DOWN)
        elif road_type==self.RoadType.BEND_ROAD:
            self.passable_direction=(Direction.UP,Direction.RIGHT)
        elif road_type==self.RoadType.T_SHAPED_ROAD:
            self.passable_direction=(Direction.UP,Direction.RIGHT,Direction.LEFT)
        else:
            self.passable_direction=(Direction.UP,Direction.RIGHT,Direction.DOWN,Direction.LEFT)

        self.rotated=0
        print(f"A {self.road_type.__str__}is created.")

    def get_passable_direction(self):
        cur_passable_direction=[]
        for dir in self.passable_direction:
            cur_passable_direction.append(Direction((dir.value+self.rotated)%4))
        return cur_passable_direction
    
    def rotate(self):
        self.rotated+=1

    def reset(self):
        self.rotated=0


        
