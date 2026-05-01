import pygame as pg
from models import RoadType as rt
from models import RoadModel as rm
import os

class RoadView:
    def __init__(self, road: rm, screen: pg.surface.Surface, pos: pg.Rect) -> None:
        # 兼容传入 RoadCellModel 的情况
        from models.roadcell import RoadCellModel
        if isinstance(road, RoadCellModel):
            road = road.road_model

        self.road = road
        self.__screen = screen
        self.__pos = pos.copy()

        # 旋转相关状态
        self.__is_rotating = False
        self.__rotation_start_angle = 0
        self.__rotation_current_angle = 0
        self.__rotation_target_angle = 0
        self.__rotation_duration = 0
        self.__rotation_start_time = 0
        self.__rotation_center = pos.center

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 加载原图
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if road.road_type == rt.OBSTACLE_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/terrainTile3.png"))
        elif road.road_type == rt.STRAIGHT_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile27.png"))
        elif road.road_type == rt.BEND_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile7.png"))
        elif road.road_type == rt.T_SHAPED_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile9.png"))
        elif road.road_type == rt.CROSS_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile5.png"))
        elif road.road_type == rt.START_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile27.png"))  # 直道
        elif road.road_type == rt.END_ROAD:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile27.png"))  # 直道
        else:
            img = pg.image.load(os.path.join(base_path, "view/assets/Legacy/PNG/roadTile18.png"))

        img = img.convert_alpha()
        # 转换格式，保证 smoothscale 可用
        img = img.convert_alpha()

        # 根据格子大小缩放图片
        cell_size = min(pos.width, pos.height)
        target_size = int(cell_size * 1.0)
        self.__original_img = pg.transform.smoothscale(img, (target_size, target_size))

        # 生成当前显示的图像（初始无旋转）
        self.__img = self.__original_img.copy()
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def set_position(self, pos: pg.Rect):
        self.__pos = pos.copy()
        self.__rotation_center = pos.center
        # 如果已加载图像，重新调整位置
        if hasattr(self, '_RoadView__img') and self.__img is not None:
            self.__pos = self.__img.get_rect(center=self.__rotation_center)

    # ========== 以下部分不变 ==========
    def __normalize_angle(self, angle: float):
        return angle % 360

    def rotated(self, duration: int = 500):
        self.road.rotate()
        if self.__is_rotating:
            return
        self.__is_rotating = True
        self.__rotation_start_angle = self.__rotation_current_angle
        self.__rotation_duration = duration
        self.__rotation_start_time = pg.time.get_ticks()
        self.__rotation_target_angle = self.__normalize_angle(self.__rotation_start_angle + 90)

    def update(self):
        if not self.__is_rotating:
            return
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.__rotation_start_time
        if elapsed_time >= self.__rotation_duration:
            self.__rotation_current_angle = self.__rotation_target_angle
            self.__is_rotating = False
        else:
            progress = elapsed_time / self.__rotation_duration
            start_angle = self.__rotation_start_angle
            target_angle = self.__rotation_target_angle
            if start_angle == 270 and target_angle == 0:
                self.__rotation_current_angle = start_angle + 90 * progress
            else:
                angle_diff = target_angle - start_angle
                self.__rotation_current_angle = start_angle + angle_diff * progress
        self.__rotation_current_angle = self.__normalize_angle(self.__rotation_current_angle)
        self.__update_rotated_image()

    def __update_rotated_image(self):
        self.__img = pg.transform.rotate(self.__original_img, -self.__rotation_current_angle)
        self.__pos = self.__img.get_rect(center=self.__rotation_center)

    def draw(self):
        if self.__is_rotating:
            self.update()
        self.__screen.blit(self.__img, self.__pos)