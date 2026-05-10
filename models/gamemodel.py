"""Game models module.

Contains models for game levels, the map, and road lists. These classes are
responsible for storing game state, loading level configurations, and
providing level-related operations. The primary class is `GameLevelModel`,
which represents the runtime state and behavior of a single level.
"""

from enum import Enum
from typing import Optional, List, Tuple
import os
import pygame as pg
import config
from .map import MapModel
from .roadlist import RoadListModel, NormalRoadListModel, AdminRoadListModel
from .roadcell import RoadCellModel
from .Road import RoadType, Direction


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


LEVEL_CONFIGS = {
    1: {
        "map": [
            ['S', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "roads": (10, 6, 3, 1),
    },
    2: {
        "map": [
            ['S', ' ', 'O', ' '],
            [' ', ' ', ' ', ' '],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', 'E']
        ],
        "roads": (8, 4, 2, 0),
    },
    3: {
        "map": [
            ['S', ' ', ' ', 'O'],
            [' ', 'O', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['O', ' ', ' ', 'E']
        ],
        "roads": (6, 4, 2, 1),
    },
    4: {
        "map": [
            ['S', ' ', 'O', ' '],
            [' ', ' ', ' ', 'O'],
            ['O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'E']
        ],
        "roads": (4, 4, 2, 0),
    }
}


class GameLevelModel:
    """Model class representing a single game level's state.

    Responsibilities include: loading level configurations, initializing the
    map and road resources, managing timing and score calculations, and
    checking level completion.
    """

    def __init__(self,
                 level_id: int = 1,
                 player_road_list: Optional[RoadListModel] = None,
                 difficulty: Difficulty = Difficulty.EASY,
                 initial_score: int = 0) -> None:
        """Initialize a `GameLevelModel` instance.

        Args:
            level_id (int): Level identifier used to load built-in or custom levels.
            player_road_list (Optional[RoadListModel]): Optional road list for the player.
            difficulty (Difficulty): Difficulty level affecting initial road counts and scoring.
            initial_score (int): Initial score.
        """
        self.level_id = level_id
        self.map = MapModel(rows=4, cols=4)
        self.difficulty = difficulty
        self.score = initial_score
        self.is_complete = False

        self.player_road_list = player_road_list if player_road_list else NormalRoadListModel(10, 6, 3, 1)
        self.admin_road_list: Optional[AdminRoadListModel] = None

        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

        if level_id in LEVEL_CONFIGS:
            self.load_level(level_id)

    def load_level(self, level_id: int):
        """Load and initialize level data from built-in `LEVEL_CONFIGS` or an
        external file.

        Road counts are adjusted according to the current difficulty and map
        cells are initialized as `RoadCellModel` instances.

        Args:
            level_id (int): Level identifier.
        """
        if level_id in LEVEL_CONFIGS:
            config = LEVEL_CONFIGS[level_id]
            layout = config["map"]
            base_roads = config["roads"]
        else:
            self._load_from_file(level_id)
            return

        if self.difficulty == Difficulty.EASY:
            factor = 1.5
        elif self.difficulty == Difficulty.HARD:
            factor = 0.7
        else:
            factor = 1.0
        roads_cfg = tuple(max(0, int(x * factor)) for x in base_roads)

        self.map.reset()

        for r in range(4):
            for c in range(4):
                char = layout[r][c]
                cell_type = None
                if char == 'S':
                    cell_type = RoadType.START_ROAD
                elif char == 'E':
                    cell_type = RoadType.END_ROAD
                elif char == 'O':
                    cell_type = RoadType.OBSTACLE_ROAD
                if cell_type is not None:
                    cell = RoadCellModel(r, c, cell_type)
                    if cell_type == RoadType.START_ROAD:
                        cell.rotate()
                    if cell_type == RoadType.END_ROAD:
                        if level_id == 3:
                            cell.rotate()
                            cell.rotate()
                            cell.rotate()
                    self.map.set_cell(r, c, cell)

        self.player_road_list = NormalRoadListModel(*roads_cfg)
        self.score = 0
        self.is_complete = False
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

    def _load_from_file(self, level_id: int):
        """Load a custom level from a save file and initialize the model.

        The file format is expected to contain a type grid, lock/rotation
        information, and road counts.

        Args:
            level_id (int): Custom level file identifier.

        Raises:
            FileNotFoundError: If the level file does not exist.
            ValueError: If the file format is invalid.
        """
        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Custom level file {file_path} not found")

        with open(file_path, 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) < 2:
                raise ValueError("Invalid level file format")

            # Read the type grid (lines 1-4)
            type_grid = []
            for i in range(4):
                type_grid.append(list(map(int, lines[1 + i].split())))
            # Locked state (lines 5-8) may appear before the rotation grid in
            # the file; we skip or read appropriately to keep offsets correct.
            # Rotation grid (lines 9-12)
            rotation_grid = []
            for i in range(4):
                idx = 9 + i
                if idx < len(lines):
                    rotation_grid.append(list(map(int, lines[idx].split())))
                else:
                    rotation_grid.append([0, 0, 0, 0])

            # The last line contains road counts
            last_line = lines[-1] if lines else "10 6 3 1"
            raw_counts = list(map(int, last_line.split()))
            while len(raw_counts) < 4:
                raw_counts.append(0)
            raw_counts = raw_counts[:4]

        if self.difficulty == Difficulty.EASY:
            factor = 1.5
        elif self.difficulty == Difficulty.HARD:
            factor = 0.7
        else:
            factor = 1.0
        road_counts = tuple(max(0, int(x * factor)) for x in raw_counts)

        self.map.reset()
        for r in range(4):
            for c in range(4):
                t = type_grid[r][c]
                cell = None
                if t == 5:
                    cell = RoadCellModel(r, c, RoadType.START_ROAD)
                elif t == 6:
                    cell = RoadCellModel(r, c, RoadType.END_ROAD)
                elif t == 0:
                    cell = RoadCellModel(r, c, RoadType.OBSTACLE_ROAD)
                if cell:
                    # Apply the saved rotation counts
                    for _ in range(rotation_grid[r][c]):
                        cell.rotate()
                    self.map.set_cell(r, c, cell)

        self.player_road_list = NormalRoadListModel(*road_counts)
        self.score = 0
        self.is_complete = False
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False

    @classmethod
    def load_from_custom_file(cls, level_id: int, difficulty: Difficulty = Difficulty.EASY):
        model = cls.__new__(cls)
        model.level_id = level_id
        model.map = MapModel(rows=4, cols=4)
        model.difficulty = difficulty
        model.score = 0
        model.is_complete = False
        model.admin_road_list = None
        model.start_time = 0
        model.elapsed_time = 0
        model.active = False

        """Create and return a `GameLevelModel` instance loaded from a custom
        level file for tools or editors.

        Use case: level editors or tools that need to preview a custom level
        without starting the full game.

        Args:
            level_id (int): Custom level identifier.
            difficulty (Difficulty): Difficulty to apply when loading.

        Returns:
            GameLevelModel: The loaded model instance.
        """
        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Custom level file {file_path} not found")

        with open(file_path, 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) < 2:
                raise ValueError("Invalid level file format")

            # Read the type grid
            type_grid = []
            for i in range(4):
                type_grid.append(list(map(int, lines[1 + i].split())))

            # Skip locked state and read rotation grid
            rotation_grid = []
            for i in range(4):
                idx = 9 + i
                if idx < len(lines):
                    rotation_grid.append(list(map(int, lines[idx].split())))
                else:
                    rotation_grid.append([0, 0, 0, 0])

            # The last line contains road counts
            last_line = lines[-1] if lines else "10 6 3 1"
            raw_counts = list(map(int, last_line.split()))
            while len(raw_counts) < 4:
                raw_counts.append(0)
            raw_counts = raw_counts[:4]

        if difficulty == Difficulty.EASY:
            factor = 1.5
        elif difficulty == Difficulty.HARD:
            factor = 0.7
        else:
            factor = 1.0
        road_counts = tuple(max(0, int(x * factor)) for x in raw_counts)

        model.player_road_list = NormalRoadListModel(*road_counts)

        for r in range(4):
            for c in range(4):
                t = type_grid[r][c]
                cell = None
                if t == 5:
                    cell = RoadCellModel(r, c, RoadType.START_ROAD)
                elif t == 6:
                    cell = RoadCellModel(r, c, RoadType.END_ROAD)
                elif t == 0:
                    cell = RoadCellModel(r, c, RoadType.OBSTACLE_ROAD)
                if cell:
                    # Apply saved rotation counts
                    for _ in range(rotation_grid[r][c]):
                        cell.rotate()
                    model.map.set_cell(r, c, cell)

        return model

    def set_admin_mode(self, enabled: bool = True) -> None:
        """Toggle admin mode. In admin mode, the road list contains unlimited roads.

        Args:
            enabled (bool): Whether to enable admin mode.
        """
        if enabled:
            self.admin_road_list = AdminRoadListModel()
        else:
            self.admin_road_list = None

    def add_score(self, points: int) -> None:
        """Add the specified number of points to the current score.

        Args:
            points (int): Points to add.
        """
        self.score += points

    def start_timer(self):
        """Start the level timer (records start time in milliseconds)."""
        if not self.active:
            self.start_time = pg.time.get_ticks()
            self.active = True

    def update_time(self):
        """Update elapsed time (in milliseconds) using pygame's timer."""
        if self.active and not self.is_complete:
            self.elapsed_time = pg.time.get_ticks() - self.start_time

    def get_elapsed_seconds(self) -> float:
        """Return elapsed time in seconds as a float."""
        return self.elapsed_time / 1000.0

    def calculate_final_score(self):
        """Calculate the final score based on elapsed time and difficulty, and
        store it in `self.score`.
        """
        seconds = self.get_elapsed_seconds()
        base = max(0, 1000 - int(seconds * 10))
        multiplier = 1.0
        if self.difficulty == Difficulty.MEDIUM:
            multiplier = 1.5
        elif self.difficulty == Difficulty.HARD:
            multiplier = 2.0
        self.score = int(base * multiplier)

    def check_completion(self) -> bool:
        """Check whether there is a connected path from the start to end on
        the map.

        If a path is found and the level is not already marked complete, this
        will calculate the final score and set `is_complete` to True.

        Returns:
            bool: True if the level is complete.
        """
        connected = self.map.is_path_connected()
        if connected and not self.is_complete:
            self.is_complete = True
            self.calculate_final_score()
        return self.is_complete

    def get_path(self) -> List[Tuple[int, int]]:
        """Return the cell-coordinate path from start to end on the current
        map, if one exists."""
        return self.map.get_path()

    def reset(self) -> None:
        """Reset the level to its initially loaded state."""
        self.load_level(self.level_id)