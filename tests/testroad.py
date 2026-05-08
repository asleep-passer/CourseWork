from models import RoadModel as rm
from models import RoadType as rt
from view import RoadView as rv
import pygame as pg
import config as cg


def test1():
    road = rm(rt.STRAIGHT_ROAD)
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())


def test2():
    screen = pg.display.set_mode(cg.screenSize)
    road = rm(rt.STRAIGHT_ROAD)
    road_view = rv(road, screen, pg.Rect(100, 100, 100, 100))
    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    road_view.rotated()


        WHITE = (255, 255, 255)
        screen.fill(WHITE)

        road_view.draw()

        pg.display.flip()

        clock.tick(60)

    pg.quit()


def main():
    test2()


pg.init()
main()