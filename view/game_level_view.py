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
from view.road import RoadView

class GameLevelView:
    def __init__(self, screen: pg.Surface, level_model: GameLevelModel):
        self.screen = screen
        self.model = level_model
        self.font = pg.font.Font(None, 28)

        w, h = screen.get_size()
        map_x = 50
        map_y = 130
        self.map_view = MapView(level_model.map, map_x, map_y, 120, screen)

        # 库存面板
        self.inventory = InventoryView(map_x + 4*120 + 20, 150, screen)
        self.inventory.update_from_model(level_model.player_road_list)

        self.back_btn = ButtonView(20, 20, 90, 40, "Back")
        self.reset_btn = ButtonView(130, 20, 90, 40, "Reset")
        self.rotate_btn = ButtonView(240, 20, 90, 40, "Rotate")
        self.remove_btn = ButtonView(350, 20, 90, 40, "Remove")
        self.selected_cell: Optional[Tuple[int, int]] = None

        # 拖拽相关
        self.drag_road_type: Optional[RoadType] = None
        self.drag_preview_road: Optional[RoadCellModel] = None  # 用于绘制预览
        self.drag_mouse_pos: Tuple[int, int] = (0, 0)
        self.is_dragging: bool = False

        # 胜利
        self.win_dialog = DialogView(250, 200, 350, 200)
        self.win_dialog.set_message("Congratulations!\nLevel Complete")
        next_btn = ButtonView(400, 300, 100, 40, "Next")
        self.win_dialog.add_button(next_btn)
        self.car_view = None
        self.showing_win = False

    # 事件处理方法
    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        """处理所有事件，返回动作字符串如 'back', 'next_level' 或 None"""
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
            # 检查库存面板拖拽开始
            if event.button == 1:
                road_type = self.inventory.get_road_type_at(pos)
                if road_type is not None and self.model.player_road_list.get_road_num(road_type) != 0:
                    # 开始拖拽（但也要准备点击，这里记录起来）
                    self.drag_road_type = road_type
                    self.is_dragging = True
                    self.drag_mouse_pos = pos
                    # 创建一个预览用的 RoadCellModel，没有实际位置
                    self.drag_preview_road = RoadCellModel(0, 0, road_type)
                    return None

            # 右键旋转或移除（右键旋转格子）
            if event.button == 3:
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and self.model.map.is_locked(cell_pos[0], cell_pos[1]) == False:
                    r, c = cell_pos
                    cell = self.model.map.get_cell(r, c)
                    if cell is not None:
                        # 旋转并动画
                        self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                        cell.rotate()
                    else:
                        # 空地上右键无效
                        pass
                return None

        # 鼠标释放
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.is_dragging:
                pos = event.pos
                # 检查是否释放在地图格子上
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and self.drag_road_type is not None:
                    r, c = cell_pos
                    if not self.model.map.is_locked(r, c):
                        road = self.model.player_road_list.get_road(self.drag_road_type)
                        if road is not None:
                            cell = RoadCellModel(r, c, road.road_type)
                            self.model.map.set_cell(r, c, cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                # 结束拖拽
                self.is_dragging = False
                self.drag_road_type = None
                self.drag_preview_road = None
                return None

            # 如果没有拖拽移动，只是点击，处理按钮
            if not self.is_dragging:
                return self.handle_click(event.pos)

        # 鼠标移动（拖拽中）
        if event.type == pg.MOUSEMOTION and self.is_dragging:
            self.drag_mouse_pos = event.pos

        # 按钮点击（非拖拽时）
        if event.type == pg.MOUSEBUTTONDOWN and not self.is_dragging:
            return self.handle_click(event.pos)

        return None

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """处理简单的点击事件（无拖拽时）"""
        # 返回按钮
        if self.back_btn.rect.collidepoint(pos):
            return "back"
        if self.reset_btn.rect.collidepoint(pos):
            self.model.reset()
            self.inventory.update_from_model(self.model.player_road_list)
            self.selected_cell = None
            self.car_view = None
            self.showing_win = False
            self.drag_reset()
            return None
        if self.rotate_btn.rect.collidepoint(pos):
            self.rotate_selected()
            return None
        if self.remove_btn.rect.collidepoint(pos):
            self.remove_selected()
            return None

        # 库存面板点击（左键选中类型，不拖拽）
        road_type = self.inventory.handle_click(pos)
        if road_type is not None:
            self.selected_road_type = road_type
            return None

        # 地图格子点击（放置选中的类型，或选中格子）
        cell_pos = self.map_view.check_click(pos)
        if cell_pos is not None:
            r, c = cell_pos
            if self.model.map.is_locked(r, c):
                print("Cannot modify locked cell")
                return None
            # 如果有选中的道路类型，则放置
            if hasattr(self, 'selected_road_type') and self.selected_road_type is not None:
                road = self.model.player_road_list.get_road(self.selected_road_type)
                if road is not None:
                    cell = RoadCellModel(r, c, road.road_type)
                    self.model.map.set_cell(r, c, cell)
                    self.inventory.update_from_model(self.model.player_road_list)
                else:
                    print("No more roads of this type")
            # 无论是否放置，选中此格子
            self.selected_cell = (r, c)
            return None
        return None

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
            # 还原库存
            road_model = cell.road_model
            self.model.player_road_list.store_road(road_model)
            self.model.map.set_cell(r, c, None)
            self.inventory.update_from_model(self.model.player_road_list)

    def drag_reset(self):
        self.is_dragging = False
        self.drag_road_type = None
        self.drag_preview_road = None

    def update(self):
        if self.model.check_completion() and not self.showing_win:
            self.showing_win = True
            path = self.model.get_path()
            if path:
                self.car_view = CarView(path, 120, (self.map_view.x, self.map_view.y))
        if self.car_view and self.showing_win:
            self.car_view.update()
            if self.car_view.finished:
                # 动画完成
                pass

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

        self.map_view.draw()
        self.inventory.draw()

        # 绘制选中格子的高亮
        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c*120, self.map_view.y + r*120, 120, 120)
            pg.draw.rect(self.screen, (0, 0, 255), rect, 3)

        # 拖拽预览
        if self.is_dragging and self.drag_preview_road is not None:
            # 绘制半透明道路跟随鼠标
            preview_rect = pg.Rect(self.drag_mouse_pos[0]-60, self.drag_mouse_pos[1]-60, 120, 120)
            temp_surf = pg.Surface((120, 120), pg.SRCALPHA)
            RoadView(self.drag_preview_road, temp_surf, pg.Rect(0, 0, 120, 120)).draw()
            temp_surf.set_alpha(150)
            self.screen.blit(temp_surf, preview_rect)

        # 小车动画 & 对话框
        if self.car_view and self.showing_win:
            self.car_view.draw(self.screen)
            if self.car_view.finished:
                self.win_dialog.draw(self.screen)
        elif self.showing_win and self.car_view is None:
            self.win_dialog.draw(self.screen)