import os
import pygame
from typing import Optional, Tuple
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 40)
FONT_SUBTITLE = pygame.font.Font(None, 28)
FONT_BUTTON = pygame.font.Font(None, 24)
BG = (235, 245, 255)
BUILTIN_BG = (255, 255, 180)
CUSTOM_BG = (230, 210, 250)
BORDER_COLOR = (80, 80, 80)

class LevelSelectView:
    def __init__(self, w, h, saves_path="models/levels/"):
        self.w = w
        self.h = h
        self.saves_path = saves_path

        self.back_button = ButtonView(w//2 - 60, h - 80, 120, 50, "Back",
                                      normal_color=(120, 120, 120),
                                      hover_color=(160, 160, 160))

        self.builtin_buttons = []
        btn_w, btn_h = 150, 50
        margin_x = (w - 2 * btn_w) // 3
        start_y = 150
        for i in range(4):
            row = i // 2
            col = i % 2
            x = margin_x + col * (btn_w + margin_x)
            y = start_y + row * (btn_h + 15)
            btn = ButtonView(x, y, btn_w, btn_h, f"Level {i+1}",
                             normal_color=(70, 130, 200),
                             hover_color=(100, 160, 230))
            self.builtin_buttons.append(btn)

        self.custom_groups = []
        self._load_custom_levels()

        self.background = None
        try:
            path = os.path.join("view", "assets", "backgrounds", "level_select.jpg")
            print("[LevelSelect] Loading:", path)
            img = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(img, (self.w, self.h))
            print("[LevelSelect] Success!")
        except Exception as e:
            print("[LevelSelect] Background not loaded:", e)

    def _load_custom_levels(self):
        self.custom_groups.clear()
        if not os.path.exists(self.saves_path):
            os.makedirs(self.saves_path, exist_ok=True)
            return

        files = [f for f in os.listdir(self.saves_path) if f.startswith('level') and f.endswith('.txt')]
        nums = []
        for f in files:
            try:
                num = int(f.replace('level', '').replace('.txt', ''))
                nums.append(num)
            except ValueError:
                continue
        nums = sorted(nums)[:12]

        small_btn_w, small_btn_h = 100, 35
        spacing = 8
        total_width = small_btn_w * 3 + spacing * 2
        start_x = (self.w - total_width) // 2
        start_y = 330
        row_h = 45

        for i, num in enumerate(nums):
            x = start_x
            y = start_y + i * row_h
            play_btn = ButtonView(x, y, small_btn_w, small_btn_h, f"Play {num}",
                                  normal_color=(80, 180, 80),
                                  hover_color=(110, 210, 110))
            edit_btn = ButtonView(x + small_btn_w + spacing, y, small_btn_w, small_btn_h, "Edit",
                                  normal_color=(255, 140, 0),
                                  hover_color=(255, 165, 40))
            del_btn = ButtonView(x + 2*(small_btn_w + spacing), y, small_btn_w, small_btn_h, "Del",
                                 normal_color=(200, 70, 70),
                                 hover_color=(230, 100, 100))
            self.custom_groups.append((play_btn, edit_btn, del_btn, num))

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG)

        title = FONT_TITLE.render("Select Level", True, (20, 40, 80))
        screen.blit(title, title.get_rect(center=(self.w//2, 60)))

        builtin_rect = pygame.Rect(20, 110, self.w - 40, 160)
        pygame.draw.rect(screen, BUILTIN_BG, builtin_rect, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, builtin_rect, 2, border_radius=12)

        subtitle = FONT_SUBTITLE.render("Built-in Levels", True, (40, 40, 80))
        screen.blit(subtitle, (40, 120))

        for btn in self.builtin_buttons:
            btn.draw(screen)

        custom_y_start = 290
        custom_height = min(40 + len(self.custom_groups) * 45, 300)
        custom_rect = pygame.Rect(20, custom_y_start, self.w - 40, custom_height)
        if self.custom_groups:
            pygame.draw.rect(screen, CUSTOM_BG, custom_rect, border_radius=12)
            pygame.draw.rect(screen, BORDER_COLOR, custom_rect, 2, border_radius=12)

        custom_subtitle = FONT_SUBTITLE.render("Custom Levels", True, (40, 40, 80))
        screen.blit(custom_subtitle, (40, custom_y_start + 5))

        for play_btn, edit_btn, del_btn, _ in self.custom_groups:
            play_btn.draw(screen)
            edit_btn.draw(screen)
            del_btn.draw(screen)

        self.back_button.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for i, btn in enumerate(self.builtin_buttons):
            if btn.rect.collidepoint(mouse_pos):
                return f"play_builtin_{i+1}"

        for play_btn, edit_btn, del_btn, level_id in self.custom_groups:
            if play_btn.rect.collidepoint(mouse_pos):
                return f"play_custom_{level_id}"
            if edit_btn.rect.collidepoint(mouse_pos):
                return f"edit_custom_{level_id}"
            if del_btn.rect.collidepoint(mouse_pos):
                return f"delete_custom_{level_id}"

        if self.back_button.rect.collidepoint(mouse_pos):
            return "back_to_menu"
        return None

    def refresh_levels(self):
        self._load_custom_levels()