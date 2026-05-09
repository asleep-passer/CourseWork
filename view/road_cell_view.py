import pygame
from models.roadcell import RoadCellModel
from view.road import RoadView


class RoadCellView:
    """A view component that renders a single road cell within a grid layout.

    Displays a semi-transparent grid background and delegates road rendering to
    a :class:`RoadView`. Additionally overlays labels or borders for special
    cell types such as start, end, or obstacle roads.

    Attributes:
        rect (pygame.Rect): The screen rectangle defining the cell's position and size.
        screen (pygame.Surface): The Pygame surface to draw onto.
        _road_view (RoadView or None): The current road view instance, if any.
        _current_cell (RoadCellModel or None): The model currently associated with this view.
        font (pygame.font.Font): Font used for rendering labels like 'S' or 'E'.
        GRID_SIZE (int): Number of sub-cells in the background grid (currently 1).
        ALPHA (int): Alpha transparency value for background and border colors.
        BG_COLOR (tuple[int, int, int, int]): Background color of the grid cell (RGBA).
        BORDER_COLOR (tuple[int, int, int, int]): Border color of the grid cell (RGBA).
    """

    def __init__(self, rect: pygame.Rect, screen: pygame.Surface):
        """Initialize the RoadCellView.

        Args:
            rect (pygame.Rect): The bounding rectangle for this cell on screen.
            screen (pygame.Surface): The Pygame surface to render onto.
        """
        self.rect = rect
        self.screen = screen
        self._road_view = None
        self._current_cell = None
        self.font = pygame.font.Font(None, 20)

        self.GRID_SIZE = 1
        self.ALPHA = 128
        self.BG_COLOR = (210, 210, 210, self.ALPHA)
        self.BORDER_COLOR = (170, 170, 170, self.ALPHA)

    def draw(self, cell_model: RoadCellModel):
        """Render the road cell and its background grid.

        Draws a semi-transparent grid background, then renders the road using
        an internal :class:`RoadView`. Special cell types (start, end, obstacle)
        are annotated with colored borders and optional text labels.

        Args:
            cell_model (RoadCellModel or None): The road cell model to render.
                If ``None``, only the background grid is drawn.
        """
        grid_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        cell_width = self.rect.width // self.GRID_SIZE
        cell_height = self.rect.height // self.GRID_SIZE

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = col * cell_width
                y = row * cell_height
                small_rect = pygame.Rect(x, y, cell_width - 1, cell_height - 1)
                pygame.draw.rect(grid_surface, self.BG_COLOR, small_rect)
                pygame.draw.rect(grid_surface, self.BORDER_COLOR, small_rect, 1)

        self.screen.blit(grid_surface, self.rect.topleft)

        if cell_model is None:
            self._current_cell = None
            return

        if self._road_view is None or self._current_cell != cell_model:
            self._road_view = RoadView(cell_model.road_model, self.screen, self.rect)
            self._current_cell = cell_model

        self._road_view.set_position(self.rect)
        self._road_view.draw()

        from models.Road import RoadType
        cell_type = cell_model.get_type()
        if cell_type == RoadType.START_ROAD:
            pygame.draw.rect(self.screen, (0, 180, 0), self.rect, 3)
            label = self.font.render("S", True, (0, 100, 0))
            self.screen.blit(label, (self.rect.x + 5, self.rect.y + 5))
        elif cell_type == RoadType.END_ROAD:
            pygame.draw.rect(self.screen, (180, 0, 0), self.rect, 3)
            label = self.font.render("E", True, (180, 0, 0))
            self.screen.blit(label, (self.rect.x + 5, self.rect.y + 5))
        elif cell_type == RoadType.OBSTACLE_ROAD:
            pygame.draw.rect(self.screen, (100, 100, 100), self.rect, 3)

    def trigger_rotate_animation(self, duration: int = 500):
        """Trigger a rotation animation on the contained road view.

        Delegates the animation request to the internal :class:`RoadView`.

        Args:
            duration (int): Animation duration in milliseconds. Defaults to 500.
        """
        if self._road_view is not None:
            self._road_view.rotated(duration)