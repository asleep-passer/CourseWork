import pygame
from models.roadcell import RoadCellModel
from view.road import RoadView

class RoadCellView:
    def __init__(self, rect: pygame.Rect, screen: pygame.Surface):
        self.rect = rect
        self.screen = screen
        self._road_view = None
        self._current_cell = None
        self.font = pygame.font.Font(None, 20)

    def draw(self, cell_model):
        if cell_model is None:
            pygame.draw.rect(self.screen, (210, 210, 210), self.rect)
            pygame.draw.rect(self.screen, (170, 170, 170), self.rect, 1)
            self._current_cell = None
            return

        if self._road_view is None or self._current_cell != cell_model:
            self._road_view = RoadView(cell_model, self.screen, self.rect)
            self._current_cell = cell_model

        self._road_view.set_position(self.rect)
        self._road_view.draw()

        from models.Road import RoadType
        cell_type = cell_model.get_type()
        if cell_type == RoadType.START_ROAD:
            pygame.draw.rect(self.screen, (0, 180, 0), self.rect, 3)
            label = self.font.render("S", True, (0, 100, 0))
            self.screen.blit(label, (self.rect.x+5, self.rect.y+5))
        elif cell_type == RoadType.END_ROAD:
            pygame.draw.rect(self.screen, (180, 0, 0), self.rect, 3)
            label = self.font.render("E", True, (180, 0, 0))
            self.screen.blit(label, (self.rect.x+5, self.rect.y+5))
        elif cell_type == RoadType.OBSTACLE_ROAD:
            pygame.draw.rect(self.screen, (100, 100, 100), self.rect, 3)

    def trigger_rotate_animation(self, duration=500):
        if self._road_view is not None:
            self._road_view.rotated(duration)