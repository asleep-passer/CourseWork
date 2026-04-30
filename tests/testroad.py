import sys
import os
# 获取项目根目录并添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


from models import road as rd

def test1():
    road=rd.RoadModel(rd.RoadModel.RoadType.STRAIGHT_ROAD)
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())
    road.rotate()
    print(road.get_passable_direction())

def main():
    test1()

main()
