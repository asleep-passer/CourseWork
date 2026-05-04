import pygame
import os
from typing import Optional, Tuple
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 40)
BG = (235, 245, 255)

class DifficultySelectView:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.buttons = []
        cx = w // 2 - 90

        self.buttons.append(ButtonView(cx, 180, 180, 50, "Easy",
                                       normal_color=(100, 200, 100),
                                       hover_color=(130, 230, 130)))
        self.buttons.append(ButtonView(cx, 250, 180, 50, "Medium",
                                       normal_color=(255, 165, 0),
                                       hover_color=(255, 190, 60)))
        self.buttons.append(ButtonView(cx, 320, 180, 50, "Hard",
                                       normal_color=(220, 80, 80),
                                       hover_color=(250, 120, 120)))
        self.buttons.append(ButtonView(w//2 - 60, 400, 120, 50, "Back"))

        self.background = None
        try:
            path = os.path.join("view", "assets", "backgrounds", "difficulty_select.png")
            print("[DifficultySelect] Loading:", path)
            img = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(img, (self.w, self.h))
            print("[DifficultySelect] Success!")
        except Exception as e:
            print("[DifficultySelect] Background not loaded:", e)

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG)
        title = FONT_TITLE.render("Select Difficulty", True, (20, 40, 80))
        screen.blit(title, title.get_rect(center=(self.w//2, 100)))
        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        return None