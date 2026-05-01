import pygame
from typing import List
from view.button_view import ButtonView

pygame.font.init()
FONT_MAIN = pygame.font.Font(None, 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_OVERLAY = (20, 20, 20, 160)


class DialogView:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.message = ""
        self.buttons: List[ButtonView] = []

    def set_message(self, msg: str) -> None:
        self.message = msg

    def add_button(self, btn: ButtonView) -> None:
        self.buttons.append(btn)

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return

        # 半透明遮罩
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(GRAY_OVERLAY)
        screen.blit(overlay, (0, 0))

        # 对话框背景
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)

        # 多行文本绘制
        lines = self.message.split('\n')
        line_height = FONT_MAIN.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = self.rect.top + 30  # 上方留边距

        # 如果总高度超过对话框可用空间，可适当上移开始位置
        if total_text_height > self.rect.height - 60:
            start_y = self.rect.top + 10

        for i, line in enumerate(lines):
            text_surf = FONT_MAIN.render(line, True, BLACK)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, start_y + i * line_height))
            screen.blit(text_surf, text_rect)

        # 绘制按钮
        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos):
        if not self.visible:
            return
        for btn in self.buttons:
            btn.handle_click(mouse_pos)