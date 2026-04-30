from abc import ABC
from .road import RoadType as rt
from .road import RoadModel as rm

class RoadListModel(ABC):
    """
    An abstract list of roads, 
    providing three methods: 
    retrieving roads, 
    storing roads, 
    and viewing the number of roads.

    Attributes:
        _road_num (Dict[RoadType:int]):        The number of roads of the corresponding road type.
        _road_list (Dict[RoadType:RoadModel]): The instances of road of the corresponding road type.
    """

    def __init__(self) -> None:
        """
        Create attributes.
        """
        self._road_num={}
        self._road_list={}
        pass

    def get_road(self,road_type:rt):
        """
        Get the road instance,
        If the number of instances of this type of road is 0, then exit the function.
        Otherwise, return a road instance.

        Args:
            road_type (RoadType): The type of the road to be gotten.

        Returns:
            RoadModel: The road that is gotten.
        """
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
        """
        Store the road instance.

        Args:
            road (RoadModel): The road to be stored. 
        """
        for exist_road in self._road_list[road.road_type].values():
            if exist_road is road:
                return
        self._road_num[road.road_type]+=1
        self._road_list[road.road_type].append(road)

    def get_road_num(self,road_type:rt):
        """
        Get the number of roads of the corresponding road type.

        Args:
            road_type (RoadType): The type of the road to be checked.

        Returns:
            int: The number of this type of roads.
        """
        if self._road_num[road_type]<0:
            return "inf"
        return self._road_num[road_type]

    

class NormalRoadListModel(RoadListModel):
    def __init__(self, 
                 num_str_road:int, 
                 num_bend_road:int, 
                 num_t_road:int, 
                 num_cross_road:int) -> None:
        """
        Formatting Attributes.

        Args:
            num_str_road (int):   The number of straight road, negative number means infinite.
            num_bend_road (int):  The number of bend road, negative number means infinite.
            num_t_road (int):     The number of t-shaped road, negative number means infinite.
            num_cross_road (int): The number of cross road, negative number means infinite.
        """
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
        """
        Formatting Attributes
        """
        super().__init__()

        self._road_num={rt.OBSTACLE_ROAD:-1,
                        rt.STRAIGHT_ROAD:-1,
                        rt.BEND_ROAD:-1,
                        rt.T_SHAPED_ROAD:-1,
                        rt.CROSS_ROAD:-1,
                        rt.START_ROAD:-1,
                        rt.END_ROAD:-1}
        
        self._road_list={rt.OBSTACLE_ROAD:[],
                        rt.STRAIGHT_ROAD:[],
                        rt.BEND_ROAD:[],
                        rt.T_SHAPED_ROAD:[],
                        rt.CROSS_ROAD:[],
                        rt.START_ROAD:[],
                        rt.END_ROAD:[]}