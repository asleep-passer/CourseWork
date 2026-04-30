from enum import Enum

class Direction(Enum):
    UP=   0
    RIGHT=1
    DOWN= 2
    LEFT= 3

class RoadModel:
    """
    Define the road, 
    provide road type information, rotation information, 
    destination information, and reset function.

    Attributes:
        road_type (RoadType):                       The type of road.
        passable_direction (Tuple[Direction, ...]): The directions that the road can reach.
        roated (int):                               The number of times the road has been rotated.
    """
    class RoadType(Enum):
        OBSTACLE_ROAD=0
        STRAIGHT_ROAD=1
        BEND_ROAD=    2
        T_SHAPED_ROAD=3
        CROSS_ROAD=   4
        START_ROAD=   5
        END_ROAD=     6

    def __init__(self,road_type:RoadType) -> None:
        """
        Create a new RoadModel with type and 
        automatically set its other attributes according to the type.

        Args:
            road_type (RoadType): The type of the road.
        """
        self.road_type=road_type

        #Set the directions that the road can reach depending on the type of road.
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

        print(f"A {self.road_type} is created.")

    def get_passable_direction(self):
        """
        Return current directions that the road can reach.

        Returns:
            Tuple[Direction, ...]: Current directions that the road can reach.
        """

        cur_passable_direction=[]

        for dir in self.passable_direction:
            cur_passable_direction.append(Direction((dir.value+self.rotated)%4))
        
        return tuple(cur_passable_direction)
    
    def rotate(self):
        """
        Rotate the road clockwise by 90 degrees.
        """
        self.rotated+=1

    def reset(self):
        """
        Reset the attributes of the road.
        """
        self.rotated=0


        
