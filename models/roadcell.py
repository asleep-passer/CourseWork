"""Road cell model module.

`RoadCellModel` wraps a `RoadModel` located at a single grid position and
provides convenient methods to query type, rotation, and position.
"""

from .Road import RoadModel, RoadType
from typing import Tuple, Optional


class RoadCellModel:
    """Represents a road unit in a map cell.

    It stores a `RoadModel`, coordinates, and provides common convenience
    operations.
    """

    def __init__(self, row: int, col: int,
                 road_type: RoadType = RoadType.OBSTACLE_ROAD,
                 road_model: Optional[RoadModel] = None) -> None:
        """Create a `RoadCellModel`.

        Args:
            row (int): Row coordinate.
            col (int): Column coordinate.
            road_type (RoadType): Road type to use if `road_model` is not provided.
            road_model (Optional[RoadModel]): Optional `RoadModel` instance to use.
        """
        self.row = row
        self.col = col
        if road_model is not None:
            self.road_model = road_model
        else:
            self.road_model = RoadModel(road_type)

    def is_road(self) -> bool:
        """Return whether this cell is a passable road (not an obstacle)."""
        return self.road_model.road_type != RoadType.OBSTACLE_ROAD

    def get_type(self) -> RoadType:
        """Return the `RoadType` of this cell."""
        return self.road_model.road_type

    def get_passable_directions(self) -> Tuple:
        """Return a tuple of passable directions for the road given its
        current rotation."""
        return self.road_model.get_passable_direction()

    def rotate(self) -> None:
        """Rotate the road clockwise by 90 degrees (increment internal
        rotation state)."""
        self.road_model.rotate()

    def reset_rotation(self) -> None:
        """Reset the road's rotation state to its initial orientation."""
        self.road_model.reset()

    def get_position(self) -> Tuple[int, int]:
        """Return the (row, col) coordinates of this cell."""
        return self.row, self.col

    def set_position(self, row: int, col: int) -> None:
        """Set the cell's coordinates (used when moving or editing)."""
        self.row = row
        self.col = col