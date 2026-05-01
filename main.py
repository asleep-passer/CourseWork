import pygame
import sys
from models.gamemodel import GameLevelModel
from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.game_level_view import GameLevelView

STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_GAME = 2

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 650))
    pygame.display.set_caption("Road Builder")
    clock = pygame.time.Clock()

    state = STATE_MAIN_MENU
    current_level_id = 1

    main_menu_view = MainMenuView(800, 650)
    level_select_view = LevelSelectView(800, 650)
    game_view = None
    game_model = None

    running = True
    while running:
        clock.tick(60)

        # 绘制
        if state == STATE_MAIN_MENU:
            main_menu_view.draw(screen)
        elif state == STATE_LEVEL_SELECT:
            level_select_view.draw(screen)
        elif state == STATE_GAME:
            if game_view is not None:
                game_view.update()
                game_view.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == STATE_MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = main_menu_view.handle_click(event.pos)
                    if result == "Start Game":
                        state = STATE_LEVEL_SELECT
                    elif result == "Quit":
                        running = False

            elif state == STATE_LEVEL_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = level_select_view.handle_click(event.pos)
                    if result and result.startswith("Level"):
                        level_id = int(result.split()[-1])
                        current_level_id = level_id
                        game_model = GameLevelModel(level_id=level_id)
                        game_view = GameLevelView(screen, game_model)
                        state = STATE_GAME
                    elif result == "Back":
                        state = STATE_MAIN_MENU

            elif state == STATE_GAME:
                if game_view is not None:
                    action = game_view.handle_event(event)
                    if action == "back":
                        state = STATE_LEVEL_SELECT
                    elif action == "next_level":
                        next_id = current_level_id + 1
                        if next_id <= 4:
                            current_level_id = next_id
                            game_model = GameLevelModel(level_id=next_id)
                            game_view = GameLevelView(screen, game_model)
                        else:
                            print("All levels complete!")
                            state = STATE_MAIN_MENU

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()