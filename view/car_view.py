"""Car visualization component for tower defense game.
Handles car rendering, path movement, rotation, and screen position updates.
"""
import pygame
import math
from typing import List, Tuple, Optional

class CarView:
    """Visual and movement controller for enemy cars on the game map.
    Manages path following, smooth movement, rotation, and rendering.
    """
    def __init__(self, cell_size: int, map_offset: Tuple[int, int],
                 start_grid: Optional[Tuple[int, int]] = None):
        """Initialize car with map settings and visual assets.

        Args:
            cell_size: Pixel size of one grid cell on the map
            map_offset: (x, y) screen offset for map drawing position
            start_grid: Initial (row, column) grid position to spawn the car
        """

        self.cell_size = cell_size
        self.map_offset = map_offset
        self.path: List[Tuple[int, int]] = []
        self.current_index = 0
        self.position = (0.0, 0.0)
        self.speed = 2.0
        self.finished = False
        self.moving = False
        self.car_img = self._create_car_surface()

        if start_grid:
            self.position = self._grid_to_screen(start_grid)
        else:
            self.position = (0, 0)

    def _create_car_surface(self):
        """Create and return a custom car surface with wheels and border.

        Returns:
            pygame.Surface: Pre-designed car graphic
        """
        surf = pygame.Surface((26, 16), pygame.SRCALPHA)
        surf.fill((255, 80, 80))
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
        for ox, oy in [(6,4), (20,4), (6,12), (20,12)]:
            pygame.draw.circle(surf, (0,0,0), (ox, oy), 3)
        return surf

    def _grid_to_screen(self, rc: Tuple[int, int]) -> Tuple[float, float]:
        """Convert grid (row, column) coordinates to screen pixel coordinates.

        Args:
            rc: (row, column) grid position

        Returns:
            (x, y) pixel coordinates on the screen
        """
        row, col = rc
        x = self.map_offset[0] + col * self.cell_size + self.cell_size / 2
        y = self.map_offset[1] + row * self.cell_size + self.cell_size / 2
        return x, y

    def start_move(self, path: List[Tuple[int, int]]):
        """Start moving the car along a given grid path.

        Args:
            path: List of (row, column) grid points to follow
        """
        if not path:
            return
        self.path = path
        self.current_index = 0
        self.position = self._grid_to_screen(path[0])
        self.moving = True
        self.finished = False

    def update(self):
        """Update car position each frame for smooth path movement.
        Handles step-by-step navigation to next target point on the path.
        """
        if not self.moving or self.finished:
            return
        if self.current_index >= len(self.path) - 1:
            self.finished = True
            self.moving = False
            return
        target = self._grid_to_screen(self.path[self.current_index + 1])
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.position = target
            self.current_index += 1
        else:
            self.position = (self.position[0] + self.speed * dx / dist,
                             self.position[1] + self.speed * dy / dist)

    def draw(self, screen: pygame.Surface):
        """Render the car on the screen with direction-based rotation.

        Args:
            screen: Pygame surface to draw the car on
        """
        angle = 0
        if self.moving and self.current_index < len(self.path) - 1:
            next_pos = self._grid_to_screen(self.path[self.current_index + 1])
            dx = next_pos[0] - self.position[0]
            dy = next_pos[1] - self.position[1]
            if dx != 0 or dy != 0:
                angle = -math.degrees(math.atan2(dy, dx))
        rotated = pygame.transform.rotate(self.car_img, angle)
        rect = rotated.get_rect(center=self.position)
        screen.blit(rotated, rect)

    def move_one_step(self, next_grid: Tuple[int, int]):
        """Instantly move the car to a specific grid position.

        Args:
            next_grid: Target (row, column) grid position to jump to
        """
        self.position = self._grid_to_screen(next_grid)
        self.current_index = self.path.index(next_grid) if next_grid in self.path else 0