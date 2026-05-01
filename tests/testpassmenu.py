from models import NormalRoadListModel as nl
from models import AdminRoadListModel as al
from models import Road as rd
import pygame as pg
import config as cg
from view.passmenu import PassMenuView

def test3():
    screen=pg.display.set_mode(cg.screenSize)
    pass_menu = PassMenuView(screen, score=2500, level_id=3, stars=2)
    running = True
    clock = pg.time.Clock()

    while running:
    # 处理事件 (如关闭窗口)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            action = pass_menu.handle_event(event)
            if action == 'next_level':
                pass
                # 跳转到下一关
            elif action == 'retry':
                pass
                # 重试当前关卡

    # --- 渲染步骤 ---
    # 1. 清空屏幕 (用白色填充)
        WHITE = (255, 255, 255)
        screen.fill(WHITE)

    # 2. 将图片绘制到屏幕上
    # screen.blit(Surface_to_draw, destination_Rect_or_Coordinates)
        pass_menu.draw()

    # 3. 更新显示
        pg.display.flip()

    # 控制帧率
        clock.tick(60)

    # 退出 Pygame
    pg.quit()

def main():
    pg.init()
    test3()

main()