from enum import Enum
from typing import Optional
from .map import MapModel
from .roadlist import RoadListModel, NormalRoadListModel, AdminRoadListModel


class Difficulty(Enum):
    """Enumeration for game level difficulty settings."""
    EASY = 1
    MEDIUM = 2
    HARD = 3


class GameLevelModel:
    """
    Defines a game level, maintaining the grid map, available road lists, difficulty, and score.
    Provides core state management for a single game level.

    Attributes:
        map (MapModel): The grid map instance for this level.
        player_road_list (RoadListModel): Road list available to the player (normal roads).
        admin_road_list (Optional[AdminRoadListModel]): Optional admin road list for editing/debug modes.
        difficulty (Difficulty): The difficulty setting of the level.
        score (int): The player's current score in this level.
        is_complete (bool): Flag indicating whether the level has been successfully completed.
    """

    def __init__(self,
                 map_rows: int = 4,
                 map_cols: int = 4,
                 player_road_list: Optional[RoadListModel] = None,
                 difficulty: Difficulty = Difficulty.EASY,
                 initial_score: int = 0) -> None:
        """
        Initialize a new game level with a grid map, road lists, and difficulty.

        Args:
            map_rows (int): Number of rows in the level's grid map (default: 4).
            map_cols (int): Number of columns in the level's grid map (default: 4).
            player_road_list (Optional[RoadListModel]): Road list available to the player.
            difficulty (Difficulty): Difficulty level (EASY, MEDIUM, HARD) (default: EASY).
            initial_score (int): Starting score for the level (default: 0).
        """
        self.map = MapModel(rows=map_rows, cols=map_cols)
        self.default_road_config = (10, 6, 3, 1)

        if player_road_list is None:
            self.player_road_list = NormalRoadListModel(*self.default_road_config)
        else:
            self.player_road_list = player_road_list

        self.admin_road_list: Optional[AdminRoadListModel] = None
        self.difficulty = difficulty
        self.score = initial_score
        self.is_complete = False

    def set_admin_mode(self, enabled: bool = True) -> None:
        """
        Enable or disable admin mode with unlimited roads.

        Args:
            enabled (bool): True to enable admin mode, False to disable it.
        """
        if enabled:
            self.admin_road_list = AdminRoadListModel()
        else:
            self.admin_road_list = None

    def add_score(self, points: int) -> None:
        """
        Add points to the player's current score.

        Args:
            points (int): Number of points to add (positive or negative).
        """
        self.score += points

    def check_completion(self) -> bool:
        """
        Check if the level is completed based on the game rules.

        Returns:
            bool: True if the level is complete, False otherwise.
        """
        self.is_complete = self.score > 0
        return self.is_complete

    def reset(self) -> None:
        """Reset the level to its initial state: clear map, reset score and road counts."""
        self.map.reset()
        self.score = 0
        self.is_complete = False
        self.player_road_list = NormalRoadListModel(*self.default_road_config)