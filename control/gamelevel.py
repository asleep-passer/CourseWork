import config
from typing import List, Tuple, Optional
from models.Road import RoadType

class GameLevelController:
    """
    临时存储关卡信息的数据包，属性结构与硬编码配置完全匹配
    """
    def __init__(self):
        self.map: List[List[str]] = []  # 4x4 网格，包含 'S', 'E', 'O', ' '
        self.roads: Tuple[int, int, int, int] = (0, 0, 0, 0)  # (straight, curve, t_junction, cross)

    @classmethod
    def load_from_file(cls, level_id: int) -> Optional['GameLevelController']:
        """
        从文件加载关卡数据并转换为与硬编码配置匹配的格式
        """
        try:
            level_id = max(1, level_id)
            file_path = config.saves_path + "level" + str(level_id)+".txt"
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            if not lines:
                return None
                
            # 解析第一行：行数和列数
            rows, cols = map(int, lines[0].strip().split())
            data = cls()
            
            # 读取道路类型矩阵
            current_line = 1
            road_types = []
            for _ in range(rows):
                if current_line >= len(lines):
                    break
                row = list(map(int, lines[current_line].strip().split()))
                road_types.append(row)
                current_line += 1
            
            # 读取锁定状态（这里我们不使用，因为硬编码配置中没有锁定信息）
            current_line += rows  # 跳过锁定状态
            
            # 读取旋转状态（这里我们不使用，因为硬编码配置中没有旋转信息）
            current_line += rows  # 跳过旋转状态
            
            # 读取可用道路数量
            if current_line < len(lines):
                available_roads = list(map(int, lines[current_line].strip().split()))
                # 确保有4个值，与硬编码配置匹配
                if len(available_roads) >= 4:
                    data.roads = tuple(available_roads[:4]) # type: ignore
            
            # 将道路类型矩阵转换为硬编码配置格式
            # 5=START_ROAD -> 'S', 6=END_ROAD -> 'E', 0=OBSTACLE_ROAD -> 'O', 7=EMPTY -> ' '
            data.map = []
            for r in range(min(rows, 4)):  # 限制为4x4
                row_data = []
                for c in range(min(cols, 4)):
                    if r < len(road_types) and c < len(road_types[r]):
                        road_num = road_types[r][c]
                        if road_num == 5:
                            row_data.append('S')
                        elif road_num == 6:
                            row_data.append('E')
                        elif road_num == 0:
                            row_data.append('O')
                        else:  # 7 or other
                            row_data.append(' ')
                    else:
                        row_data.append(' ')
                data.map.append(row_data)
            
            # 确保是4x4网格
            while len(data.map) < 4:
                data.map.append([' '] * 4)
            for i in range(4):
                while len(data.map[i]) < 4:
                    data.map[i].append(' ')
            
            return data
            
        except (FileNotFoundError, ValueError, IndexError) as e:
            print(f"Error loading level {level_id} from file: {e}")
            return None