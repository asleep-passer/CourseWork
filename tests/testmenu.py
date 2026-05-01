import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.difficulty_select_view import DifficultySelectView

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

main_menu = MainMenuView(W, H)
level_select = LevelSelectView(W, H)
diff_select = DifficultySelectView(W, H)

state = "menu"

running = True
while running:
    screen.fill((235, 245, 255))

    if state == "menu":
        main_menu.draw(screen)
    elif state == "level":
        level_select.draw(screen)
    elif state == "difficulty":
        diff_select.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if state == "menu":
                res = main_menu.handle_click(pos)
                if res == "Start Game":
                    state = "level"
                if res == "Quit":
                    running = False

            elif state == "level":
                res = level_select.handle_click(pos)
                if res == "Back":
                    state = "menu"
                if res and res.startswith("Level"):
                    state = "difficulty"

            elif state == "difficulty":
                res = diff_select.handle_click(pos)
                if res == "Back":
                    state = "level"
                if res in ["Easy", "Medium", "Hard"]:
                    print(f"进入游戏：关卡+难度 → {res}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()