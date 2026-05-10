import pygame
from typing import Tuple, List, Optional
from models.map import MapModel
from view.road_cell_view import RoadCellView

class MapView:
    """
    Visual representation and rendering logic for the game map grid.
    Handles cell rendering, mouse interaction detection, and layout positioning.
    
    Acts as the view component that displays the MapModel data on the screen.
    """
    def __init__(self, map_model: MapModel, x: int, y: int, cell_size: int, screen: pygame.Surface):
        """
        Initialize the map view with position, size, and associated data model.
        
        Args:
            map_model: The data model containing grid state and logic
            x: X coordinate of the top-left corner of the map on the screen
            y: Y coordinate of the top-left corner of the map on the screen
            cell_size: Pixel size of each individual grid cell
            screen: Pygame surface for rendering the map
        """
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
        """
        Render the entire map and all cells to the screen.
        Iterates through each cell and delegates drawing to the corresponding RoadCellView.
        """
        for r in range(self.map_model.rows):
            for c in range(self.map_model.cols):
                cell = self.map_model.get_cell(r, c)
                self.cell_views[r][c].draw(cell)

    def check_click(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Detect which cell was clicked by the user.
        
        Args:
            mouse_pos: Tuple containing (x, y) coordinates of the mouse click
            
        Returns:
            Tuple (row, column) of the clicked cell if a cell was hit,
            None if the click is outside the map area
        """
        for r in range(self.map_model.rows):
            for c in range(self.map_model.cols):
                rect = pygame.Rect(self.x + c*self.cell_size, self.y + r*self.cell_size, self.cell_size, self.cell_size)
                if rect.collidepoint(mouse_pos):
                    return (r, c)
        return None