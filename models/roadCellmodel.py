from enum import Enum
from typing import Tuple, List

# ----------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# RoadModel
# ----------------------------------------------------------------------
class RoadModel:
    """
    Define the road,
    provide road type information, rotation information,
    destination information, and reset function.

    Attributes:
        road_type (RoadType):                         The type of road.
        __passable_direction (Tuple[Direction, ...]): The directions that the road can reach.
        __rotated (int):                              The number of times the road has been rotated.
    """

    def __init__(self, road_type: RoadType) -> None:
        """
        Create a new RoadModel with type and
        automatically set its other attributes according to the type.

        Args:
            road_type (RoadType): The type of the road.
        """
        self.road_type = road_type

        # Set the directions that the road can reach depending on the type of road.
        if road_type == RoadType.OBSTACLE_ROAD:
            self.__passable_direction = ()
        elif road_type == RoadType.STRAIGHT_ROAD:
            self.__passable_direction = (Direction.UP, Direction.DOWN)
        elif road_type == RoadType.BEND_ROAD:
            self.__passable_direction = (Direction.UP, Direction.RIGHT)
        elif road_type == RoadType.T_SHAPED_ROAD:
            self.__passable_direction = (Direction.UP, Direction.RIGHT, Direction.LEFT)
        else:  # CROSS_ROAD, START_ROAD, END_ROAD
            self.__passable_direction = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)

        self.__rotated = 0

        print(f"A {self.road_type} is created.")

    def get_passable_direction(self) -> Tuple[Direction, ...]:
        """
        Return current directions that the road can reach.

        Returns:
            Tuple[Direction, ...]: Current directions that the road can reach.
        """
        cur_passable_direction = []
        for d in self.__passable_direction:
            # Rotate clockwise: each direction value increases by 1 (mod 4)
            cur_passable_direction.append(Direction((d.value + self.__rotated) % 4))
        return tuple(cur_passable_direction)

    def rotate(self) -> None:
        """
        Rotate the road clockwise by 90 degrees.
        """
        self.__rotated += 1

    def reset(self) -> None:
        """
        Reset the attributes of the road.
        """
        self.__rotated = 0

    def get_rotation_count(self) -> int:
        """
        Return the number of clockwise rotations applied.

        Returns:
            int: Rotation count modulo 4 is effectively the rotation state.
        """
        return self.__rotated % 4


# ----------------------------------------------------------------------
# RoadCellModel
# ----------------------------------------------------------------------
class RoadCellModel:
    """
    Represents a road cell in a grid. Manages road information, grid position,
    and provides interoperability with the grid map.

    Attributes:
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        road_model (RoadModel): The actual road model containing type and rotation state.
    """

    def __init__(self, row: int, col: int, road_type: RoadType = RoadType.OBSTACLE_ROAD) -> None:
        """
        Create a new road cell.

        Args:
            row (int): Row index.
            col (int): Column index.
            road_type (RoadType): Type of the road, default is obstacle.
        """
        self.row = row
        self.col = col
        self.road_model = RoadModel(road_type)

    def is_road(self) -> bool:
        """
        Check whether this cell is a passable road (not an obstacle).

        Returns:
            bool: True if it's a road (not OBSTACLE_ROAD), otherwise False.
        """
        return self.road_model.road_type != RoadType.OBSTACLE_ROAD

    def get_type(self) -> RoadType:
        """Return the current road type."""
        return self.road_model.road_type

    def get_passable_directions(self) -> Tuple[Direction, ...]:
        """
        Get the passable directions of this road cell (considering rotations).

        Returns:
            Tuple[Direction, ...]: Directions through which the road can be traversed.
        """
        return self.road_model.get_passable_direction()

    def rotate(self) -> None:
        """Rotate the road clockwise by 90 degrees."""
        self.road_model.rotate()

    def reset_rotation(self) -> None:
        """Reset the rotation state of the road."""
        self.road_model.reset()

    def get_position(self) -> Tuple[int, int]:
        """Return the (row, col) position of the cell."""
        return self.row, self.col

    def set_position(self, row: int, col: int) -> None:
        """Set the position of the cell."""
        self.row = row
        self.col = col

    def get_neighbor_in_direction(self, direction: Direction) -> Tuple[int, int]:
        """
        Compute the coordinates of the neighboring cell in a given direction.

        Args:
            direction (Direction): The direction to move.

        Returns:
            Tuple[int, int]: (row, col) of the neighbor.
        """
        delta = {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
        }
        dr, dc = delta[direction]
        return self.row + dr, self.col + dc

    def get_connected_neighbors(self, grid_map: List[List['RoadCellModel']]) -> List['RoadCellModel']:
        """
        Get all neighboring road cells that are connected (both directions allow passage).

        Args:
            grid_map (List[List[RoadCellModel]]): The entire grid map.

        Returns:
            List[RoadCellModel]: List of connected neighboring RoadCellModel objects.
        """
        neighbors = []
        for direction in self.get_passable_directions():
            nr, nc = self.get_neighbor_in_direction(direction)
            if 0 <= nr < len(grid_map) and 0 <= nc < len(grid_map[0]):
                neighbor_cell = grid_map[nr][nc]
                if neighbor_cell.is_road():
                    opposite = Direction((direction.value + 2) % 4)
                    if opposite in neighbor_cell.get_passable_directions():
                        neighbors.append(neighbor_cell)
        return neighbors

    def __repr__(self) -> str:
        return (f"RoadCellModel(row={self.row}, col={self.col}, "
                f"type={self.road_model.road_type}, rotated={self.road_model.get_rotation_count()})")


# ----------------------------------------------------------------------
# Example usage (optional, for testing)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create a 2x2 grid
    grid = [
        [RoadCellModel(0, 0, RoadType.START_ROAD), RoadCellModel(0, 1, RoadType.STRAIGHT_ROAD)],
        [RoadCellModel(1, 0, RoadType.OBSTACLE_ROAD), RoadCellModel(1, 1, RoadType.END_ROAD)]
    ]

    # Rotate the first cell and check connections
    grid[0][0].rotate()
    print(grid[0][0].get_passable_directions())
    print("Connected neighbors of (0,0):", grid[0][0].get_connected_neighbors(grid))