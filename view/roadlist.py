from models.roadlist import RoadListModel as rl
import pygame as pg
class RoadListView:
    def __init__(self,road_list:rl,screen: pg.surface.Surface,is_horizontal:bool=False) -> None:
        self.__road_list=road_list
        self.__screen=screen
        self.__mode=is_horizontal

        
        pass

    def on_click(self):

        self.draw()
        pass

    def draw(self):
        pass