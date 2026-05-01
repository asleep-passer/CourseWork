import pygame
from typing import Optional, Tuple
from view.button_view import ButtonView

# Initialize Pygame font module for text rendering
pygame.font.init()

# Default font for the main menu title
FONT_TITLE = pygame.font.Font(None, 50)
# Background color for the main menu screen
BACKGROUND_COLOR = (235, 245, 255)

class MainMenuView:
    """
    UI View for the game's main menu screen.
    Contains three buttons: Start Game, Level Editor, and Quit.
    """
    
    def __init__(self, w: int, h: int):
        """
        Initialize the main menu layout
        :param w: Initial window width
        :param h: Initial window height
        """
        self.w = w
        self.h = h
        self.buttons = []

        # Calculate center position for buttons
        center_x = w // 2 - 100
        # Add core menu buttons
        self.buttons.append(ButtonView(center_x, 250, 200, 50, "Start Game"))
        self.buttons.append(ButtonView(center_x, 320, 200, 50, "Level Editor"))
        self.buttons.append(ButtonView(center_x, 390, 200, 50, "Quit"))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the main menu on the screen
        :param screen: Pygame display surface
        """
        # Update window size for responsive display
        self.w, self.h = screen.get_size()
        screen.fill(BACKGROUND_COLOR)

        # Render and center the game title
        title = FONT_TITLE.render("Road Builder", True, (20, 40, 80))
        screen.blit(title, title.get_rect(center=(self.w // 2, 120)))

        # Draw all buttons
        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Process mouse click events on menu buttons
        :param mouse_pos: (x, y) coordinates of the mouse
        :return: The text of the clicked button, or None
        """
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.text
        return None