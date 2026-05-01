import pygame as pg
from models import RoadType as rt
from models import RoadModel as rm

class RoadView:
    def __init__(self,road:rm,screen:pg.surface.Surface,x:int,y:int) -> None:
        self.road=road
        self.__screen=screen
        self.__x=x
        self.__y=y

        if road.road_type==rt.OBSTACLE_ROAD:
            self.__img=pg.image.load("./ssets/Legacy/PNG/terrainTile3.png")
        elif road.road_type==rt.STRAIGHT_ROAD:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile27.png")
        elif road.road_type==rt.BEND_ROAD:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile7.png")
        elif road.road_type==rt.T_SHAPED_ROAD:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile9.png")
        elif road.road_type==rt.CROSS_ROAD:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile5.png")
        else:
            self.__img=pg.image.load("./assets/Legacy/PNG/roadTile18.png")