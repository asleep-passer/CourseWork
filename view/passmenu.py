import pygame as pg
import math
from typing import Optional
from view.button_view import ButtonView

class PassMenuView:
    def __init__(self, screen: pg.Surface, score: int, level_id: int, stars: int = 0):
        self.screen = screen
        self.score = score
        self.level_id = level_id
        self.stars = min(max(stars, 0), 3)

        if stars == 0:
            self.stars = self._calculate_stars_from_score(score)

        screen_w, screen_h = screen.get_size()
        self.dialog_w, self.dialog_h = 400, 400
        self.dialog_x = (screen_w - self.dialog_w) // 2
        self.dialog_y = (screen_h - self.dialog_h) // 2

        self.bg_color = (240, 248, 255)
        self.border_color = (60, 120, 200)
        self.star_color = (255, 215, 0)          # 金色实心
        self.star_empty = (180, 180, 180)        # 灰色空心
        self.text_color = (30, 30, 30)
        self.shadow_color = (80, 80, 80)         # 星星投影

        self.title_font = pg.font.Font(None, 40)
        self.score_font = pg.font.Font(None, 32)

        btn_width, btn_height = 120, 45
        btn_y = self.dialog_y + self.dialog_h - 70

        def set_next():
            self._action = 'next_level'
        def set_retry():
            self._action = 'retry'

        self.next_btn = ButtonView(
            self.dialog_x + 30, btn_y, btn_width, btn_height, "Next",
            callback=set_next
        )
        self.retry_btn = ButtonView(
            self.dialog_x + self.dialog_w - btn_width - 30, btn_y,
            btn_width, btn_height, "Retry",
            callback=set_retry
        )

        self._action = None
        self.visible = True

        # 动画相关：星星逐个弹出
        self.stars_revealed = 0          # 当前已显示的星星数
        self.star_reveal_timer = 0       # 计时器
        self.star_reveal_delay = 15      # 每颗星出现的间隔帧数（约0.25秒/60fps）
        self._star_animation_done = False

    def _calculate_stars_from_score(self, score: int) -> int:
        if score >= 1000:
            return 3
        elif score >= 800:
            return 2
        elif score >= 500:
            return 1
        return 0

    def _draw_star(self, center_x, center_y, radius, filled=True):
        """绘制一个带阴影和边框的五角星，加强立体感"""
        points = []
        inner_radius = radius * 0.4
        for i in range(10):
            angle = math.pi / 2 - i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = inner_radius
            x = center_x + r * math.cos(angle)
            y = center_y - r * math.sin(angle)
            points.append((x, y))

        if filled:
            # 1. 投影（向下向右偏移 3px）
            shadow_points = [(x+3, y+3) for (x, y) in points]
            pg.draw.polygon(self.screen, self.shadow_color, shadow_points)
            # 2. 描边（深色边框加粗）
            pg.draw.polygon(self.screen, (180, 120, 0), points, 4)
            # 3. 金色填充
            pg.draw.polygon(self.screen, self.star_color, points)
            # 4. 高光小圆点（星星中心偏左上）
            pg.draw.circle(self.screen, (255, 255, 200), (int(center_x-5), int(center_y-5)), 5)
        else:
            # 空心星星：浅灰填充 + 深灰边框
            pg.draw.polygon(self.screen, self.star_empty, points)
            pg.draw.polygon(self.screen, (120, 120, 120), points, 2)

    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        if not self.visible:
            return None
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for btn in [self.next_btn, self.retry_btn]:
                if btn.rect.collidepoint(pos):
                    btn.handle_click(pos)
                    action = self._action
                    self._action = None
                    return action
        return None

    def draw(self) -> None:
        if not self.visible:
            return

        # 更新星星逐个弹出动画
        if not self._star_animation_done and self.stars_revealed < self.stars:
            self.star_reveal_timer += 1
            if self.star_reveal_timer >= self.star_reveal_delay:
                self.star_reveal_timer = 0
                self.stars_revealed += 1
        else:
            self._star_animation_done = True

        # 半透明遮罩
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # 对话框背景
        dialog_rect = pg.Rect(self.dialog_x, self.dialog_y, self.dialog_w, self.dialog_h)
        pg.draw.rect(self.screen, self.bg_color, dialog_rect, border_radius=15)
        pg.draw.rect(self.screen, self.border_color, dialog_rect, 3, border_radius=15)

        # 标题
        title_text = self.title_font.render(f"Level {self.level_id} Pass!", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.dialog_x + self.dialog_w // 2, self.dialog_y + 45))
        self.screen.blit(title_text, title_rect)

        # 星星（带动画和立体边框）
        star_radius = 28
        star_spacing = 75
        total_width = 3 * star_spacing
        start_x = self.dialog_x + (self.dialog_w - total_width) // 2 + star_spacing // 2
        star_y = self.dialog_y + 135

        for i in range(3):
            filled = i < self.stars_revealed   # 只显示已弹出的实心星星，未弹出则为空心
            self._draw_star(start_x + i * star_spacing, star_y, star_radius, filled)

        # 分数
        score_text = self.score_font.render(f"Score: {self.score}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.dialog_x + self.dialog_w // 2, self.dialog_y + 225))
        self.screen.blit(score_text, score_rect)

        # 按钮
        self.next_btn.draw(self.screen)
        self.retry_btn.draw(self.screen)

    def set_visible(self, visible: bool) -> None:
        self.visible = visible
        if visible:
            # 重置动画状态
            self.stars_revealed = 0
            self.star_reveal_timer = 0
            self._star_animation_done = False

    def update_stars(self, new_stars: int) -> None:
        self.stars = min(max(new_stars, 0), 3)

    def update_score(self, new_score: int) -> None:
        self.score = new_score
        self.stars = self._calculate_stars_from_score(new_score)