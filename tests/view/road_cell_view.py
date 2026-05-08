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

        self.GRID_SIZE = 1
        self.ALPHA = 128
        self.BG_COLOR = (210, 210, 210, self.ALPHA)
        self.BORDER_COLOR = (170, 170, 170, self.ALPHA)

    def draw(self, cell_model: RoadCellModel):
        # 绘制半透明网格背景
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

        # 如果道路视图不存在或模型已变，重新创建
        if self._road_view is None or self._current_cell != cell_model:
            # 注意：这里直接使用 cell_model.road_model，它已经包含了正确的旋转状态
            self._road_view = RoadView(cell_model.road_model, self.screen, self.rect)
            self._current_cell = cell_model
            # 不再需要手动旋转，因为 RoadView 内部会根据 road._rotated 自动处理图像

        self._road_view.set_position(self.rect)
        self._road_view.draw()

        # 绘制起点、终点、障碍物标识
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

    def trigger_rotate_animation(self, duration=500):
        if self._road_view is not None:
            self._road_view.rotated(duration)   # 只传 duration