import pygame
from typing import Optional, Tuple
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 40)
BG = (235, 245, 255)

class LevelSelectView:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.buttons = []
        self.buttons.append(ButtonView(120, 180, 120, 50, "Level 1"))
        self.buttons.append(ButtonView(280, 180, 120, 50, "Level 2"))
        self.buttons.append(ButtonView(440, 180, 120, 50, "Level 3"))
        self.buttons.append(ButtonView(600, 180, 120, 50, "Level 4"))
        self.buttons.append(ButtonView(w//2 - 60, 350, 120, 50, "Back"))

    def draw(self, screen):
        screen.fill(BG)
        title = FONT_TITLE.render("Select Level", True, (20,40,80))
        screen.blit(title, title.get_rect(center=(self.w//2, 100)))
        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        return None