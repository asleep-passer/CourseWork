from typing import Tuple, Optional
from .Road import RoadModel


class DragStateModel:
    """
    Temporary state model for road dragging operations.
    Maintains the currently dragged road instance and its position during interaction.

    Attributes:
        dragged_road (Optional[RoadModel]): The road instance being dragged, None if no drag in progress.
        current_position (Optional[Tuple[int, int]]): The current position (screen/grid coordinates) of the dragged road.
        is_dragging (bool): Flag indicating whether a drag operation is active.
    """

    def __init__(self) -> None:
        """Initialize an empty drag state."""
        self.dragged_road: Optional[RoadModel] = None
        self.current_position: Optional[Tuple[int, int]] = None
        self.is_dragging: bool = False

    def start_drag(self, road: RoadModel, start_position: Tuple[int, int]) -> None:
        """
        Begin a drag operation with the given road and starting position.

        Args:
            road (RoadModel): The road instance to be dragged.
            start_position (Tuple[int, int]): Initial position (x,y or row,col) of the drag.
        """
        self.dragged_road = road
        self.current_position = start_position
        self.is_dragging = True

    def update_position(self, new_position: Tuple[int, int]) -> None:
        """
        Update the current position of the dragged road during the drag.

        Args:
            new_position (Tuple[int, int]): New position (x,y or row,col) of the dragged road.
        """
        if self.is_dragging and self.dragged_road is not None:
            self.current_position = new_position

    def end_drag(self) -> Optional[RoadModel]:
        """
        End the drag operation, reset state, and return the dragged road.

        Returns:
            Optional[RoadModel]: The road that was dragged, None if no drag was in progress.
        """
        dragged_road = self.dragged_road
        self.dragged_road = None
        self.current_position = None
        self.is_dragging = False
        return dragged_road

    def cancel_drag(self) -> None:
        """Cancel the drag operation without keeping the road (e.g., if drag is aborted)."""
        self.dragged_road = None
        self.current_position = None
        self.is_dragging = False