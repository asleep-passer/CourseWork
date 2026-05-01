import pygame as pg
from models import RoadType as rt
from models import RoadModel as rm
import os


class RoadView:
    """
    Used for rendering roads and providing simple animation effects.

    Attributes:
        road (RoadModel): Stores the input road object.
        __screen (pygame.surface.Surface): Private attribute storing the pygame surface for rendering.
        __pos (pygame.Rect): Private attribute storing the position rectangle (copied to prevent external modification).
        __is_rotating (bool): Flag indicating whether the road is currently undergoing rotation animation.
        __rotation_start_angle (float): Starting angle when a rotation animation begins.
        __rotation_current_angle (float): Current rotation angle during an active rotation animation.
        __rotation_target_angle (float): Target angle to reach at the end of a rotation animation.
        __rotation_duration (int): Total duration of the rotation animation in milliseconds.
        __rotation_start_time (int): Timestamp when the rotation animation started.
        __rotation_center (pygame.Rect): Center point around which rotation occurs, based on initial position.
        __original_img (pygame.surface.Surface): The original loaded image corresponding to the road type, unmodified.
        __img (pygame.surface.Surface): A copy of the original image that can be transformed (rotated) without affecting the original.
    """

    def __init__(self, road: rm, screen: pg.surface.Surface, pos: pg.Rect) -> None:
        """
        Initializes the RoadRenderer object for rendering roads and providing simple animation effects.

        Args:
        road (RoadModel): The road object containing road type information used to determine which image to load.
        screen (pygame.surface.Surface): The pygame surface where the road will be rendered.
        pos (pygame.Rect): The initial position rectangle defining where the road should be placed on screen.
        """
        # ====================== 【只加这 4 行，其他完全不动！】 ======================
        from models.roadcell import RoadCellModel
        if isinstance(road, RoadCellModel):
            road = road.road_model
        # ==========================================================================

        self.road = road
        self.__screen = screen
        self.__pos = pos.copy()

        # Rotational related states
        self.__is_rotating = False
        self.__rotation_start_angle = 0
        self.__rotation_current_angle = 0
        self.__rotation_target_angle = 0
        self.__rotation_duration = 0
        self.__rotation_start_time = 0
        self.__rotation_center = pos.center

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if road.road_type == rt.OBSTACLE_ROAD:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/terrainTile3.png"))
        elif road.road_type == rt.STRAIGHT_ROAD:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile27.png"))
        elif road.road_type == rt.BEND_ROAD:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile7.png"))
        elif road.road_type == rt.T_SHAPED_ROAD:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile9.png"))
        elif road.road_type == rt.CROSS_ROAD:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile5.png"))
        else:
            self.__original_img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile18.png"))

        self.__img = self.__original_img.copy()
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def set_position(self, pos: pg.Rect):
        """
        Set the positon of the road picture.
        """
        self.__pos = pos.copy()
        self.__rotation_center = pos.center
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def __normalize_angle(self, angle: float):
        """
        Normalize the angle to the range of 0 to 360 degrees.

        Args:
            angle (float): An angle with degree.

        Returns:
            float: An angle belongs to [0,360)
        """
        return angle % 360

    def rotated(self, duration: int = 500):
        """
        Start the 90-degree rotation animation

        Args:
            duration (int): Duration, measured in milliseconds.
        """
        self.road.rotate()
        if self.__is_rotating:
            return

        self.__is_rotating = True
        self.__rotation_start_angle = self.__rotation_current_angle
        self.__rotation_duration = duration
        self.__rotation_start_time = pg.time.get_ticks()

        self.__rotation_target_angle = self.__normalize_angle(self.__rotation_start_angle + 90)

    def update(self):
        """
        Update the rotation status
        """
        if not self.__is_rotating:
            return

        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.__rotation_start_time

        if elapsed_time >= self.__rotation_duration:
            self.__rotation_current_angle = self.__rotation_target_angle
            self.__is_rotating = False
        else:
            # Calculate the rotation progress
            progress = elapsed_time / self.__rotation_duration

            start_angle = self.__rotation_start_angle
            target_angle = self.__rotation_target_angle

            if start_angle == 270 and target_angle == 0:
                # A clockwise rotation from 270 to 360
                self.__rotation_current_angle = start_angle + 90 * progress
            else:
                # Linear interpolation
                angle_diff = target_angle - start_angle
                self.__rotation_current_angle = start_angle + angle_diff * progress

        self.__rotation_current_angle = self.__normalize_angle(self.__rotation_current_angle)
        self.__update_rotated_image()

    def __update_rotated_image(self):
        """
        Update the image and position based on the current angle
        """
        self.__img = pg.transform.rotate(self.__original_img, -self.__rotation_current_angle)

        # Re-calculate the position while keeping the rotation center unchanged
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def draw(self):
        """
        Draw the road
        """
        if self.__is_rotating:
            self.update()
        self.__screen.blit(self.__img, self.__pos)