from models import NormalRoadListModel as nl
from models import AdminRoadListModel as al
from models import Road as rd
from view import RoadListView as rl
import pygame as pg
import config as cg

def test1():
    print("Test1:")
    road_list=nl(1,-1,2,0)
    road=road_list.get_road(rd.RoadType.CROSS_ROAD)
    print(road_list.get_road_num(rd.RoadType.CROSS_ROAD))

    road=road_list.get_road(rd.RoadType.BEND_ROAD)
    print(road_list.get_road_num(rd.RoadType.BEND_ROAD))
    if road!= None: road_list.store_road(road)
    print(road_list.get_road_num(rd.RoadType.BEND_ROAD))

    road=road_list.get_road(rd.RoadType.STRAIGHT_ROAD)
    print(road_list.get_road_num(rd.RoadType.STRAIGHT_ROAD))
    if road!= None: road_list.store_road(road)
    print(road_list.get_road_num(rd.RoadType.STRAIGHT_ROAD))

def test2():
    print("Test2:")
    road_list=al()
    print(road_list.get_road_num(rd.RoadType.START_ROAD))
    road=road_list.get_road(rd.RoadType.START_ROAD)
    print(road_list.get_road_num(rd.RoadType.START_ROAD))
    if road!=None: road_list.store_road(road)
    print(road_list.get_road_num(rd.RoadType.START_ROAD))

def test3():
    screen=pg.display.set_mode(cg.screenSize)
    road_list=rl(nl(1,2,3,4),screen)
    running = True
    clock = pg.time.Clock()

    while running:
    # 处理事件 (如关闭窗口)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

    # --- 渲染步骤 ---
    # 1. 清空屏幕 (用白色填充)
        WHITE = (255, 255, 255)
        screen.fill(WHITE)

    # 2. 将图片绘制到屏幕上
    # screen.blit(Surface_to_draw, destination_Rect_or_Coordinates)
        road_list.draw()

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
    