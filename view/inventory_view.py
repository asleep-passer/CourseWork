import pygame
from models.Road import RoadType
from models.roadlist import RoadListModel
import os

class InventoryView:
    def __init__(self, x, y, screen):
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
        self.buttons.clear()
        spacing = 90
        for i, rt in enumerate(self.display_types):
            rect = pygame.Rect(self.x, self.y + i * spacing, 80, 80)
            count = road_list.get_road_num(rt)
            self.buttons.append((rect, rt, count))

    def draw(self):
        for rect, rt, count in self.buttons:
            # 背景色
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
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                self.selected_type = rt
                return rt
        return None

    def get_road_type_at(self, pos):
        for rect, rt, count in self.buttons:
            if rect.collidepoint(pos) and count != 0:
                return rt
        return None