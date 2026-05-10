"""
roadview.py - Pygame-based visual representation of road tiles in a grid-based road editor or simulation.

This module defines the RoadView class, which is responsible for rendering individual road tiles
with appropriate textures and handling smooth 90-degree rotation animations. It synchronizes its
visual state with an underlying RoadModel instance and supports various road types such as straight,
bend, T-junction, crossroad, start/end points, and obstacles.

The view uses preloaded PNG assets from a fixed asset directory and scales them to fit within a given
cell rectangle. Rotation is animated over time using linear interpolation of the angle, and all drawing
is performed via Pygame's blit operations.
"""

import pygame as pg
from models import RoadType as rt
from models import RoadModel as rm
import os


class RoadView:
    """A view class responsible for rendering a road model in Pygame.

    This class loads the appropriate texture based on the road type and handles
    smooth 90-degree rotation animations synchronized with the underlying model.
    Supported road types include obstacles, straight roads, bends, T-junctions,
    crossroads, start tiles, and end tiles.

    Attributes:
        road (rm): The associated road model instance.
        __screen (pg.Surface): The Pygame surface to draw on.
        __pos (pg.Rect): The current position and size rectangle of the image.
        __is_rotating (bool): Flag indicating whether a rotation animation is in progress.
        __rotation_start_angle (float): Starting angle of the current rotation (in degrees).
        __rotation_current_angle (float): Current visual rotation angle (in degrees).
        __rotation_target_angle (float): Target angle for the ongoing rotation (in degrees).
        __rotation_duration (int): Duration of the rotation animation in milliseconds.
        __rotation_start_time (int): Timestamp (in ms) when the rotation started.
        __rotation_center (tuple[int, int]): Center point around which rotation occurs.
        __original_img (pg.Surface): The original unrotated image loaded from disk.
        __img (pg.Surface): The currently displayed (possibly rotated) image.
    """

    def __init__(self, road: rm, screen: pg.surface.Surface, pos: pg.Rect) -> None:
        """Initialize a RoadView instance.

        Loads the appropriate image asset based on the road type and sets the initial
        visual rotation angle according to the model's current rotation state.

        Args:
            road (rm): The road model to render. May also be a RoadCellModel,
                in which case its associated RoadModel will be used.
            screen (pg.Surface): The Pygame surface onto which to draw.
            pos (pg.Rect): The initial position and size rectangle for the image.
        """
        from models.roadcell import RoadCellModel
        if isinstance(road, RoadCellModel):
            road = road.road_model

        self.road = road
        self.__screen = screen
        self.__pos = pos.copy()

        self.__is_rotating = False
        self.__rotation_start_angle = 0
        self.__rotation_current_angle = 0
        self.__rotation_target_angle = 0
        self.__rotation_duration = 0
        self.__rotation_start_time = 0
        self.__rotation_center = pos.center

        # Determine base path relative to this file to locate assets reliably
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        asset_path = os.path.join(base_path, "view/assets/Legacy/PNG")

        # Load appropriate texture based on road type
        road_type = road.road_type
        if road_type == rt.OBSTACLE_ROAD:
            img_path = os.path.join(asset_path, "terrainTile3.png")
        elif road_type == rt.STRAIGHT_ROAD:
            img_path = os.path.join(asset_path, "roadTile27.png")
        elif road_type == rt.BEND_ROAD:
            img_path = os.path.join(asset_path, "roadTile7.png")
        elif road_type == rt.T_SHAPED_ROAD:
            img_path = os.path.join(asset_path, "roadTile9.png")
        elif road_type == rt.CROSS_ROAD:
            img_path = os.path.join(asset_path, "roadTile5.png")
        elif road_type in (rt.START_ROAD, rt.END_ROAD):
            img_path = os.path.join(asset_path, "roadTile18.png")
        else:
            # Fallback for unknown road types
            img_path = os.path.join(asset_path, "roadTile18.png")

        img = pg.image.load(img_path).convert_alpha()

        # Scale image to fit within the cell while preserving aspect ratio
        cell_size = min(pos.width, pos.height)
        target_size = int(cell_size * 1.0)  # No scaling factor; use full cell size
        self.__original_img = pg.transform.smoothscale(img, (target_size, target_size))

        # Initialize displayed image and position centered in the given rect
        self.__img = self.__original_img.copy()
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

        # Synchronize initial visual rotation with model's rotation count (each rotation = 90°)
        if self.road._rotated != 0:
            self.__rotation_current_angle = self.__normalize_angle(90 * self.road._rotated)
            self.__update_rotated_image()

    def set_position(self, pos: pg.Rect):
        """Update the screen position of the road view.

        Args:
            pos (pg.Rect): The new position and size rectangle.
        """
        self.__pos = pos.copy()
        self.__rotation_center = pos.center
        if hasattr(self, '_RoadView__img') and self.__img is not None:
            self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def __normalize_angle(self, angle: float) -> float:
        """Normalize an angle to the range [0, 360) degrees.

        Args:
            angle (float): Input angle in degrees (can be any real number).

        Returns:
            float: Normalized angle in degrees within [0, 360).
        """
        return angle % 360

    def rotated(self, duration: int = 500):
        """Trigger a 90-degree clockwise rotation animation and update the model.

        If a rotation is already in progress, this call is ignored to prevent overlapping animations.

        Args:
            duration (int): Duration of the rotation animation in milliseconds.
                Defaults to 500 ms.
        """
        self.road.rotate()  # Update the underlying model's rotation state
        if self.__is_rotating:
            return  # Ignore if already rotating

        self.__is_rotating = True
        self.__rotation_start_angle = self.__rotation_current_angle
        self.__rotation_duration = duration
        self.__rotation_start_time = pg.time.get_ticks()
        self.__rotation_target_angle = self.__normalize_angle(self.__rotation_start_angle + 90)

    def update(self):
        """Update the state of the rotation animation.

        Computes the current rotation angle based on elapsed time and updates
        the displayed image accordingly. Stops the animation when complete.

        Handles the special case where rotation wraps from 270° to 0° by treating it
        as a continuous +90° motion instead of a -270° jump, ensuring smooth visual transition.
        """
        if not self.__is_rotating:
            return

        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.__rotation_start_time

        if elapsed_time >= self.__rotation_duration:
            # Animation finished: snap to target angle
            self.__rotation_current_angle = self.__rotation_target_angle
            self.__is_rotating = False
        else:
            # Interpolate rotation angle linearly over time
            progress = elapsed_time / self.__rotation_duration
            start_angle = self.__rotation_start_angle
            target_angle = self.__rotation_target_angle

            # Special handling for 270° → 0° wrap-around to avoid backward spin
            if start_angle == 270 and target_angle == 0:
                self.__rotation_current_angle = start_angle + 90 * progress
            else:
                angle_diff = target_angle - start_angle
                self.__rotation_current_angle = start_angle + angle_diff * progress

        # Ensure angle stays normalized after interpolation
        self.__rotation_current_angle = self.__normalize_angle(self.__rotation_current_angle)
        self.__update_rotated_image()

    def __update_rotated_image(self):
        """Regenerate the rotated image and re-center it.

        Pygame's transform.rotate() rotates counter-clockwise, so we negate the angle
        to achieve clockwise visual rotation consistent with model logic.
        """
        self.__img = pg.transform.rotate(self.__original_img, -self.__rotation_current_angle)
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def draw(self):
        """Draw the current road image onto the screen.

        If a rotation animation is active, it updates the state before drawing.
        This ensures the visual always reflects the latest interpolated frame.
        """
        if self.__is_rotating:
            self.update()
        self.__screen.blit(self.__img, self.__pos)