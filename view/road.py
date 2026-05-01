import pygame as pg
from models import RoadType as rt

class RoadView:
    def __init__(self,road_type:rt,screen:pg.surface.Surface,x:int,y:int) -> None:
        self.road_type=road_type
        self.__screen=screen
        self.__x=x
        self.__y=y

        if road_type==rt.OBSTACLE_ROAD:
            pass
        elif road_type==rt.STRAIGHT_ROAD:
            pass
        elif road_type==rt.BEND_ROAD:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile7.png")
        elif road_type==rt.T_SHAPED_ROAD:
            self.__img=