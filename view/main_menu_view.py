"""Main menu UI view for the game.
Displays the main menu with background image and navigation buttons.
"""
import pygame
import os
from typing import Optional, Tuple
from view.button_view import ButtonView

pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 50)
BACKGROUND_COLOR = (235, 245, 255)

class MainMenuView:
    """Main menu interface that provides game navigation options.
    Contains Start Game, Level Editor, and Quit buttons.
    """
    def __init__(self, w: int, h: int):
        """Initialize main menu with screen size and UI elements.

        Args:
            w: Screen width
            h: Screen height
        """
        self.w = w
        self.h = h
        self.buttons = []

        center_x = w // 2 - 100
        self.buttons.append(ButtonView(center_x, 250, 200, 50, "Start Game",
                                       normal_color=(100, 200, 100),
                                       hover_color=(130, 230, 130)))
        self.buttons.append(ButtonView(center_x, 320, 200, 50, "Level Editor",
                                       normal_color=(100, 150, 220),
                                       hover_color=(130, 180, 250)))
        self.buttons.append(ButtonView(center_x, 390, 200, 50, "Quit",
                                       normal_color=(220, 80, 80),
                                       hover_color=(250, 120, 120)))

        self.background = None
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_path, "view", "assets", "backgrounds", "main_menu.jpg")
            img = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(img, (self.w, self.h))
        except Exception as e:
            print(f"[MainMenu] Background not loaded: {e}")

    def draw(self, screen: pygame.Surface) -> None:
        """Render background and all menu buttons to the screen.

        Args:
            screen: Pygame surface to draw on
        """
        self.w, self.h = screen.get_size()
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)

   

        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Detect mouse clicks on menu buttons and return the action.

        Args:
            mouse_pos: Mouse (x, y) coordinates

        Returns:
            Button text (action name) or None if no button was clicked
        """
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        return None