import pygame as pg
from typing import Tuple, Optional
from view.map_view import MapView
from view.button_view import ButtonView
from view.dialog_view import DialogView
from view.inventory_view import InventoryView
from view.car_view import CarView
from view.passmenu import PassMenuView
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

        self.selected_cell: Optional[Tuple[int, int]] = None
        self.selected_road_type: Optional[RoadType] = None

        self.is_dragging = False
        self.drag_preview_road = None
        self.drag_mouse_pos = (0, 0)

        self.info_dialog = DialogView(250, 200, 350, 150)
        self.info_dialog.add_button(
            ButtonView(400, 290, 80, 35, "OK", callback=self.info_dialog.hide)
        )

        self.pass_menu = None
        self._pass_menu_ready = False

        self.car_view = None
        self.showing_win = False

        # 小车初始化：放在起点
        start_cell = None
        for r in range(self.model.map.rows):
            for c in range(self.model.map.cols):
                cell = self.model.map.get_cell(r, c)
                if cell and cell.get_type() == RoadType.START_ROAD:
                    start_cell = (r, c)
                    break
            if start_cell:
                break
        self.car_view = CarView(120, (self.map_view.x, self.map_view.y),
                                start_grid=start_cell)

    def show_info(self, msg: str):
        self.info_dialog.set_message(msg)
        self.info_dialog.show()

    def show_pass_menu(self):
        score = self.model.score
        self.pass_menu = PassMenuView(self.screen, score, self.model.level_id)
        self.pass_menu.visible = True
        self._pass_menu_ready = True

    def try_autocomplete(self):
        if self.showing_win:
            return
        if self.model.map.is_path_connected():
            self.model.check_completion()
            self.showing_win = True
            path = self.model.get_path()
            print("[SUCCESS] 连通！路径：", path)
            if path:
                self.car_view.start_move(path)
                self._pass_menu_ready = False

    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        if self.info_dialog.visible:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.info_dialog.buttons:
                    if btn.rect.collidepoint(event.pos):
                        btn.callback()
            return None

        if self.showing_win:
            if self.pass_menu is not None and self.pass_menu.visible:
                action = self.pass_menu.handle_event(event)
                if action == 'next_level':
                    return 'next_level'
                elif action == 'retry':
                    self.reset_all()
                    return None
            return None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.rotate_selected()
                self.try_autocomplete()
            elif event.key in (pg.K_DELETE, pg.K_BACKSPACE):
                self.remove_selected()
                self.try_autocomplete()
            return None

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1:
                road_type = self.inventory.get_road_type_at(pos)
                if road_type is not None:
                    self.selected_road_type = road_type
                    self.inventory.selected_type = road_type
                    self.is_dragging = True
                    self.drag_preview_road = RoadCellModel(0, 0, road_type)
                    self.drag_mouse_pos = pos
                    self.model.start_timer()
                    return None

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
                            new_cell = RoadCellModel(r, c, road.road_type, road_model=road)
                            self.model.map.set_cell(r, c, new_cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                            self.model.start_timer()
                            self.try_autocomplete()
                        else:
                            self.show_info("No more roads of this type!")
                    return None

            if event.button == 3:
                cell_pos = self.map_view.check_click(pos)
                if cell_pos and not self.model.map.is_locked(cell_pos[0], cell_pos[1]):
                    r, c = cell_pos
                    cell = self.model.map.get_cell(r, c)
                    if cell is not None:
                        self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                        cell.rotate()
                        self.model.start_timer()
                        self.try_autocomplete()
                    return None

        if event.type == pg.MOUSEMOTION and self.is_dragging:
            self.drag_mouse_pos = event.pos

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
                            new_cell = RoadCellModel(r, c, road.road_type, road_model=road)
                            self.model.map.set_cell(r, c, new_cell)
                            self.inventory.update_from_model(self.model.player_road_list)
                            self.selected_cell = (r, c)
                            self.model.start_timer()
                            self.try_autocomplete()
                        else:
                            self.show_info("No more roads of this type!")
                    elif not locked and existing is not None:
                        self.selected_cell = (r, c)
                self.is_dragging = False
                self.drag_preview_road = None
                return None

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.is_dragging:
            pos = event.pos
            if self.back_btn.rect.collidepoint(pos):
                return "back"
            if self.reset_btn.rect.collidepoint(pos):
                self.reset_all()
                return None
            if self.rotate_btn.rect.collidepoint(pos):
                self.rotate_selected()
                self.try_autocomplete()
                return None
            if self.remove_btn.rect.collidepoint(pos):
                self.remove_selected()
                self.try_autocomplete()
                return None
            if self.clear_btn.rect.collidepoint(pos):
                self.selected_road_type = None
                self.inventory.selected_type = None
                self.selected_cell = None
                return None

        return None

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
        self.showing_win = False
        self.pass_menu = None
        self._pass_menu_ready = False

        start_cell = None
        for r in range(self.model.map.rows):
            for c in range(self.model.map.cols):
                cell = self.model.map.get_cell(r, c)
                if cell and cell.get_type() == RoadType.START_ROAD:
                    start_cell = (r, c)
                    break
            if start_cell:
                break
        self.car_view = CarView(120, (self.map_view.x, self.map_view.y),
                                start_grid=start_cell)

    def update(self):
        self.model.update_time()
        # 更新小车（无论是否胜利）
        self.car_view.update()
        # 小车到终点后弹出菜单
        if self.showing_win and self.car_view.finished and not self._pass_menu_ready:
            self.show_pass_menu()
            self._pass_menu_ready = True

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

        self.map_view.draw()
        self.inventory.draw()

        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c*120, self.map_view.y + r*120, 120, 120)
            pg.draw.rect(self.screen, (0, 0, 255), rect, 3)

        if self.is_dragging and self.drag_preview_road is not None:
            preview_rect = pg.Rect(self.drag_mouse_pos[0]-60, self.drag_mouse_pos[1]-60, 120, 120)
            temp = pg.Surface((120, 120), pg.SRCALPHA)
            from view.road import RoadView
            RoadView(self.drag_preview_road, temp, pg.Rect(0,0,120,120)).draw()
            temp.set_alpha(150)
            self.screen.blit(temp, preview_rect)

        # 小车始终绘制
        self.car_view.draw(self.screen)

        if self.pass_menu is not None and self.pass_menu.visible:
            self.pass_menu.draw()

        if self.info_dialog.visible:
            self.info_dialog.draw(self.screen)