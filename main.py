import pygame
import sys
from models.gamemodel import GameLevelModel, Difficulty
from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.difficulty_select_view import DifficultySelectView
from view.game_level_view import GameLevelView
from view.LevelEditorView import LevelEditorView

STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_DIFFICULTY = 2
STATE_GAME = 3
STATE_EDITOR = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 650))
    pygame.display.set_caption("Road Builder")
    clock = pygame.time.Clock()

    state = STATE_MAIN_MENU
    pending_level_id = 1

    main_menu_view = MainMenuView(800, 650)
    level_select_view = LevelSelectView(800, 650)
    difficulty_select_view = DifficultySelectView(800, 650)
    game_view = None
    game_model = None

    running = True
    while running:
        clock.tick(60)
        if state == STATE_MAIN_MENU:
            main_menu_view.draw(screen)
        elif state == STATE_LEVEL_SELECT:
            level_select_view.draw(screen)
        elif state == STATE_DIFFICULTY:
            difficulty_select_view.draw(screen)
        elif state == STATE_GAME:
            if game_view is not None:
                game_view.update()
                game_view.draw()
        elif state==STATE_EDITOR:
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
                    elif result == "Level Editor":
                        state = STATE_EDITOR
                    elif result == "Quit":
                        running = False

            elif state == STATE_LEVEL_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = level_select_view.handle_click(event.pos)
                    if result and result.startswith("Level"):
                        pending_level_id = int(result.split()[-1])
                        state = STATE_DIFFICULTY
                    elif result == "Back":
                        state = STATE_MAIN_MENU

            elif state == STATE_DIFFICULTY:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = difficulty_select_view.handle_click(event.pos)
                    if result == "Back":
                        state = STATE_LEVEL_SELECT
                    elif result in ("Easy", "Medium", "Hard"):
                        diff_map = {"Easy": Difficulty.EASY,
                                    "Medium": Difficulty.MEDIUM,
                                    "Hard": Difficulty.HARD}
                        game_model = GameLevelModel(level_id=pending_level_id,
                                                    difficulty=diff_map[result])
                        game_view = GameLevelView(screen, game_model)
                        state = STATE_GAME


            elif state == STATE_GAME:
                if game_view is not None:
                    action = game_view.handle_event(event)
                    if action == "back":
                        state = STATE_LEVEL_SELECT
                        game_view=None
                    elif action == "next_level":
                        next_id = pending_level_id + 1
                        if next_id <= 12:
                            pending_level_id = next_id
                            game_model = GameLevelModel(level_id=next_id,
                                                        difficulty=game_model.difficulty)
                            game_view = GameLevelView(screen, game_model)
                        else:
                            print("All levels complete!")
                            state = STATE_MAIN_MENU
                    elif action == "back_to_select":
                        state = STATE_LEVEL_SELECT

            elif state==STATE_EDITOR:
                if game_view is None:
                    game_view = LevelEditorView(screen)
                else: 
                    action = game_view.handle_event(event)
                    if action == "back_to_menu":
                        game_view=None
                        level_select_view=LevelSelectView(800, 650)
                        state = STATE_MAIN_MENU

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()