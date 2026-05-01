import pygame
import os
from typing import Optional, Tuple, List
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 40)
FONT_BUTTON = pygame.font.Font(None, 28)
BG = (235, 245, 255)

class LevelSelectView:
    def __init__(self, w, h, saves_path="models/levels/"):
        self.w = w
        self.h = h
        self.saves_path = saves_path
        self.level_buttons = []
        self.back_button = ButtonView(w//2 - 60, h - 100, 120, 50, "Back")
        
        # Load level files and create buttons
        self.load_level_files()
        
    def load_level_files(self):
        """Scan the saves_path folder and create buttons for each level file"""
        self.level_buttons = []
        
        try:
            # Get all level files in the folder
            if os.path.exists(self.saves_path):
                files = [f for f in os.listdir(self.saves_path) if f.startswith('level') and f.endswith('.txt')]
                
                # Extract level numbers and sort them
                level_numbers = []
                for file in files:
                    try:
                        # Extract level number from filename (e.g., level1.txt -> 1)
                        level_num = int(file.replace('level', '').replace('.txt', ''))
                        level_numbers.append(level_num)
                    except ValueError:
                        continue
                
                level_numbers.sort()
                
                # Limit to maximum 12 levels (4 columns × 3 rows)
                max_levels = 12
                level_numbers = level_numbers[:max_levels]
                
                # Calculate button dimensions and spacing
                button_width = 120
                button_height = 50
                horizontal_margin = (self.w - (4 * button_width + 3 * 20)) // 2
                vertical_start = 180
                vertical_spacing = 80
                
                # Create buttons in grid layout (max 4 per row, max 3 rows)
                for i, level_num in enumerate(level_numbers):
                    row = i // 4  # 0, 1, 2 for rows
                    col = i % 4   # 0, 1, 2, 3 for columns
                    
                    # Calculate position
                    x = horizontal_margin + col * (button_width + 20)
                    y = vertical_start + row * vertical_spacing
                    
                    button_text = f"Level {level_num}"
                    button = ButtonView(x, y, button_width, button_height, button_text)
                    self.level_buttons.append(button)
            else:
                # If folder doesn't exist, create it and show message
                os.makedirs(self.saves_path, exist_ok=True)
                print(f"Created level folder at: {self.saves_path}")
                
        except Exception as e:
            print(f"Error loading level files: {e}")
            # Create some default buttons for testing
            self.create_default_buttons()
    
    def create_default_buttons(self):
        """Create default buttons if no levels are found"""
        button_width = 120
        button_height = 50
        horizontal_margin = (self.w - (4 * button_width + 3 * 20)) // 2
        vertical_start = 180
        vertical_spacing = 80
        
        default_levels = [1, 2, 3]
        for i, level_num in enumerate(default_levels):
            row = i // 4
            col = i % 4
            x = horizontal_margin + col * (button_width + 20)
            y = vertical_start + row * vertical_spacing
            button_text = f"Level {level_num}"
            button = ButtonView(x, y, button_width, button_height, button_text)
            self.level_buttons.append(button)
    
    def draw(self, screen):
        screen.fill(BG)
        
        # Draw title
        title = FONT_TITLE.render("Select Level", True, (20, 40, 80))
        screen.blit(title, title.get_rect(center=(self.w//2, 100)))
        
        # Draw level buttons
        for btn in self.level_buttons:
            btn.draw(screen)
        
        # Draw back button
        self.back_button.draw(screen)
        
        # Draw info text if no levels found
        if not self.level_buttons:
            info_text = FONT_BUTTON.render("No levels found. Create levels in the editor!", True, (150, 150, 150))
            screen.blit(info_text, info_text.get_rect(center=(self.w//2, self.h//2)))
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        # Check level buttons first
        for btn in self.level_buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        
        # Check back button
        if self.back_button.rect.collidepoint(mouse_pos):
            return self.back_button.text
        
        return None
    
    def refresh_levels(self):
        """Refresh the level list (useful after creating new levels)"""
        self.load_level_files()