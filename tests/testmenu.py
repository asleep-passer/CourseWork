import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.difficulty_select_view import DifficultySelectView


pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Road Builder")
clock = pygame.time.Clock()

main_menu = MainMenuView(W, H)
level_select = LevelSelectView(W, H)
diff_select = DifficultySelectView(W, H)

current_state = "menu"

running = True
while running:
    screen.fill((235, 245, 255))

    if current_state == "menu":
        main_menu.draw(screen)
    elif current_state == "level":
        level_select.draw(screen)
    elif current_state == "difficulty":
        diff_select.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            W, H = event.w, event.h
            screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if current_state == "menu":
                res = main_menu.handle_click(pos)
                if res == "Start Game":
                    current_state = "level"
                if res == "Quit":
                    running = False

            elif current_state == "level":
                res = level_select.handle_click(pos)
                if res == "Back":
                    current_state = "menu"
                if res and res.startswith("Level"):
                    current_state = "difficulty"

            elif current_state == "difficulty":
                res = diff_select.handle_click(pos)
                if res == "Back":
                    current_state = "level"
                if res in ["Easy", "Medium", "Hard"]:
                    print(f"Selected Difficulty: {res}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()