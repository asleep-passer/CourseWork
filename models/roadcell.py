from .road import RoadModel, RoadType

class RoadCellModel:
    def __init__(self, row: int, col: int, road_type: RoadType = RoadType.OBSTACLE_ROAD) -> None:
        self.row = row
        self.col = col
        self.road_model = RoadModel(road_type)

    def is_road(self) -> bool:
        """ Check whether this cell is a road (not an obstacle). """
        return self.road_model.road_type != RoadType.OBSTACLE_ROAD

    def get_type(self) -> RoadType:
        """ Return the current road type. """
        return self.road_model.road_type

    def get_passable_directions(self) -> Tuple:
        """ Get the passable directions considering rotations. """
        return self.road_model.get_passable_direction()

    def rotate(self) -> None:
        """ Rotate the road cell clockwise by 90 degrees. """
        self.road_model.rotate()

    def reset_rotation(self) -> None:
        """ Reset the rotation of the road. """
        self.road_model.reset()

    def get_position(self) -> Tuple[int, int]:
        """ Get the (row, col) position of the cell. """
        return self.row, self.col

    def set_position(self, row: int, col: int) -> None:
        """ Set the position of the cell. """
        self.row = row
        self.col = col