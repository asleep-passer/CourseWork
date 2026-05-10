"""Dialog UI component for popup messages and interactive buttons.
Provides a semi-transparent overlay dialog with text and clickable buttons.
"""
import pygame
from typing import List
from view.button_view import ButtonView

pygame.font.init()
FONT_MAIN = pygame.font.Font(None, 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_OVERLAY = (20, 20, 20, 160)


class DialogView:
    """Popup dialog window with text message and interactive buttons.
    Handles visibility, rendering, overlay, text wrapping, and button click events.
    """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """Initialize a dialog box with position and dimensions.

        Args:
            x: X coordinate of the dialog's top-left corner
            y: Y coordinate of the dialog's top-left corner
            width: Dialog width in pixels
            height: Dialog height in pixels
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.message = ""
        self.buttons: List[ButtonView] = []

    def set_message(self, msg: str) -> None:
        """Set the text message to display in the dialog.

        Args:
            msg: Text string to show (supports line breaks)
        """
        self.message = msg

    def add_button(self, btn: ButtonView) -> None:
        """Add a clickable button to the dialog.

        Args:
            btn: ButtonView instance to include in the dialog
        """
        self.buttons.append(btn)

    def show(self) -> None:
        """Show the dialog and enable interaction."""
        self.visible = True

    def hide(self) -> None:
        """Hide the dialog and disable interaction."""
        self.visible = False

    def draw(self, screen: pygame.Surface) -> None:
        """Render the dialog overlay, background, text, and buttons.

        Args:
            screen: Pygame surface to draw the dialog on
        """
        if not self.visible:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(GRAY_OVERLAY)
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)

        lines = self.message.split('\n')
        line_height = FONT_MAIN.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = self.rect.top + 30

        if total_text_height > self.rect.height - 60:
            start_y = self.rect.top + 10

        for i, line in enumerate(lines):
            text_surf = FONT_MAIN.render(line, True, BLACK)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, start_y + i * line_height))
            screen.blit(text_surf, text_rect)

        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, mouse_pos):
        """Forward mouse click events to dialog buttons if visible.

        Args:
            mouse_pos: (x, y) coordinates of the mouse click
        """
        if not self.visible:
            return
        for btn in self.buttons:
            btn.handle_click(mouse_pos)