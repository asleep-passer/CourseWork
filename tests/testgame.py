import pygame as pg
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.map import MapModel
from models.roadcell import RoadCellModel
from models.Road import RoadType, RoadModel
from view.map_view import MapView
from view.inventory_view import InventoryView

# ====================== 初始化游戏 ======================
pg.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("道路拼图游戏")
clock = pg.time.Clock()

# ====================== 创建测试地图 ======================
def create_test_map():
    map_model = MapModel(rows=4, cols=4)
    for r in range(4):
        for c in range(4):
            map_model.set_cell(r,c, RoadCellModel(r,c, RoadType.OBSTACLE_ROAD))
    map_model.set_cell(3,0, RoadCellModel(3,0, RoadType.START_ROAD))
    map_model.set_cell(0,3, RoadCellModel(0,3, RoadType.END_ROAD))
    for r in range(4):
        for c in range(4):
            if not ((r==3 and c==0) or (r==0 and c==3)):
                map_model.set_cell(r,c, None)
    return map_model

# ====================== 初始化视图 ======================
test_map = create_test_map()
map_view = MapView(test_map, 200, 100, 150, screen)
inventory = InventoryView(230, 720, 100, screen)

# 选中的地图格子（用于 R 键旋转）
selected_map_cell = None

# ====================== 主循环 ======================
running = True
while running:
    screen.fill((240, 248, 255))
    map_view.draw()
    inventory.draw()

    # ============== 事件处理 ==============
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # -------- 鼠标点击地图格子 --------
        if event.type == pg.MOUSEBUTTONDOWN:
            cell = map_view.check_click(event.pos)
            if cell:
                selected_map_cell = cell
            inventory.handle_click(event.pos)

        # -------- R 键：旋转选中的格子（绝对生效） --------
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r and selected_map_cell:
                r,c = selected_map_cell
                if not test_map.is_locked(r,c):
                    map_view.rotate_cell(r,c)

        # -------- 拖拽 --------
        if event.type == pg.MOUSEMOTION and inventory.dragging:
            inventory.drag_pos = event.pos

        # -------- 放置道路 --------
        if event.type == pg.MOUSEBUTTONUP:
            if inventory.dragging:
                cell = map_view.check_click(event.pos)
                road = inventory.get_selected_road()
                if cell and road:
                    r,c = cell
                    if test_map.get_cell(r,c) is None and not test_map.is_locked(r,c):
                        test_map.set_cell(r,c, RoadCellModel(r,c, road))
                        map_view = MapView(test_map,200,100,150,screen)
            inventory.stop_drag()

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()