"""Button UI component module
Provides a reusable, styled button with hover effect, click handling, and custom font rendering.
"""

import pygame
import os
from typing import Tuple, Optional, Callable

pygame.font.init()



def get_font(size):
    """Load and return a custom font from assets, or fallback to default font.

    Args:
        size: Font size in pixels

    Returns:
        pygame.font.Font: Loaded font object
    """
    path = "view/assets/Font/LilitaOne-Regular.ttf"
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    return pygame.font.Font(None, size + 6)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


DEFAULT_NORMAL = (255, 215, 0, 140) 
DEFAULT_HOVER = (147, 112, 219, 180)  


class ButtonView:
    """Reusable interactive button component with styling, hover effects, and click callbacks.
    Supports custom colors, text, positioning, and click event handling.
    """
    def __init__(self,
                 x: int, y: int, width: int, height: int,
                 text: str,
                 callback: Optional[Callable[[], None]] = None,
                 normal_color: Optional[Tuple[int, ...]] = None,
                 hover_color: Optional[Tuple[int, ...]] = None,
                 font_size: int = 18) -> None:
        """Initialize a new button with position, size, text, and visual styles.

        Args:
            x: X coordinate of the button's top-left corner
            y: Y coordinate of the button's top-left corner
            width: Button width in pixels
            height: Button height in pixels
            text: Text displayed on the button
            callback: Function to execute when the button is clicked (optional)
            normal_color: Background color in normal state (optional)
            hover_color: Background color when mouse hovers (optional)
            font_size: Text font size (default: 18)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.normal_color = normal_color if normal_color is not None else DEFAULT_NORMAL
        self.hover_color = hover_color if hover_color is not None else DEFAULT_HOVER
        self.font = get_font(font_size)

    def draw(self, screen: pygame.Surface) -> None:
        """Render the button with shadow, hover effect, border, and text to the screen.

        Args:
            screen: Pygame surface to draw the button on
        """
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.normal_color

        
        if len(color) == 3:
            color = (*color, 180 if is_hover else 140)

  
        draw_rect = self.rect.copy()
        if is_hover:
            draw_rect.y -= 2

     
        shadow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    
        pygame.draw.rect(shadow_surf, (40, 40, 40, 80), shadow_surf.get_rect(), border_radius=8)
        screen.blit(shadow_surf, (self.rect.x, self.rect.y + 4))

     
        btn_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
       
        pygame.draw.rect(btn_surf, color, btn_surf.get_rect(), border_radius=8)
      
        pygame.draw.rect(btn_surf, (255, 255, 255, 200), btn_surf.get_rect(), 2, border_radius=8)

    
        screen.blit(btn_surf, draw_rect.topleft)

       
        text_shadow = self.font.render(self.text, True, (0, 0, 0))
        text_shadow.set_alpha(100)  
        shadow_rect = text_shadow.get_rect(center=(draw_rect.centerx + 1, draw_rect.centery + 1))
        screen.blit(text_shadow, shadow_rect)

       
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        """Trigger the button's callback if clicked within its bounds.

        Args:
            mouse_pos: Tuple of (x, y) mouse click coordinates
        """
        if self.rect.collidepoint(mouse_pos) and self.callback:
            self.callback()