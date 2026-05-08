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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            action = pass_menu.handle_event(event)
            if action == 'next_level':
                pass
            elif action == 'retry':
                pass

        WHITE = (255, 255, 255)
        screen.fill(WHITE)

        pass_menu.draw()

        pg.display.flip()

        clock.tick(60)

    pg.quit()

def main():
    pg.init()
    test3()

main()