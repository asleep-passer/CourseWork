import pygame
import models
import config
from models.Road import RoadModel, RoadType
from models.map import MapModel
from models.roadcell import RoadCellModel

# Initialize Pygame
pygame.init()

# Set up the main screen with dimensions from config
mainScreen = pygame.display.set_mode(config.screenSize)

# Variable to control the game loop
isRunning = True

# Create a clock to manage the frame rate
clock = pygame.time.Clock()

# Variable to track time delta for frame-rate independent movement
dt = 0

# Set the initial position of the player (center of the screen)
player_pos = pygame.Vector2(mainScreen.get_width() / 2, mainScreen.get_height() / 2)

# Create 4x4 grid function
def create_4x4_grid() -> MapModel:
    """ Create and initialize a 4x4 grid with roads. """
    map_model = MapModel(4, 4)  # Create 4x4 grid

    for row in range(4):
        for col in range(4):
            # Set default roads for the grid (you can customize road types here)
            if (row == 0 and col == 0):
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.START_ROAD))
            elif (row == 3 and col == 3):
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.END_ROAD))
            else:
                map_model.set_cell(row, col, RoadCellModel(row, col, RoadType.STRAIGHT_ROAD))

    return map_model

# Create the 4x4 grid
map_model = create_4x4_grid()

# Game loop
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            break

    # Fill the screen with purple background
    mainScreen.fill("purple")

    # Render the 4x4 grid (Road Cells)
    for row in range(4):
        for col in range(4):
            road_cell = map_model.get_cell(row, col)
            road_type = road_cell.get_type()

            # Set color based on the road type
            color = (255, 255, 255)  # Default white
            if road_type == RoadType.START_ROAD:
                color = (0, 255, 0)  # Green for start
            elif road_type == RoadType.END_ROAD:
                color = (255, 0, 0)  # Red for end
            elif road_type == RoadType.STRAIGHT_ROAD:
                color = (0, 0, 255)  # Blue for straight road

            # Draw the road block (each block is 100x100 pixels)
            pygame.draw.rect(mainScreen, color, pygame.Rect(col * 100, row * 100, 100, 100))

    # Draw the player as a red circle at the center
    pygame.draw.circle(mainScreen, "red", player_pos, 40)

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt  # Move up
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt  # Move down
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt  # Move left
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt  # Move right

    # Update the display
    pygame.display.flip()

    # Limit frame rate to 60 FPS
    dt = clock.tick(60) / 1000  # Delta time for smooth movement

# Quit Pygame when the loop ends
pygame.quit()