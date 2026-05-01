import pygame
from typing import Optional, Tuple
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 50)
BG = (235, 245, 255)

class MainMenuView:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.buttons = []
        cx = w // 2 - 100
        self.buttons.append(ButtonView(cx, 250, 200, 50, "Start Game"))
        self.buttons.append(ButtonView(cx, 320, 200, 50, "Quit"))

    def draw(self, screen):
        screen.fill(BG)
        title = FONT_TITLE.render("Road Builder", True, (20, 40, 80))
        screen.blit(title, title.get_rect(center=(self.w//2, 120)))
        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        return None