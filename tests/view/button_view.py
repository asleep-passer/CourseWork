import pygame
import os
from typing import Tuple, Optional, Callable

pygame.font.init()


# 动态加载字体逻辑
def get_font(size):
    path = "view/assets/Font/LilitaOne-Regular.ttf"
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    return pygame.font.Font(None, size + 6)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 改为带透明度的 RGBA 颜色，第四个值(Alpha)范围是 0~255，数字越小越透明
DEFAULT_NORMAL = (255, 215, 0, 140)  # 半透明黄色 (平时)
DEFAULT_HOVER = (147, 112, 219, 180)  # 半透明紫色 (悬停时，稍微不透明一点)


class ButtonView:
    def __init__(self,
                 x: int, y: int, width: int, height: int,
                 text: str,
                 callback: Optional[Callable[[], None]] = None,
                 normal_color: Optional[Tuple[int, ...]] = None,
                 hover_color: Optional[Tuple[int, ...]] = None,
                 font_size: int = 18) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.normal_color = normal_color if normal_color is not None else DEFAULT_NORMAL
        self.hover_color = hover_color if hover_color is not None else DEFAULT_HOVER
        self.font = get_font(font_size)

    def draw(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.normal_color

        # 安全机制：如果外部传进来的颜色没有写透明度（只有RGB三个值），自动帮它加上透明度
        if len(color) == 3:
            color = (*color, 180 if is_hover else 140)

        # 悬停时稍微把按钮向上提一点点，产生动态感
        draw_rect = self.rect.copy()
        if is_hover:
            draw_rect.y -= 2

        # ----------------------------------------------------
        # 1. 绘制半透明的底部阴影（厚度感）
        # 创建一个支持透明度的临时图层
        shadow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # 画半透明的黑色 (40, 40, 40, 80)
        pygame.draw.rect(shadow_surf, (40, 40, 40, 80), shadow_surf.get_rect(), border_radius=8)
        screen.blit(shadow_surf, (self.rect.x, self.rect.y + 4))

        # ----------------------------------------------------
        # 2. 绘制按钮主体（半透明黄色或紫色）
        btn_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        # 填充半透明颜色
        pygame.draw.rect(btn_surf, color, btn_surf.get_rect(), border_radius=8)
        # 绘制白色的玻璃边缘（200 是边缘透明度）
        pygame.draw.rect(btn_surf, (255, 255, 255, 200), btn_surf.get_rect(), 2, border_radius=8)

        # 将绘制好透明效果的图层贴到主屏幕上
        screen.blit(btn_surf, draw_rect.topleft)

        # ----------------------------------------------------
        # 3. 绘制文字
        # 由于背景变成了半透明，为了防止文字在亮色背景下看不清，增加一层淡淡的文字阴影
        text_shadow = self.font.render(self.text, True, (0, 0, 0))
        text_shadow.set_alpha(100)  # 设置文字阴影透明度
        shadow_rect = text_shadow.get_rect(center=(draw_rect.centerx + 1, draw_rect.centery + 1))
        screen.blit(text_shadow, shadow_rect)

        # 绘制主文字
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        if self.rect.collidepoint(mouse_pos) and self.callback:
            self.callback()