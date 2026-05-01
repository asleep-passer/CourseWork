import pygame
from models.roadcell import RoadCellModel
from view.road import RoadView

class RoadCellView:
    def __init__(self, rect: pygame.Rect, screen: pygame.Surface):
        self.rect = rect
        self.screen = screen
        self._road_view = None
        self._current_cell = None

    def draw(self, cell_model):
        # 清空旧 RoadView 如果 model 变了
        if cell_model is None:
            if self._road_view is not None:
                self._road_view = None
            pygame.draw.rect(self.screen, (210, 210, 210), self.rect)
            pygame.draw.rect(self.screen, (170, 170, 170), self.rect, 1)
            self._current_cell = None
            return

        if self._road_view is None or self._current_cell != cell_model:
            # 创建新的 RoadView，位置用 self.rect
            self._road_view = RoadView(cell_model, self.screen, self.rect)
            self._current_cell = cell_model

        # 更新位置（如果 rect 发生变化）
        self._road_view.set_position(self.rect)
        self._road_view.draw()

        # 锁定标记红框
        from models.Road import RoadType
        if cell_model.get_type() in (RoadType.START_ROAD, RoadType.END_ROAD, RoadType.OBSTACLE_ROAD):
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 3)

    def trigger_rotate_animation(self, duration=500):
        """播放旋转动画（如果该格有路）"""
        if self._road_view is not None:
            self._road_view.rotated(duration)