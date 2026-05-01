import pygame
from typing import Tuple, Optional, Callable

pygame.font.init()
FONT_MEDIUM = pygame.font.Font(None, 26)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_NORMAL = (60, 120, 200)
BUTTON_HOVER = (90, 150, 230)

class ButtonView:
    """
    Universal clickable button with hover effect and click callback.
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 text: str,
                 callback: Optional[Callable[[], None]] = None) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, screen: pygame.Surface) -> None:
        """Draw button with normal or hover color."""
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_NORMAL

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)

        text_surf = FONT_MEDIUM.render(self.text, True, WHITE)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        """Trigger callback if button is clicked."""
        if self.rect.collidepoint(mouse_pos) and self.callback:
            self.callback()