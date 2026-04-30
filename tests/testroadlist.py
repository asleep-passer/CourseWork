from models import NormalRoadListModel as nl
from models import road as rd

def test1():
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

def main():
    test1()

main()
    