import pygame as pg
import os
from typing import Tuple, Optional, List
from models.roadlist import NormalRoadListModel
from view.map_view import MapView
from view.button_view import ButtonView
from view.dialog_view import DialogView
from models.gamemodel import GameLevelModel
from models.Road import RoadType
from models.roadcell import RoadCellModel
from models.map import MapModel
import config


class EditorInventoryView:
    def __init__(self, x, y, screen, model):
        self.x = x
        self.y = y
        self.screen = screen
        self.model = model
        self.font = pg.font.Font(None, 28)
        self.small_font = pg.font.Font(None, 22)

        self.editor_types = [
            RoadType.OBSTACLE_ROAD,
            RoadType.START_ROAD,
            RoadType.END_ROAD
        ]

        self.editable_types = [
            RoadType.STRAIGHT_ROAD,
            RoadType.BEND_ROAD,
            RoadType.T_SHAPED_ROAD,
            RoadType.CROSS_ROAD
        ]

        self.buttons = []
        self.counts = {}
        self.selected_type = None

        self.minus_buttons = []
        self.plus_buttons = []

        self._create_buttons()

    def _create_buttons(self):
        btn_width = 180
        btn_height = 50
        spacing = 55

        for i, rt in enumerate(self.editor_types):
            btn_rect = pg.Rect(self.x, self.y + i * spacing, btn_width, btn_height)
            self.buttons.append((btn_rect, rt))

        for rt in self.editable_types:
            self.counts[rt] = str(self.model.player_road_list.get_road_num(rt))

    def handle_click(self, pos):
        for rect, rt in self.buttons:
            if rect.collidepoint(pos):
                if rt in self.editor_types:
                    self.selected_type = rt
                    return rt

        section_y = self.y + len(self.editor_types) * 60 + 20
        start_y = section_y + 40
        row_spacing = 35
        btn_w, btn_h = 30, 25
        for i, rt in enumerate(self.editable_types):
            label_y = start_y + i * row_spacing
            minus_rect = pg.Rect(self.x + 90, label_y - 5, btn_w, btn_h)
            plus_rect = pg.Rect(self.x + 140, label_y - 5, btn_w, btn_h)
            if minus_rect.collidepoint(pos):
                self._change_count(rt, -1)
                return rt
            elif plus_rect.collidepoint(pos):
                self._change_count(rt, 1)
                return rt
        return None

    def _change_count(self, rt, delta):
        cur = int(self.counts[rt])
        cur += delta
        if cur < 0:
            cur = 0
        if cur > 999:
            cur = 999
        self.counts[rt] = str(cur)

    def apply_counts(self):
        new_counts = []
        for rt in self.editable_types:
            new_counts.append(int(self.counts[rt]))
        self.model.player_road_list = NormalRoadListModel(*new_counts)

    def draw(self):
        title = self.font.render("Editor Tools", True, (0, 0, 0))
        self.screen.blit(title, (self.x, self.y - 45))

        for rect, rt in self.buttons:
            if rt in self.editor_types:
                is_selected = (rt == self.selected_type)
                bg_color = (180, 180, 180) if is_selected else (220, 220, 220)
                pg.draw.rect(self.screen, bg_color, rect)
                pg.draw.rect(self.screen, (0, 0, 0), rect, 2)

                text_str = rt.name.replace("_ROAD", "")
                text = self.small_font.render(text_str, True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

        section_title = self.font.render("Available Roads", True, (0, 0, 0))
        section_y = self.y + len(self.editor_types) * 60 + 20
        self.screen.blit(section_title, (self.x, section_y))

        row_spacing = 35
        start_y = section_y + 40
        btn_w, btn_h = 30, 25
        for i, rt in enumerate(self.editable_types):
            label_y = start_y + i * row_spacing

            type_text = self.small_font.render(rt.name.replace("_ROAD", ""), True, (0, 0, 0))
            self.screen.blit(type_text, (self.x, label_y))

            minus_rect = pg.Rect(self.x + 90, label_y - 5, btn_w, btn_h)
            pg.draw.rect(self.screen, (200, 200, 200), minus_rect)
            pg.draw.rect(self.screen, (0, 0, 0), minus_rect, 2)
            minus_text = self.small_font.render("-", True, (0, 0, 0))
            self.screen.blit(minus_text, (minus_rect.x + 8, minus_rect.y))

            count_str = self.counts[rt]
            count_text = self.small_font.render(count_str, True, (0, 0, 0))
            self.screen.blit(count_text, (self.x + 120, label_y))

            plus_rect = pg.Rect(self.x + 140, label_y - 5, btn_w, btn_h)
            pg.draw.rect(self.screen, (200, 200, 200), plus_rect)
            pg.draw.rect(self.screen, (0, 0, 0), plus_rect, 2)
            plus_text = self.small_font.render("+", True, (0, 0, 0))
            self.screen.blit(plus_text, (plus_rect.x + 8, plus_rect.y))


class LevelEditorView:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 18)

        w, h = screen.get_size()
        map_x = 50
        map_y = 130
        self.model = GameLevelModel(level_id=999)
        self.model.map = MapModel(rows=4, cols=4)
        self.model.player_road_list = NormalRoadListModel(10, 6, 3, 1)

        self.map_view = MapView(self.model.map, map_x, map_y, 120, screen)

        inventory_x = w - 210
        inventory_y = 150
        self.inventory = EditorInventoryView(inventory_x, inventory_y, screen, self.model)

        btn_w = 130
        btn_h = 50
        self.back_btn = ButtonView(20, 20, btn_w, btn_h, "Back")
        self.reset_btn = ButtonView(160, 20, btn_w, btn_h, "Reset")
        self.save_btn = ButtonView(300, 20, btn_w, btn_h, "Save")
        self.clear_btn = ButtonView(440, 20, btn_w, btn_h, "Clear")
        self.remove_btn = ButtonView(580, 20, btn_w + 20, btn_h, "Remove")

        self.selected_cell: Optional[Tuple[int, int]] = None
        self.selected_road_type: Optional[RoadType] = None

        self.info_dialog = DialogView(250, 200, 350, 150)
        self.info_dialog.add_button(
            ButtonView(400, 290, 80, 35, "OK", callback=self.info_dialog.hide)
        )

        self.edit_level_id = None

        self.background = None
        try:
            path = os.path.join("view", "assets", "backgrounds", "level_editor.png")
            img = pg.image.load(path).convert()
            self.background = pg.transform.scale(img, self.screen.get_size())
        except Exception:
            pass

    def show_info(self, msg: str):
        self.info_dialog.set_message(msg)
        self.info_dialog.show()

    def get_next_level_id(self):
        level_id = 5
        while True:
            file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
            if not os.path.exists(file_path):
                return level_id
            level_id += 1

    def load_level(self, level_id: int):
        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
        if not os.path.exists(file_path):
            self.show_info(f"Level file level{level_id}.txt not found!")
            return

        try:
            with open(file_path, 'r') as f:
                lines = f.read().strip().split('\n')
                rows, cols = map(int, lines[0].split())
                type_map = []
                for i in range(4):
                    type_map.append(list(map(int, lines[1 + i].split())))

                last_line = lines[-1] if lines else ""
                counts = list(map(int, last_line.split()))

            self.model.map.reset()

            for r in range(4):
                for c in range(4):
                    cell_type_num = type_map[r][c]
                    cell = None
                    if cell_type_num == 5:
                        cell = RoadCellModel(r, c, RoadType.START_ROAD)
                    elif cell_type_num == 6:
                        cell = RoadCellModel(r, c, RoadType.END_ROAD)
                    elif cell_type_num == 0:
                        cell = RoadCellModel(r, c, RoadType.OBSTACLE_ROAD)
                    if cell:
                        self.model.map.set_cell(r, c, cell)

            self.model.player_road_list = NormalRoadListModel(*counts)
            for rt in self.inventory.editable_types:
                self.inventory.counts[rt] = str(self.model.player_road_list.get_road_num(rt))

            self.edit_level_id = level_id

            self.clear_selection()

        except Exception as e:
            self.show_info(f"Error loading level: {str(e)}")

    def save_level(self):
        self.inventory.apply_counts()

        start_count = 0
        end_count = 0
        for r in range(4):
            for c in range(4):
                cell = self.model.map.get_cell(r, c)
                if cell:
                    if cell.get_type() == RoadType.START_ROAD:
                        start_count += 1
                    elif cell.get_type() == RoadType.END_ROAD:
                        end_count += 1

        if start_count < 1 or end_count < 1:
            self.show_info("Error: Level must have at\nleast one start and one end point!")
            return False

        if self.edit_level_id is not None:
            level_id = self.edit_level_id
        else:
            level_id = self.get_next_level_id()
            self.edit_level_id = level_id

        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")

        try:
            with open(file_path, 'w') as f:
                f.write("4 4\n")

                road_types = []
                for r in range(4):
                    row = []
                    for c in range(4):
                        cell = self.model.map.get_cell(r, c)
                        if cell:
                            if cell.get_type() == RoadType.START_ROAD:
                                row.append("5")
                            elif cell.get_type() == RoadType.END_ROAD:
                                row.append("6")
                            elif cell.get_type() == RoadType.OBSTACLE_ROAD:
                                row.append("0")
                            else:
                                row.append("7")
                        else:
                            row.append("7")
                    road_types.append(" ".join(row))
                f.write("\n".join(road_types) + "\n")

                locked_status = ["0 0 0 0"] * 4
                f.write("\n".join(locked_status) + "\n")

                rotation_status = ["0 0 0 0"] * 4
                f.write("\n".join(rotation_status) + "\n")

                straight = self.model.player_road_list.get_road_num(RoadType.STRAIGHT_ROAD)
                bend = self.model.player_road_list.get_road_num(RoadType.BEND_ROAD)
                t_shape = self.model.player_road_list.get_road_num(RoadType.T_SHAPED_ROAD)
                cross = self.model.player_road_list.get_road_num(RoadType.CROSS_ROAD)
                f.write(f"{straight} {bend} {t_shape} {cross}")

            self.show_info(f"Level saved successfully\nas level{level_id}.txt!")
            return True

        except Exception as e:
            self.show_info(f"Error saving level: {str(e)}")
            return False

    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        if self.info_dialog.visible:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.info_dialog.buttons:
                    if btn.rect.collidepoint(event.pos):
                        btn.callback()
            return None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return "back_to_menu"
            return None

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1:
                if self.back_btn.rect.collidepoint(pos):
                    return "back_to_menu"
                if self.reset_btn.rect.collidepoint(pos):
                    self.reset_editor()
                    return None
                if self.save_btn.rect.collidepoint(pos):
                    self.save_level()
                    return None
                if self.clear_btn.rect.collidepoint(pos):
                    self.clear_selection()
                    return None
                if self.remove_btn.rect.collidepoint(pos):
                    self.remove_selected()
                    return None

                road_type = self.inventory.handle_click(pos)
                if road_type is not None:
                    self.selected_road_type = road_type
                    return None

                cell_pos = self.map_view.check_click(pos)
                if cell_pos is not None:
                    r, c = cell_pos
                    self.selected_cell = (r, c)

                    if self.selected_road_type is not None:
                        if self.selected_road_type in [RoadType.START_ROAD, RoadType.END_ROAD, RoadType.OBSTACLE_ROAD]:
                            new_cell = RoadCellModel(r, c, self.selected_road_type)
                            self.model.map.set_cell(r, c, new_cell)
                    return None

                self.selected_road_type = None

            if event.button == 3:
                cell_pos = self.map_view.check_click(pos)
                if cell_pos:
                    r, c = cell_pos
                    self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                return None

        return None

    def reset_editor(self):
        self.model.map.reset()
        self.selected_cell = None
        self.selected_road_type = None
        self.inventory.selected_type = None

        self.model.player_road_list = NormalRoadListModel(10, 6, 3, 1)
        for rt in self.inventory.editable_types:
            self.inventory.counts[rt] = str(self.model.player_road_list.get_road_num(rt))

    def clear_selection(self):
        self.selected_cell = None
        self.selected_road_type = None
        self.inventory.selected_type = None

    def remove_selected(self):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.model.map.set_cell(r, c, None)
            self.selected_cell = None

    def update(self):
        pass

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((240, 248, 255))

        self.back_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.save_btn.draw(self.screen)
        self.clear_btn.draw(self.screen)
        self.remove_btn.draw(self.screen)

        self.map_view.draw()

        self.inventory.draw()

        for r in range(5):
            pg.draw.line(self.screen, (100, 100, 100),
                         (self.map_view.x, self.map_view.y + r * 120),
                         (self.map_view.x + 4 * 120, self.map_view.y + r * 120), 1)
        for c in range(5):
            pg.draw.line(self.screen, (100, 100, 100),
                         (self.map_view.x + c * 120, self.map_view.y),
                         (self.map_view.x + c * 120, self.map_view.y + 4 * 120), 1)

        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c * 120, self.map_view.y + r * 120, 120, 120)
            pg.draw.rect(self.screen, (255, 255, 0), rect, 3)

        if self.selected_road_type is not None:
            for rect, rt in self.inventory.buttons:
                if rt == self.inventory.selected_type:
                    pg.draw.rect(self.screen, (255, 0, 0), rect, 3)

        if self.info_dialog.visible:
            self.info_dialog.draw(self.screen)