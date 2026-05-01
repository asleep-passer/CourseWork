import pygame
from models.Road import RoadType, RoadModel
from models.roadlist import RoadListModel

class InventoryView:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.buttons = []          # (rect, RoadType, count)
        self.selected_type = None
        self.font = pygame.font.Font(None, 18)
        self.display_types = [RoadType.STRAIGHT_ROAD, RoadType.BEND_ROAD,
                              RoadType.T_SHAPED_ROAD, RoadType.CROSS_ROAD]

    def update_from_model(self, road_list):
        self.buttons.clear()
        for i, rt in enumerate(self.display_types):
            rect = pygame.Rect(self.x + i*90, self.y, 80, 80)
            count = road_list.get_road_num(rt)
            self.buttons.append((rect, rt, count))

    def draw(self):
        for rect, rt, count in self.buttons:
            color = (180,180,180) if count == 0 else (240,240,240)
            if rt == self.selected_type:
                color = (100,200,100)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0,0,0), rect, 2)
            text = self.font.render(rt.name.replace("_ROAD",""), True, (0,0,0))
            self.screen.blit(text, (rect.x+5, rect.y+5))
            count_text = self.font.render(str(count), True, (0,0,0))
            self.screen.blit(count_text, (rect.x+5, rect.y+25))

    def handle_click(self, pos):
        """左键点击选中道具类型"""
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                self.selected_type = rt
                return rt
        return None

    def get_road_type_at(self, pos):
        """返回鼠标位置下的道具类型，如果有货；用于拖拽开始"""
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                return rt
        return None