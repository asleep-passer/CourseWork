from abc import ABC, abstractmethod
from .road import RoadType as rt
from .road import RoadModel as rm

class RoadListModel(ABC):
    def __init__(self) -> None:
        self._road_num={}
        self._road_list={}
        pass

    def get_road(self,road_type:rt):
        if self._road_num[road_type]>0:
            self._road_num[road_type]-=1
            return self._road_list[road_type].pop()
        elif self._road_num[road_type]<0:
            self._road_num[road_type]-=1
            if self._road_list[road_type].__len__()>0:
                return self._road_list[road_type].pop()
            else:
                return rm(road_type)
        else:
            print("There is no more road can be used.")
        
    def store_road(self,road:rm):
        for exist_road in self._road_list.values():
            if exist_road is road:
                return
        self._road_num[road.road_type]+=1
        self._road_list[road.road_type].append(road)

    def get_road_num(self,road_type:rt):
        if self._road_num[road_type]<0:
            return "inf"
        return self._road_num[road_type]

    

class NormalRoadListModel(RoadListModel):
    def __init__(self, num_str_road:int, num_bend_road:int, num_t_road:int, num_cross_road:int) -> None:
        super().__init__()

        self._road_num={rt.STRAIGHT_ROAD:num_str_road,
                        rt.BEND_ROAD:num_bend_road,
                        rt.T_SHAPED_ROAD:num_t_road,
                        rt.CROSS_ROAD:num_cross_road}
        
        self._road_list={rt.STRAIGHT_ROAD:[],
                        rt.BEND_ROAD:[],
                        rt.T_SHAPED_ROAD:[],
                        rt.CROSS_ROAD:[]}
        
        for type,num in self._road_num.items():
            if num > 0:
                for i in range(num):
                    self._road_list[type].append(rm(type))
    
    


class AdminRoadListModel(RoadListModel):
    def __init__(self) -> None:
        super().__init__()