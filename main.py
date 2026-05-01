from models.Road import RoadModel, RoadType
from models.map import MapModel
from models.roadcell import RoadCellModel

def create_4x4_grid() -> MapModel:
    """
    Create and initialize a 4x4 grid with roads.
    """
    map_model = MapModel(4, 4)

    # Initialize the grid with some road types for example
    for row in range(4):
        for col in range(4):
            # You can customize which roads to place where
            if (row == 0 and col == 0):
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.START_ROAD))
            elif (row == 3 and col == 3):
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.END_ROAD))
            else:
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.STRAIGHT_ROAD))

    return map_model

def main():
    # Create the 4x4 grid with roads
    map_model = create_4x4_grid()

    # Print the grid (just for checking)
    map_model.print_grid()

    # Example: Rotate a road at (0, 1)
    road_cell = map_model.get_cell(0, 1)
    road_cell.rotate()

    # Print the grid after rotation
    print("\nAfter rotating:")
    map_model.print_grid()

if __name__ == "__main__":
    main()