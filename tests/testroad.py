from models import RoadModel as rm
from models import RoadType as rt
from view import RoadView as rv
import pygame as pg
import config as cg

def test1():
    road=rm(rt.STRAIGHT_ROAD)
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())

def test2():
    
    screen=pg.display.set_mode(cg.screenSize)
    road=rm(rt.STRAIGHT_ROAD)
    road_view=rv(road,screen,pg.Rect(100,100,100,100))
    running = True
    clock = pg.time.Clock()

    while running:
    # 处理事件 (如关闭窗口)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key==pg.K_r:
                    road_view.rotated()

    # --- 渲染步骤 ---
    # 1. 清空屏幕 (用白色填充)
        WHITE = (255, 255, 255)
        screen.fill(WHITE)

    # 2. 将图片绘制到屏幕上
    # screen.blit(Surface_to_draw, destination_Rect_or_Coordinates)
        road_view.draw()

    # 3. 更新显示
        pg.display.flip()

    # 控制帧率
        clock.tick(60)

    # 退出 Pygame
    pg.quit()
        

def main():
    test2()


pg.init()
main()
