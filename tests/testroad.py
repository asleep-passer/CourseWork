from models import RoadModel
from models import RoadType

def test1():
    road=RoadModel(RoadType.STRAIGHT_ROAD)
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())

def main():
    test1()

main()
