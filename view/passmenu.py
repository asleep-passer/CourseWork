import pygame as pg
from typing import Tuple, Optional, Callable
from view.button_view import ButtonView

class PassMenuView:
    def __init__(self, screen: pg.Surface, score: int, level_id: int, stars: int = 0):
        self.screen = screen
        self.score = score
        self.level_id = level_id
        self.stars = min(max(stars, 0), 3)  # 限制在0-3颗星
        
        # 计算星星评分（基于分数）
        if stars == 0:
            self.stars = self._calculate_stars_from_score(score)
        
        # UI尺寸和位置
        screen_w, screen_h = screen.get_size()
        self.dialog_w, self.dialog_h = 400, 350
        self.dialog_x = (screen_w - self.dialog_w) // 2
        self.dialog_y = (screen_h - self.dialog_h) // 2
        
        # 颜色定义
        self.bg_color = (240, 248, 255)  # 淡蓝色背景
        self.border_color = (60, 120, 200)
        self.star_color = (255, 215, 0)  # 金色星星
        self.text_color = (30, 30, 30)
        
        # 字体
        self.title_font = pg.font.Font(None, 36)
        self.score_font = pg.font.Font(None, 28)
        self.star_font = pg.font.Font(None, 48)
        
        # 创建按钮
        btn_width, btn_height = 120, 45
        btn_y = self.dialog_y + self.dialog_h - 70
        
        self.next_btn = ButtonView(
            self.dialog_x + 30, btn_y, btn_width, btn_height, "next level",
            callback=lambda: setattr(self, '_action', 'next_level')
        )
        
        self.retry_btn = ButtonView(
            self.dialog_x + self.dialog_w - btn_width - 30, btn_y, 
            btn_width, btn_height, "retry",
            callback=lambda: setattr(self, '_action', 'retry')
        )
        
        # 内部状态
        self._action = None
        self.visible = True
    
    def _calculate_stars_from_score(self, score: int) -> int:
        """根据分数计算星星数量"""
        if score >= 3000:
            return 3
        elif score >= 2000:
            return 2
        elif score >= 1000:
            return 1
        return 0
    
    def handle_event(self, event: pg.event.Event) -> Optional[str]:
        """处理事件，返回动作"""
        if not self.visible:
            return None
            
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # 检查按钮点击
            for btn in [self.next_btn, self.retry_btn]:
                if btn.rect.collidepoint(pos):
                    btn.handle_click(pos)
                    action = self._action
                    self._action = None
                    return action
        return None
    
    def draw(self) -> None:
        """绘制过关菜单"""
        if not self.visible:
            return
            
        # 1. 绘制半透明背景遮罩
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色
        self.screen.blit(overlay, (0, 0))
        
        # 2. 绘制对话框背景
        dialog_rect = pg.Rect(self.dialog_x, self.dialog_y, self.dialog_w, self.dialog_h)
        pg.draw.rect(self.screen, self.bg_color, dialog_rect, border_radius=15)
        pg.draw.rect(self.screen, self.border_color, dialog_rect, 3, border_radius=15)
        
        # 3. 绘制标题
        title_text = self.title_font.render(f"Level {self.level_id} pass!", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.dialog_x + self.dialog_w // 2, self.dialog_y + 40))
        self.screen.blit(title_text, title_rect)
        
        
        # 5. 绘制分数
        score_text = self.score_font.render(f"Scores: {self.score}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.dialog_x + self.dialog_w // 2, self.dialog_y + 160))
        self.screen.blit(score_text, score_rect)
        
        
        # 7. 绘制按钮
        self.next_btn.draw(self.screen)
        self.retry_btn.draw(self.screen)
        
        # 8. 绘制提示文字
        tip_text = "click button to continue"
        tip_surf = pg.font.Font(None, 20).render(tip_text, True, (100, 100, 100))
        tip_rect = tip_surf.get_rect(center=(self.dialog_x + self.dialog_w // 2, self.dialog_y + self.dialog_h - 20))
        self.screen.blit(tip_surf, tip_rect)
    
    def set_visible(self, visible: bool) -> None:
        """设置可见性"""
        self.visible = visible
    
    def update_stars(self, new_stars: int) -> None:
        """更新星星数量"""
        self.stars = min(max(new_stars, 0), 3)
    
    def update_score(self, new_score: int) -> None:
        """更新分数"""
        self.score = new_score
        self.stars = self._calculate_stars_from_score(new_score)