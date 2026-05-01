import pygame
from typing import List, Tuple

class CarView:
    def __init__(self, path: List[Tuple[int, int]], cell_size: int, map_offset: Tuple[int, int]):
        """
        path: 格子坐标序列 (row, col)
        cell_size: 每个格子的像素大小
        map_offset: 地图左上角在屏幕上的 (x, y)
        """
        self.path = path
        self.cell_size = cell_size
        self.map_offset = map_offset
        self.current_index = 0
        self.position = self._grid_to_screen(path[0])
        self.speed = 2.0          # 每帧移动像素
        self.finished = False
        self.car_img = self._create_car_surface()

    def _create_car_surface(self):
        """创建一个简单的小车表面"""
        surf = pygame.Surface((30, 20), pygame.SRCALPHA)
        surf.fill((255, 100, 100))   # 红色小车
        pygame.draw.rect(surf, (0,0,0), surf.get_rect(), 2)
        # 加上轮子（四个小圆）
        pygame.draw.circle(surf, (0,0,0), (8, 5), 4)
        pygame.draw.circle(surf, (0,0,0), (22, 5), 4)
        pygame.draw.circle(surf, (0,0,0), (8, 15), 4)
        pygame.draw.circle(surf, (0,0,0), (22, 15), 4)
        return surf

    def _grid_to_screen(self, rc: Tuple[int, int]) -> Tuple[float, float]:
        row, col = rc
        x = self.map_offset[0] + col * self.cell_size + self.cell_size/2
        y = self.map_offset[1] + row * self.cell_size + self.cell_size/2
        return x, y

    def update(self):
        if self.finished or self.current_index >= len(self.path) - 1:
            self.finished = True
            return
        # 当前目标点（下一个格子中心）
        target = self._grid_to_screen(self.path[self.current_index + 1])
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dist = (dx**2 + dy**2) ** 0.5
        if dist < self.speed:
            self.position = target
            self.current_index += 1
            if self.current_index >= len(self.path) - 1:
                self.finished = True
        else:
            self.position = (self.position[0] + self.speed * dx / dist,
                             self.position[1] + self.speed * dy / dist)

    def draw(self, screen: pygame.Surface):
        """绘制小车（根据移动方向旋转）"""
        angle = 0
        if not self.finished and self.current_index < len(self.path) - 1:
            # 简单计算朝向
            next_pos = self._grid_to_screen(self.path[self.current_index + 1])
            dx = next_pos[0] - self.position[0]
            dy = next_pos[1] - self.position[1]
            if dx != 0 or dy != 0:
                import math
                angle = -math.degrees(math.atan2(dy, dx))
        rotated = pygame.transform.rotate(self.car_img, angle)
        rect = rotated.get_rect(center=self.position)
        screen.blit(rotated, rect)