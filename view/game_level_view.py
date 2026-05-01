import pygame as pg
from typing import Tuple, Optional
from view.map_view import MapView
from view.button_view import ButtonView
from view.dialog_view import DialogView
from view.inventory_view import InventoryView
from view.car_view import CarView
from models.gamemodel import GameLevelModel
from models.Road import RoadType
from models.roadcell import RoadCellModel

class GameLevelView:
    def __init__(self, screen: pg.Surface, level_model: GameLevelModel):
        self.screen = screen
        self.model = level_model
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 18)

        w, h = screen.get_size()
        map_x = 50
        map_y = 130
        self.map_view = MapView(level_model.map, map_x, map_y, 120, screen)

        self.inventory = InventoryView(map_x + 4*120 + 40, map_y + 10, screen)
        self.inventory.update_from_model(level_model.player_road_list)

        self.back_btn = ButtonView(20, 20, 90, 40, "Back")
        self.reset_btn = ButtonView(130, 20, 90, 40, "Reset")
        self.rotate_btn = ButtonView(240, 20, 90, 40, "Rotate")
        self.remove_btn = ButtonView(350, 20, 90, 40, "Remove")
        self.clear_btn = ButtonView(460, 20, 110, 40, "Clear Sel")
        self.submit_btn = ButtonView(580, 20, 90, 40, "Submit")

        self.selected_cell: Optional[Tuple[int, int]] = None
        self.selected_road_type: Optional[RoadType] = None

        self.is_dragging = False
        self.drag_preview_road = None
        self.drag_mouse_pos = (0, 0)

        # 提示对话框
        self.info_dialog = DialogView(250, 200, 350, 150)
        self.info_dialog.add_button(
            ButtonView(400, 290, 80, 35, "OK", callback=self.info_dialog.hide)
        )

        # 胜利对话框（先配置好，但不显示）
        self.win_dialog = DialogView(230, 180, 340, 240)
        self.win_dialog.visible = False
        self.win_dialog.message = ""
        self.win_dialog.buttons = []
        self._win_dialog_ready = False   # 标记是否已经配置好但等待显示

        self.car_view = None
        self.showing_win = False

    # ================= 提示 =================
    def show_info(self, msg: str):
        self.info_dialog.set_message(msg)
        self.info_dialog.show()

    def setup_win_dialog(self):
        """配置胜利对话框的消息和按钮，但不显示"""
        score = self.model.score
        level = self.model.level_id
        msg = f"Congratulations!\nLevel {level} Complete\nYour Score: {score}"
        self.win_dialog.set_message(msg)
        self.win_dialog.buttons.clear()
        btn_y = self.win_dialog.rect.bottom - 60
        next_btn = ButtonView(self.win_dialog.rect.centerx - 110, btn_y, 100, 40, "Next")
        back_btn = ButtonView(self.win_dialog.rect.centerx + 10, btn_y, 100, 40, "Back")
        self.win_dialog.add_button(next_btn)
        self.win_dialog.add_button(back_btn)
        self._win_dialog_ready = True

    # ================= 事件处理 =================
    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        # 信息对话框拦截
        if self.info_dialog.visible:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.info_dialog.buttons:
                    if btn.rect.collidepoint(event.pos):
                        btn.callback()
            return None

        # 胜利对话框可见时处理按钮
        if self.win_dialog.visible:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for btn in self.win_dialog.buttons:
                    if btn.rect.collidepoint(pos):
                        if btn.text == "Next":
                            return "next_level"
                        elif btn.text == "Back":
                            return "back_to_select"
            return None

        # 键盘操作
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.rotate_selected()
            elif event.key in (pg.K_DELETE, pg.K_BACKSPACE):
                self.remove_selected()
            return None

        # 鼠标按下
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos

            if event.button == 1:
                # 库存按钮
                road_type = self.inventory.get_road_type_at(pos)
                if road_type is not None:
                    self.selected_road_type = road_type
                    self.inventory.selected_type = road_type
                    self.is_dragging = True
                    self.drag_preview_road = RoadCellModel(0, 0, road_type)
                    self.drag_mouse_pos = pos
                    self.model.start_timer()
                    return None

                # 地图格子点击
                cell_pos = self.map_view.check_click(pos)
                if cell_pos is not None:
                    r, c = cell_pos
                    locked = self.model.map.is_locked(r, c)
                    existing = self.model.map.get_cell(r, c)

                    if not locked:
                        self.selected_cell = (r, c)

                    if not locked and existing is None and self.selected_road_type is not None:
                        road = self.model.player_road_list.get_road(self.selected_road_type)
                        if road is not None:
                            new_cell = RoadCellModel(r, c, road.road_type)
                            self.model.map.set_cell(r, c, new_cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                            self.model.start_timer()
                        else:
                            self.show_info("No more roads of this type!")
                    return None

            # 右键旋转
            if event.button == 3:
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and not self.model.map.is_locked(cell_pos[0], cell_pos[1]):
                    r, c = cell_pos
                    cell = self.model.map.get_cell(r, c)
                    if cell is not None:
                        self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                        cell.rotate()
                        self.model.start_timer()
                    return None

        # 鼠标移动
        if event.type == pg.MOUSEMOTION and self.is_dragging:
            self.drag_mouse_pos = event.pos

        # 鼠标释放（拖放）
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                pos = event.pos
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and self.selected_road_type is not None:
                    r, c = cell_pos
                    locked = self.model.map.is_locked(r, c)
                    existing = self.model.map.get_cell(r, c)
                    if not locked and existing is None:
                        road = self.model.player_road_list.get_road(self.selected_road_type)
                        if road is not None:
                            new_cell = RoadCellModel(r, c, road.road_type)
                            self.model.map.set_cell(r, c, new_cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                            self.selected_cell = (r, c)
                            self.model.start_timer()
                        else:
                            self.show_info("No more roads of this type!")
                    elif not locked and existing is not None:
                        self.selected_cell = (r, c)
                self.is_dragging = False
                self.drag_preview_road = None
                return None

        # 按钮点击（无拖拽）
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.is_dragging:
            pos = event.pos
            if self.back_btn.rect.collidepoint(pos):
                return "back"
            if self.reset_btn.rect.collidepoint(pos):
                self.reset_all()
                return None
            if self.rotate_btn.rect.collidepoint(pos):
                self.rotate_selected()
                return None
            if self.remove_btn.rect.collidepoint(pos):
                self.remove_selected()
                return None
            if self.clear_btn.rect.collidepoint(pos):
                self.selected_road_type = None
                self.inventory.selected_type = None
                self.selected_cell = None
                return None
            if self.submit_btn.rect.collidepoint(pos):
                self.try_submit()
                return None

        return None

    def try_submit(self):
        """提交检查：连通→启动小车；否则提示"""
        if self.model.map.is_path_connected():
            # 计算分数并设置完成状态
            self.model.check_completion()
            self.showing_win = True
            path = self.model.get_path()
            if path:
                self.car_view = CarView(path, 120, (self.map_view.x, self.map_view.y))
                self._win_dialog_ready = False   # 等待小车跑完再显示对话框
            else:
                # 极端情况：连通但没路径（不应发生），直接显示胜利对话框
                self.setup_win_dialog()
                self.win_dialog.show()
        else:
            self.show_info("Path not connected!\nKeep trying.")

    # ================= 旋转 / 移除 / 重置 =================
    def rotate_selected(self):
        if self.selected_cell is None: return
        r, c = self.selected_cell
        if self.model.map.is_locked(r, c): return
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.map_view.cell_views[r][c].trigger_rotate_animation(500)
            cell.rotate()
            self.model.start_timer()

    def remove_selected(self):
        if self.selected_cell is None: return
        r, c = self.selected_cell
        if self.model.map.is_locked(r, c): return
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.model.player_road_list.store_road(cell.road_model)
            self.model.map.set_cell(r, c, None)
            self.inventory.update_from_model(self.model.player_road_list)
            self.selected_cell = None
            self.model.start_timer()

    def reset_all(self):
        self.model.reset()
        self.inventory.update_from_model(self.model.player_road_list)
        self.selected_cell = None
        self.selected_road_type = None
        self.inventory.selected_type = None
        self.car_view = None
        self.showing_win = False
        self.win_dialog.hide()
        self._win_dialog_ready = False

    # ================= 更新与绘制 =================
    def update(self):
        self.model.update_time()

        # 小车行驶
        if self.car_view and self.showing_win:
            self.car_view.update()
            # 小车到达终点后，显示胜利对话框（仅一次）
            if self.car_view.finished and not self._win_dialog_ready:
                self.setup_win_dialog()
                self.win_dialog.show()
                self._win_dialog_ready = True

    def draw(self):
        self.screen.fill((235, 245, 245))

        diff_str = f"Level {self.model.level_id}  {self.model.difficulty.name}"
        time_str = f"Time: {self.model.get_elapsed_seconds():.1f}s"
        self.screen.blit(self.font.render(diff_str, True, (0,0,0)), (20, 70))
        self.screen.blit(self.font.render(time_str, True, (0,0,0)), (200, 70))

        sel_str = "Selected: " + (self.selected_road_type.name.replace("_ROAD","") if self.selected_road_type else "None")
        self.screen.blit(self.small_font.render(sel_str, True, (0,0,0)), (560, 70))

        self.back_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.rotate_btn.draw(self.screen)
        self.remove_btn.draw(self.screen)
        self.clear_btn.draw(self.screen)
        self.submit_btn.draw(self.screen)

        self.map_view.draw()
        self.inventory.draw()

        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c*120, self.map_view.y + r*120, 120, 120)
            pg.draw.rect(self.screen, (0, 0, 255), rect, 3)

        # 拖拽预览
        if self.is_dragging and self.drag_preview_road is not None:
            preview_rect = pg.Rect(self.drag_mouse_pos[0]-60, self.drag_mouse_pos[1]-60, 120, 120)
            temp = pg.Surface((120, 120), pg.SRCALPHA)
            from view.road import RoadView
            RoadView(self.drag_preview_road, temp, pg.Rect(0,0,120,120)).draw()
            temp.set_alpha(150)
            self.screen.blit(temp, preview_rect)

        # 小车行驶中
        if self.car_view and self.showing_win:
            self.car_view.draw(self.screen)

        # 胜利对话框（只有小车跑完或特殊情况下显示）
        if self.win_dialog.visible:
            self.win_dialog.draw(self.screen)

        # 信息提示对话框
        if self.info_dialog.visible:
            self.info_dialog.draw(self.screen)