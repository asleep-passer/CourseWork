from models.roadlist import RoadListModel as rl
from models.roadlist import AdminRoadListModel
from models import RoadModel
from view.road import RoadView as rv
import pygame as pg

class RoadListView:
    def __init__(self, road_list: rl, screen: pg.surface.Surface) -> None:
        self.__road_list = road_list
        self.__screen = screen
        self.__background = pg.image.load("view/assets/PNG/Grey/Default/button_square_flat.png")
        self.__road_view_list = []  # 保存RoadView实例
        self.__positions = []       # 保存位置信息
        self.__road_types = []      # 保存道路类型

        if isinstance(road_list, AdminRoadListModel):
            new_size = (screen.get_rect().width * 0.8, screen.get_rect().height * 0.2)
            self.__background = pg.transform.scale(self.__background, new_size)
            self.__pos = pg.Rect(0, screen.get_rect().height * 0.8, new_size[0], new_size[1])
            self.__block_size = (new_size[0] / 7, new_size[1])
            
            # Admin模式：7种道路类型
            from models.Road import RoadType
            self.__road_types = [
                RoadType.OBSTACLE_ROAD,
                RoadType.STRAIGHT_ROAD,
                RoadType.BEND_ROAD,
                RoadType.T_SHAPED_ROAD,
                RoadType.CROSS_ROAD,
                RoadType.START_ROAD,
                RoadType.END_ROAD
            ]

        else:
            new_size = (screen.get_rect().width * 0.2, screen.get_rect().height)
            self.__background = pg.transform.scale(self.__background, new_size)
            self.__pos = pg.Rect(screen.get_rect().width * 0.8, 0, new_size[0], new_size[1])
            self.__block_size = (new_size[0], new_size[1] / 4)
            
            # 普通模式：4种道路类型
            from models.Road import RoadType
            self.__road_types = [
                RoadType.STRAIGHT_ROAD,
                RoadType.BEND_ROAD,
                RoadType.T_SHAPED_ROAD,
                RoadType.CROSS_ROAD
            ]

        # 创建并保存RoadView实例
        for i, road_type in enumerate(self.__road_types):
            if isinstance(road_list, AdminRoadListModel):
                # Admin模式：水平排列
                block_x = self.__pos.x + i * self.__block_size[0]
                block_y = self.__pos.y
            else:
                # 普通模式：垂直排列
                block_x = self.__pos.x
                block_y = self.__pos.y + i * self.__block_size[1]
            
            # 创建用于显示道路图标的位置
            temp_rect = pg.Rect(block_x + 10, block_y + 10, 
                               self.__block_size[0] - 20, 
                               self.__block_size[1] / 2 - 20)
            
            # 创建临时道路对象用于显示
            temp_road = RoadModel(road_type)
            
            # 创建并保存道路视图
            road_view = rv(temp_road, self.__screen, temp_rect)
            self.__road_view_list.append(road_view)
            self.__positions.append((block_x, block_y))

    def handle_click(self):
        self.draw()

    def draw(self):
        self.__screen.blit(self.__background, self.__pos)
        
        # 绘制已保存的RoadView实例并显示数量
        for i, (road_view, pos, road_type) in enumerate(zip(self.__road_view_list, self.__positions, self.__road_types)):
            # 绘制道路图标
            road_view.draw()
            
            # 从模型获取当前数量并显示
            road_count = self.__road_list.get_road_num(road_type)
            font = pg.font.SysFont(None, 24)
            count_text = font.render(str(road_count), True, (0, 0, 0))
            text_rect = count_text.get_rect()
            text_rect.centerx = pos[0] + self.__block_size[0] // 2
            text_rect.top = pos[1] + self.__block_size[1] / 2
            self.__screen.blit(count_text, text_rect)