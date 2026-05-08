import os
import pygame
from typing import Optional, Tuple
from view.button_view import ButtonView

# --- 基础初始化 ---
pygame.font.init()

# 获取当前文件所在目录，确保路径在任何环境下都正确
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join("view", "assets", "fonts", "LilitaOne-Regular.ttf")

# --- 字体加载逻辑 ---
try:
    # 尝试加载自定义字体
    FONT_TITLE = pygame.font.Font(FONT_PATH, 42)
    FONT_SUBTITLE = pygame.font.Font(FONT_PATH, 32) # 稍微加大一点
    FONT_BUTTON = pygame.font.Font(FONT_PATH, 24)
    print(f"[LevelSelect] Successfully loaded font: {FONT_PATH}")
except Exception as e:
    print(f"[LevelSelect] Font load failed: {e}. Using default font.")
    FONT_TITLE = pygame.font.Font(None, 40)
    FONT_SUBTITLE = pygame.font.Font(None, 28)
    FONT_BUTTON = pygame.font.Font(None, 24)

# --- 样式常量 ---
BG_COLOR = (235, 245, 255)
TEXT_COLOR = (70, 45, 30)  # 温馨的深咖啡色，更配田园风
BUILTIN_BG = (255, 255, 180, 100)  # 半透明黄色
CUSTOM_BG = (230, 210, 250, 100)   # 半透明紫色
BORDER_COLOR = (255, 255, 255, 180) # 半透明白色边框


class LevelSelectView:
    def __init__(self, w, h, saves_path="models/levels/"):
        self.w = w
        self.h = h
        self.saves_path = saves_path

        # 返回按钮
        self.back_button = ButtonView(w // 2 - 60, h - 80, 120, 50, "Back",
                                      normal_color=(120, 120, 120),
                                      hover_color=(160, 160, 160))

        # 加载内置关卡按钮
        self.builtin_buttons = []
        btn_w, btn_h = 150, 50
        margin_x = (w - 2 * btn_w) // 3
        start_y = 200
        for i in range(4):
            row = i // 2
            col = i % 2
            x = margin_x + col * (btn_w + margin_x)
            y = start_y + row * (btn_h + 15)
            # 注意：如果想让按钮也用新字体，需要在 ButtonView 类里支持或修改
            btn = ButtonView(x, y, btn_w, btn_h, f"Level {i + 1}",
                             normal_color=(70, 130, 200),
                             hover_color=(100, 160, 230))
            self.builtin_buttons.append(btn)

        self.custom_groups = []
        self._load_custom_levels()

        # 背景图加载
        self.background = None
        try:
            path = os.path.join("view", "assets", "backgrounds", "level_select.jpg")
            img = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(img, (self.w, self.h))
        except Exception as e:
            print("[LevelSelect] Background load failed:", e)

    def _load_custom_levels(self):
        self.custom_groups.clear()
        if not os.path.exists(self.saves_path):
            os.makedirs(self.saves_path, exist_ok=True)
            return

        files = [f for f in os.listdir(self.saves_path) if f.startswith('level') and f.endswith('.txt')]
        nums = sorted([int(f[5:-4]) for f in files if f[5:-4].isdigit()])[:12]

        small_btn_w, small_btn_h = 100, 35
        spacing = 8
        total_width = small_btn_w * 3 + spacing * 2
        start_x = (self.w - total_width) // 2
        start_y = 380
        row_h = 45

        for i, num in enumerate(nums):
            x = start_x
            y = start_y + i * row_h
            play_btn = ButtonView(x, y, small_btn_w, small_btn_h, f"Play {num}",
                                  normal_color=(80, 180, 80), hover_color=(110, 210, 110))
            edit_btn = ButtonView(x + small_btn_w + spacing, y, small_btn_w, small_btn_h, "Edit",
                                  normal_color=(255, 140, 0), hover_color=(255, 165, 40))
            del_btn = ButtonView(x + 2 * (small_btn_w + spacing), y, small_btn_w, small_btn_h, "Del",
                                 normal_color=(200, 70, 70), hover_color=(230, 100, 100))
            self.custom_groups.append((play_btn, edit_btn, del_btn, num))

    def draw(self, screen):
        # 1. 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # 2. 绘制 Built-in Levels 区域
        builtin_rect = pygame.Rect(20, 150, self.w - 40, 180)
        builtin_surf = pygame.Surface((builtin_rect.width, builtin_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(builtin_surf, BUILTIN_BG, builtin_surf.get_rect(), border_radius=15)
        pygame.draw.rect(builtin_surf, BORDER_COLOR, builtin_surf.get_rect(), 2, border_radius=15)
        screen.blit(builtin_surf, builtin_rect.topleft)

        # 标题居中渲染 (使用加载后的 FONT_SUBTITLE)
        txt_builtin = FONT_SUBTITLE.render("Built-in Levels", True, TEXT_COLOR)
        rect_builtin = txt_builtin.get_rect(center=(self.w // 2, 175))
        screen.blit(txt_builtin, rect_builtin)

        for btn in self.builtin_buttons:
            btn.draw(screen)

        # 3. 绘制 Custom Levels 区域
        custom_y_start = 340
        if self.custom_groups:
            custom_height = min(50 + len(self.custom_groups) * 45, 220)
            custom_rect = pygame.Rect(20, custom_y_start, self.w - 40, custom_height)

            custom_surf = pygame.Surface((custom_rect.width, custom_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(custom_surf, CUSTOM_BG, custom_surf.get_rect(), border_radius=15)
            pygame.draw.rect(custom_surf, BORDER_COLOR, custom_surf.get_rect(), 2, border_radius=15)
            screen.blit(custom_surf, custom_rect.topleft)

            # 标题居中渲染
            txt_custom = FONT_SUBTITLE.render("Custom Levels", True, TEXT_COLOR)
            rect_custom = txt_custom.get_rect(center=(self.w // 2, custom_y_start + 25))
            screen.blit(txt_custom, rect_custom)

            for play_btn, edit_btn, del_btn, _ in self.custom_groups:
                play_btn.draw(screen)
                edit_btn.draw(screen)
                del_btn.draw(screen)

        # 4. 绘制返回按钮
        self.back_button.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for i, btn in enumerate(self.builtin_buttons):
            if btn.rect.collidepoint(mouse_pos):
                return f"play_builtin_{i + 1}"

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