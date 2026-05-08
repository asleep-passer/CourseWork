from .Road import RoadModel, RoadType
from typing import Tuple, Optional

class RoadCellModel:
    def __init__(self, row: int, col: int,
                 road_type: RoadType = RoadType.OBSTACLE_ROAD,
                 road_model: Optional[RoadModel] = None) -> None:
        self.row = row
        self.col = col
        if road_model is not None:
            self.road_model = road_model
        else:
            self.road_model = RoadModel(road_type)

    def is_road(self) -> bool:
        return self.road_model.road_type != RoadType.OBSTACLE_ROAD

    def get_type(self) -> RoadType:
        return self.road_model.road_type

    def get_passable_directions(self) -> Tuple:
        return self.road_model.get_passable_direction()

    def rotate(self) -> None:
        self.road_model.rotate()

    def reset_rotation(self) -> None:
        self.road_model.reset()

    def get_position(self) -> Tuple[int, int]:
        return self.row, self.col

    def set_position(self, row: int, col: int) -> None:
        self.row = row
        self.col = col