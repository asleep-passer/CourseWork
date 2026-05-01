import pygame as pg
from typing import Tuple, Optional, List
from models.roadlist import NormalRoadListModel
from view.map_view import MapView
from view.button_view import ButtonView
from view.dialog_view import DialogView
from models.gamemodel import GameLevelModel, GameLevelController
from models.Road import RoadType
from models.roadcell import RoadCellModel
from models.map import MapModel
import config

class EditorInventoryView:
    """
    Special inventory view for level editor that allows editing road counts
    """
    def __init__(self, x, y, screen, model):
        self.x = x
        self.y = y
        self.screen = screen
        self.model = model
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 20)
        
        # Editor-specific road types including special tiles
        self.editor_types = [
            RoadType.OBSTACLE_ROAD,
            RoadType.START_ROAD, 
            RoadType.END_ROAD
        ]
        
        # Regular road types that can have their counts edited
        self.editable_types = [
            RoadType.STRAIGHT_ROAD,
            RoadType.BEND_ROAD,
            RoadType.T_SHAPED_ROAD,
            RoadType.CROSS_ROAD
        ]
        
        self.buttons = []
        self.count_inputs = {}
        self.selected_type = None
        self.active_input = None  # Track which input field is currently active
        self._create_buttons()
        
    def _create_buttons(self):
        # Create buttons for special tiles (obstacle, start, end)
        spacing = 50
        for i, rt in enumerate(self.editor_types):
            btn_rect = pg.Rect(self.x, self.y + i * spacing, 180, 40)
            self.buttons.append((btn_rect, rt))
        
        # Create count inputs for editable road types
        input_y = self.y + len(self.editor_types) * spacing + 30
        for i, rt in enumerate(self.editable_types):
            # Label for road type
            label_rect = pg.Rect(self.x, input_y + i * 45, 120, 30)
            self.buttons.append((label_rect, rt))
            
            # Input field for count
            input_rect = pg.Rect(self.x + 130, input_y + i * 45, 80, 30)
            self.count_inputs[rt] = {
                'rect': input_rect,
                'text': str(self.model.player_road_list.get_road_num(rt)),
                'active': False
            }
    
    def handle_click(self, pos):
        # Check if clicking on special tile buttons
        for rect, rt in self.buttons:
            if rect.collidepoint(pos):
                if rt in self.editor_types:
                    self.selected_type = rt
                    # Deactivate all inputs when selecting a tile type
                    for data in self.count_inputs.values():
                        data['active'] = False
                    self.active_input = None
                    return rt
                elif rt in self.editable_types:
                    # Clicking on road type label does nothing special
                    continue
        
        # Check count input fields
        for rt, data in self.count_inputs.items():
            if data['rect'].collidepoint(pos):
                # Activate this input field
                data['active'] = True
                self.active_input = rt
                # Deactivate all other inputs
                for other_rt, other_data in self.count_inputs.items():
                    if other_rt != rt:
                        other_data['active'] = False
                return None
        
        # Clicked outside any input field - deactivate all
        for data in self.count_inputs.values():
            data['active'] = False
        self.active_input = None
        return None
    
    def handle_key(self, event):
        if self.active_input is None:
            return
            
        data = self.count_inputs[self.active_input]
        if event.key == pg.K_BACKSPACE:
            data['text'] = data['text'][:-1]
        elif event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, 
                         pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
            # Limit to reasonable numbers (max 99)
            if len(data['text']) < 2 or (len(data['text']) == 2 and data['text'][0] == '0'):
                data['text'] += event.unicode
    
    def apply_counts(self):
        """Apply the input counts to the model"""
        for rt in self.editable_types:
            try:
                count = int(self.count_inputs[rt]['text'])
                count = max(0, min(99, count))  # Clamp between 0 and 99
                self.count_inputs[rt]['text'] = str(count)
                self.model.player_road_list.set_road_num(rt, count)
            except ValueError:
                # If invalid input, reset to current value
                current_count = self.model.player_road_list.get_road_num(rt)
                self.count_inputs[rt]['text'] = str(current_count)
    
    def get_road_type_at(self, pos):
        for rect, rt in self.buttons:
            if rect.collidepoint(pos):
                return rt
        return None
    
    def draw(self):
        # Draw title
        title = self.font.render("Editor Tools", True, (0, 0, 0))
        self.screen.blit(title, (self.x, self.y - 40))
        
        # Draw special tile buttons
        for rect, rt in self.buttons:
            if rt in self.editor_types:
                color = (100, 200, 100) if rt == self.selected_type else (200, 200, 200)
                pg.draw.rect(self.screen, color, rect)
                pg.draw.rect(self.screen, (0, 0, 0), rect, 2)
                
                text = self.small_font.render(rt.name.replace("_ROAD", ""), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
        
        # Draw editable road counts section title
        section_title = self.font.render("Available Roads", True, (0, 0, 0))
        section_y = self.y + len(self.editor_types) * 50 + 10
        self.screen.blit(section_title, (self.x, section_y))
        
        # Draw road type labels and count inputs
        for i, rt in enumerate(self.editable_types):
            label_y = section_y + 30 + i * 45
            
            # Road type label
            label_text = self.small_font.render(rt.name.replace("_ROAD", ""), True, (0, 0, 0))
            self.screen.blit(label_text, (self.x, label_y))
            
            # Count input field
            data = self.count_inputs[rt]
            color = (255, 255, 200) if data['active'] else (240, 240, 240)
            pg.draw.rect(self.screen, color, data['rect'])
            pg.draw.rect(self.screen, (0, 0, 0), data['rect'], 2)
            
            # Display current count
            text_surface = self.small_font.render(data['text'], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=data['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
            # Draw label "Count:" next to input field
            count_label = self.small_font.render("Count:", True, (0, 0, 0))
            self.screen.blit(count_label, (data['rect'].x - 60, data['rect'].y + 5))

class LevelEditorView:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 18)
        
        w, h = screen.get_size()
        map_x = 50
        map_y = 130
        
        # Create empty map model for editing
        self.model = GameLevelModel(level_id=999)  # Use high ID for editor
        self.model.map = MapModel(rows=4, cols=4)  # 4x4 grid for editor
        self.model.player_road_list = NormalRoadListModel(10, 6, 3, 1)  # Default counts
        
        # Map view
        self.map_view = MapView(self.model.map, map_x, map_y, 120, screen)
        
        # Editor inventory with special tools
        inventory_x = map_x + 4*120 + 40
        inventory_y = map_y
        self.inventory = EditorInventoryView(inventory_x, inventory_y, screen, self.model)
        
        # Editor buttons
        self.back_btn = ButtonView(20, 20, 90, 40, "Back")
        self.reset_btn = ButtonView(130, 20, 90, 40, "Reset")
        self.save_btn = ButtonView(240, 20, 90, 40, "Save")
        self.clear_btn = ButtonView(350, 20, 90, 40, "Clear")
        self.remove_btn = ButtonView(460, 20, 110, 40, "Remove")
        
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.selected_road_type: Optional[RoadType] = None
        
        self.info_dialog = DialogView(250, 200, 350, 150)
        self.info_dialog.add_button(
            ButtonView(400, 290, 80, 35, "OK", callback=self.info_dialog.hide)
        )
        
        self.hint_cells = []
        self.hint_timer = 0
        
    def show_info(self, msg: str):
        self.info_dialog.set_message(msg)
        self.info_dialog.show()
    
    def get_next_level_id(self):
        """Find the next available level ID"""
        level_id = 1
        while True:
            file_path = config.saves_path + f"level{level_id}.txt"
            try:
                with open(file_path, 'r'):
                    level_id += 1
            except FileNotFoundError:
                break
        return level_id
    
    def save_level(self):
        """Save the current level to a file"""
        # Apply current counts before saving
        self.inventory.apply_counts()
        
        # Validate level has at least one start and one end
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
            self.show_info("Error: Level must have at least one start and one end point!")
            return False
        
        # Get next available level ID
        level_id = self.get_next_level_id()
        file_path = config.saves_path + f"level{level_id}.txt"
        
        try:
            with open(file_path, 'w') as f:
                # Write dimensions
                f.write("4 4\n")
                
                # Write road types matrix
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
                                row.append("7")  # Empty space
                        else:
                            row.append("7")  # Empty space
                    road_types.append(" ".join(row))
                f.write("\n".join(road_types) + "\n")
                
                # Write locked status matrix (all unlocked in editor)
                locked_status = ["0 0 0 0"] * 4
                f.write("\n".join(locked_status) + "\n")
                
                # Write rotation status matrix
                rotation_status = []
                for r in range(4):
                    row = []
                    for c in range(4):
                        cell = self.model.map.get_cell(r, c)
                        if cell:
                            # Get rotation count (0-3)
                            rotation = 0
                            row.append(str(rotation))
                        else:
                            row.append("0")
                    rotation_status.append(" ".join(row))
                f.write("\n".join(rotation_status) + "\n")
                
                # Write available roads counts
                straight_count = self.model.player_road_list.get_road_num(RoadType.STRAIGHT_ROAD)
                bend_count = self.model.player_road_list.get_road_num(RoadType.BEND_ROAD)
                t_count = self.model.player_road_list.get_road_num(RoadType.T_SHAPED_ROAD)
                cross_count = self.model.player_road_list.get_road_num(RoadType.CROSS_ROAD)
                f.write(f"{straight_count} {bend_count} {t_count} {cross_count}")
            
            self.show_info(f"Level saved successfully as level{level_id}.txt!")
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
            
            # Handle text input for count fields
            self.inventory.handle_key(event)
            return None
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            if event.button == 1:
                # Check editor buttons first
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
                
                # Check inventory
                road_type = self.inventory.handle_click(pos)
                if road_type is not None:
                    self.selected_road_type = road_type
                    return None
                
                # Check map cells
                cell_pos = self.map_view.check_click(pos)
                if cell_pos is not None:
                    r, c = cell_pos
                    self.selected_cell = (r, c)
                    
                    if self.selected_road_type is not None:
                        # Place the selected road type
                        if self.selected_road_type in [RoadType.START_ROAD, RoadType.END_ROAD, RoadType.OBSTACLE_ROAD]:
                            # Special tiles replace existing cells
                            new_cell = RoadCellModel(r, c, self.selected_road_type)
                            self.model.map.set_cell(r, c, new_cell)
                        else:
                            # Regular roads
                            if self.model.map.get_cell(r, c) is None:
                                new_cell = RoadCellModel(r, c, self.selected_road_type)
                                self.model.map.set_cell(r, c, new_cell)
                    return None
                
                # Deselect everything if clicked outside
                self.selected_road_type = None
            
            if event.button == 3:  # Right click to remove cell
                cell_pos = self.map_view.check_click(pos)
                if cell_pos:
                    r, c = cell_pos
                    self.map_view.cell_views[r][c].trigger_rotate_animation(500)
                return None
        
        return None
    
    def reset_editor(self):
        """Reset the editor to empty state"""
        self.model.map.reset()
        self.selected_cell = None
        self.selected_road_type = None
        self.inventory.selected_type = None
        
        # Reset count inputs to default values
        self.model.player_road_list = NormalRoadListModel(10, 6, 3, 1)
        for rt in self.inventory.editable_types:
            self.inventory.count_inputs[rt]['text'] = str(self.model.player_road_list.get_road_num(rt))
    
    def clear_selection(self):
        """Clear current selections"""
        self.selected_cell = None
        self.selected_road_type = None
        self.inventory.selected_type = None

    def remove_selected(self):
        if self.selected_cell is None: return
        r, c = self.selected_cell
        cell = self.model.map.get_cell(r, c)
        if cell is not None:
            self.model.map.set_cell(r, c, None)
            self.selected_cell = None

    def update(self):
        pass  # No game logic needed for editor
    
    def draw(self):
        self.screen.fill((240, 248, 255))  # Light blue background for editor
        
        # Draw title
        title = self.font.render("Level Editor", True, (0, 0, 100))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 20))
        
        # Draw editor buttons
        self.back_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.save_btn.draw(self.screen)
        self.clear_btn.draw(self.screen)
        self.remove_btn.draw(self.screen)
        
        # Draw map
        self.map_view.draw()
        
        # Draw inventory
        self.inventory.draw()
        
        # Draw grid overlay
        for r in range(5):
            pg.draw.line(self.screen, (100, 100, 100), 
                        (self.map_view.x, self.map_view.y + r * 120),
                        (self.map_view.x + 4 * 120, self.map_view.y + r * 120), 1)
        for c in range(5):
            pg.draw.line(self.screen, (100, 100, 100),
                        (self.map_view.x + c * 120, self.map_view.y),
                        (self.map_view.x + c * 120, self.map_view.y + 4 * 120), 1)
        
        # Highlight selected cell
        if self.selected_cell is not None:
            r, c = self.selected_cell
            rect = pg.Rect(self.map_view.x + c * 120, self.map_view.y + r * 120, 120, 120)
            pg.draw.rect(self.screen, (255, 255, 0), rect, 3)  # Yellow highlight
        
        # Highlight selected tool
        if self.selected_road_type is not None:
            for rect, rt in self.inventory.buttons:
                if rt == self.selected_road_type:
                    pg.draw.rect(self.screen, (255, 0, 0), rect, 3)  # Red highlight
        
        # Draw info dialog if visible
        if self.info_dialog.visible:
            self.info_dialog.draw(self.screen)