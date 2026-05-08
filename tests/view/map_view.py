import pygame
from typing import Tuple, List, Optional
from models.map import MapModel
from view.road_cell_view import RoadCellView

class MapView:
    def __init__(self, map_model: MapModel, x: int, y: int, cell_size: int, screen: pygame.Surface):
        self.map_model = map_model
        
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.screen = screen
        self.cell_views: List[List[RoadCellView]] = []
        for r in range(map_model.rows):
            row_views = []
            for c in range(map_model.cols):
                rect = pygame.Rect(x + c*cell_size, y + r*cell_size, cell_size, cell_size)
                row_views.append(RoadCellView(rect, screen))
            self.cell_views.append(row_views)

    def draw(self):
        for r in range(self.map_model.rows):
            for c in range(self.map_model.cols):
                cell = self.map_model.get_cell(r, c)
                self.cell_views[r][c].draw(cell)

    def check_click(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        for r in range(self.map_model.rows):
            for c in range(self.map_model.cols):
                rect = pygame.Rect(self.x + c*self.cell_size, self.y + r*self.cell_size, self.cell_size, self.cell_size)
                if rect.collidepoint(mouse_pos):
                    return (r, c)
        return None