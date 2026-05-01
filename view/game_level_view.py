import pygame as pg
from typing import Tuple, Optional, Union
from view.map_view import MapView
from view.button_view import ButtonView
from view.dialog_view import DialogView
from view.inventory_view import InventoryView
from view.car_view import CarView
from models.gamemodel import GameLevelModel
from models.Road import RoadType, RoadModel
from models.roadcell import RoadCellModel


class GameLevelView:
    def __init__(self, screen: pg.Surface, level_model: GameLevelModel):
        self.screen = screen
        self.model = level_model
        self.font = pg.font.Font(None, 28)

        w, h = screen.get_size()
        map_x = 50
        map_y = 130
        self.map_view = MapView(level_model.map, map_x, map_y, 120, screen)

        # 库存面板（右侧竖排）
        self.inventory = InventoryView(map_x + 4*120 + 40, map_y + 20, screen)
        self.inventory.update_from_model(level_model.player_road_list)

        # 按钮
        self.back_btn = ButtonView(20, 20, 90, 40, "Back")
        self.reset_btn = ButtonView(130, 20, 90, 40, "Reset")
        self.rotate_btn = ButtonView(240, 20, 90, 40, "Rotate")
        self.remove_btn = ButtonView(350, 20, 90, 40, "Remove")
        self.clear_sel_btn = ButtonView(460, 20, 110, 40, "Clear Select")

        # 当前选中的格子
        self.selected_cell: Optional[Tuple[int, int]] = None
        # 当前选中的道路类型（重要！）
        self.selected_road_type: Optional[RoadType] = None

        # 拖拽预览相关（不再依赖 road type，只用于视觉反馈）
        self.is_dragging = False
        self.drag_preview_road = None
        self.drag_mouse_pos = (0, 0)

        # 胜利对话框
        self.win_dialog = DialogView(250, 200, 350, 200)
        self.win_dialog.set_message("Congratulations!\nLevel Complete")
        next_btn = ButtonView(400, 300, 100, 40, "Next")
        self.win_dialog.add_button(next_btn)

        self.car_view = None
        self.showing_win = False

    # ================== 事件处理 ==================
    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        # 胜利状态下只处理对话框按钮
        if self.showing_win:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for btn in self.win_dialog.buttons:
                    if btn.rect.collidepoint(pos):
                        return "next_level"
            return None

        # 键盘事件
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.rotate_selected()
            elif event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                self.remove_selected()
            return None

        # 鼠标按下
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos

            # 左键按下：检查库存按钮，开始拖拽并选中该类型
            if event.button == 1:
                road_type = self.inventory.get_road_type_at(pos)
                if road_type is not None and self.model.player_road_list.get_road_num(road_type) != 0:
                    # 选中该类型（同时库存高亮）
                    self.selected_road_type = road_type
                    self.inventory.selected_type = road_type
                    # 开始拖拽
                    self.is_dragging = True
                    self.drag_preview_road = RoadCellModel(0, 0, road_type)
                    self.drag_mouse_pos = pos
                    return None

                # 点击地图格子（非库存区域），如果有选中类型则放置
                cell_pos = self.map_view.check_click(pos)
                if cell_pos is not None:
                    r, c = cell_pos
                    if not self.model.map.is_locked(r, c):
                        if self.selected_road_type is not None:
                            road = self.model.player_road_list.get_road(self.selected_road_type)
                            if road is not None:
                                new_cell = RoadCellModel(r, c, road.road_type)
                                self.model.map.set_cell(r, c, new_cell)
                                self.inventory.update_from_model(self.model.player_road_list)
                            else:
                                print("No more roads of this type")
                        # 选中该格子
                        self.selected_cell = (r, c)
                    else:
                        print("Locked cell, cannot modify")
                    return None

            # 右键旋转格子
            if event.button == 3:
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and not self.model.map.is_locked(cell_pos[0], cell_pos[1]):
                    r, c = cell_pos
                    cell = self.model.map.get_cell(r, c)
                    if cell is not None:
                        self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                        cell.rotate()
                    return None

        # 鼠标移动（更新拖拽预览位置）
        if event.type == pg.MOUSEMOTION and self.is_dragging:
            self.drag_mouse_pos = event.pos

        # 鼠标释放（结束拖拽并放置）
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                pos = event.pos
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and self.selected_road_type is not None:
                    r, c = cell_pos
                    if not self.model.map.is_locked(r, c):
                        road = self.model.player_road_list.get_road(self.selected_road_type)
                        if road is not None:
                            new_cell = RoadCellModel(r, c, road.road_type)
                            self.model.map.set_cell(r, c, new_cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                            self.selected_cell = (r, c)
                        else:
                            print("No more roads of this type")
                # 清理拖拽状态
                self.is_dragging = False
                self.drag_preview_road = None
                return None

        # 处理按钮点击（在没有拖拽的情况下）
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.is_dragging:
            return self.handle_click(event.pos)

        return None

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """处理按钮点击"""
        if self.back_btn.rect.collidepoint(pos):
            return "back"
        if self.reset_btn.rect.collidepoint(pos):
            self.model.reset()
            self.inventory.update_from_model(self.model.player_road_list)
            self.selected_cell = None
            self.selected_road_type = None
            self.inventory.selected_type = None
            self.car_view = None
            self.showing_win = False
            return None
        if self.rotate_btn.rect.collidepoint(pos):
            self.rotate_selected()
            return None
        if self.remove_btn.rect.collidepoint(pos):
            self.remove_selected()
            return None
        if self.clear_sel_btn.rect.collidepoint(pos):
            self.selected_road_type = None
            self.inventory.selected_type = None
            self.selected_cell = None
            return None

        # 库存面板点击（非拖拽，但已由 MOUSEBUTTONDOWN 处理过，这里不用了）
        return None

    # ================== 旋转 / 移除 ==================
    def rotate_selected(self):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        if self.model.map.is_locked(r, c):
            return
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.map_view.cell_views[r][c].trigger_rotate_animation(500)
            cell.rotate()

    def remove_selected(self):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        if self.model.map.is_locked(r, c):
            return
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.model.player_road_list.store_road(cell.road_model)
            self.model.map.set_cell(r, c, None)
            self.inventory.update_from_model(self.model.player_road_list)
            self.selected_cell = None

    # ================== 更新与绘制 ==================
    def update(self):
        # 检查胜利并创建小车
        if self.model.check_completion() and not self.showing_win:
            self.showing_win = True
            path = self.model.get_path()
            print("Path found:", path)   # 调试输出
            if path:
                self.car_view = CarView(path, 120, (self.map_view.x, self.map_view.y))
        if self.car_view and self.showing_win:
            self.car_view.update()

    def draw(self) -> None:
        self.screen.fill((235, 245, 245))

        # 信息栏
        diff_text = self.font.render(f"Level {self.model.level_id}  {self.model.difficulty.name}", True, (0,0,0))
        score_text = self.font.render(f"Score: {self.model.score}", True, (0,0,0))
        self.screen.blit(diff_text, (20, 70))
        self.screen.blit(score_text, (20, 95))

        self.back_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.rotate_btn.draw(self.screen)
        self.remove_btn.draw(self.screen)
        self.clear_sel_btn.draw(self.screen)

        self.map_view.draw()
        self.inventory.draw()

        # 选中格子蓝框
        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c*120, self.map_view.y + r*120, 120, 120)
            pg.draw.rect(self.screen, (0, 0, 255), rect, 3)

        # 拖拽预览（半透明道路跟随鼠标）
        if self.is_dragging and self.drag_preview_road is not None:
            preview_rect = pg.Rect(self.drag_mouse_pos[0]-60, self.drag_mouse_pos[1]-60, 120, 120)
            temp_surf = pg.Surface((120, 120), pg.SRCALPHA)
            from view.road import RoadView
            RoadView(self.drag_preview_road, temp_surf, pg.Rect(0, 0, 120, 120)).draw()
            temp_surf.set_alpha(150)
            self.screen.blit(temp_surf, preview_rect)

        # 小车动画与对话框
        if self.car_view and self.showing_win:
            self.car_view.draw(self.screen)
            if self.car_view.finished:
                self.win_dialog.draw(self.screen)
        elif self.showing_win and self.car_view is None:
            self.win_dialog.draw(self.screen)