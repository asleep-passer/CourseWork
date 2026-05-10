"""Inventory UI component that displays available road pieces and allows selection.
Shows road icons, remaining counts, and handles user click selection.
"""
import pygame
from models.Road import RoadType
from models.roadlist import RoadListModel
import os

class InventoryView:
    """UI panel for displaying and selecting available road types in the level editor.
    Supports visual previews, count display, and click selection.
    """
    def __init__(self, x, y, screen):
        """Initialize the inventory panel at a fixed screen position.

        Args:
            x: X coordinate of the panel's top-left corner
            y: Y coordinate of the panel's top-left corner
            screen: Pygame surface to draw on
        """
        self.x = x
        self.y = y
        self.screen = screen
        self.buttons = []
        self.selected_type = None
        self.font = pygame.font.Font(None, 18)
        self.display_types = [RoadType.STRAIGHT_ROAD, RoadType.BEND_ROAD,
                              RoadType.T_SHAPED_ROAD, RoadType.CROSS_ROAD]
        self.previews = {}
        self._load_previews()

    def _load_previews(self):
        """Load and scale road icon images from assets for visual preview display."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_map = {
            RoadType.STRAIGHT_ROAD: "roadTile27.png",
            RoadType.BEND_ROAD: "roadTile7.png",
            RoadType.T_SHAPED_ROAD: "roadTile9.png",
            RoadType.CROSS_ROAD: "roadTile5.png",
        }
        size = 50
        for rt, fname in img_map.items():
            try:
                img = pygame.image.load(os.path.join(base_path, "view/assets/Legacy/PNG", fname)).convert_alpha()
                self.previews[rt] = pygame.transform.smoothscale(img, (size, size))
            except:
                self.previews[rt] = None

    def update_from_model(self, road_list):
        """Refresh inventory display with current road counts from the data model.

        Args:
            road_list: Model containing available road counts
        """
        self.buttons.clear()
        spacing = 90
        for i, rt in enumerate(self.display_types):
            rect = pygame.Rect(self.x, self.y + i * spacing, 80, 80)
            count = road_list.get_road_num(rt)
            self.buttons.append((rect, rt, count))

    def draw(self):
        """Render inventory items, backgrounds, preview icons, and remaining counts."""
        for rect, rt, count in self.buttons:
        
            if count == 0:
                color = (180, 180, 180)
            elif rt == self.selected_type:
                color = (100, 200, 100)
            else:
                color = (240, 240, 240)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

            if rt in self.previews and self.previews[rt] is not None:
                preview = self.previews[rt]
                preview_rect = preview.get_rect(center=rect.center)
                self.screen.blit(preview, preview_rect)
            else:
                text = self.font.render(rt.name.replace("_ROAD",""), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

            count_text = self.font.render(str(count), True, (255, 255, 255), (0, 0, 0))
            self.screen.blit(count_text, (rect.right - 25, rect.top + 2))

    def handle_click(self, pos):
        """Process mouse click to select a road type.

        Args:
            pos: Mouse (x, y) coordinates

        Returns:
            Selected RoadType or None if no valid click
        """
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                self.selected_type = rt
                return rt
        return None

    def get_road_type_at(self, pos):
        """Check which road type is under the mouse position (for drag operations).

        Args:
            pos: Mouse (x, y) coordinates

        Returns:
            RoadType if found and available, None otherwise
        """
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                return rt
        return None