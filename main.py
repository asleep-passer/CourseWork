import pygame
import sys
import os
from models.gamemodel import GameLevelModel, Difficulty
from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.difficulty_select_view import DifficultySelectView
from view.game_level_view import GameLevelView
from view.LevelEditorView import LevelEditorView
import config

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
    level_select_view = LevelSelectView(800, 650, saves_path=config.saves_path)
    difficulty_select_view = DifficultySelectView(800, 650)
    game_view = None
    game_model = None
    editor_view = None

    running = True
    while running:
        clock.tick(60)

        # ---- 绘制当前状态 ----
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
        elif state == STATE_EDITOR:
            if editor_view is not None:
                editor_view.update()
                editor_view.draw()

        pygame.display.flip()

        # ---- 事件处理 ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ========== 主菜单 ==========
            if state == STATE_MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = main_menu_view.handle_click(event.pos)
                    if result == "Start Game":
                        state = STATE_LEVEL_SELECT
                    elif result == "Level Editor":
                        editor_view = LevelEditorView(screen)
                        state = STATE_EDITOR
                    elif result == "Quit":
                        running = False

            # ========== 关卡选择 ==========
            elif state == STATE_LEVEL_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = level_select_view.handle_click(event.pos)
                    if result is None:
                        continue

                    # 内置关卡
                    if result.startswith("play_builtin_"):
                        pending_level_id = int(result.split("_")[-1])
                        state = STATE_DIFFICULTY

                    # 自定义关卡 play
                    elif result.startswith("play_custom_"):
                        pending_level_id = int(result.split("_")[-1])
                        state = STATE_DIFFICULTY

                    # 自定义关卡 edit
                    elif result.startswith("edit_custom_"):
                        level_id = int(result.split("_")[-1])
                        editor_view = LevelEditorView(screen)
                        editor_view.load_level(level_id)
                        state = STATE_EDITOR

                    # 自定义关卡 delete
                    elif result.startswith("delete_custom_"):
                        level_id = int(result.split("_")[-1])
                        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        level_select_view.refresh_levels()

                    elif result == "back_to_menu":
                        state = STATE_MAIN_MENU

            # ========== 难度选择 ==========
            elif state == STATE_DIFFICULTY:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = difficulty_select_view.handle_click(event.pos)
                    if result == "Back":
                        state = STATE_LEVEL_SELECT
                    elif result in ("Easy", "Medium", "Hard"):
                        diff_map = {
                            "Easy": Difficulty.EASY,
                            "Medium": Difficulty.MEDIUM,
                            "Hard": Difficulty.HARD
                        }
                        difficulty = diff_map[result]

                        # 加载关卡（内置或自定义）
                        if pending_level_id <= 4:
                            game_model = GameLevelModel(level_id=pending_level_id, difficulty=difficulty)
                        else:
                            game_model = GameLevelModel.load_from_custom_file(pending_level_id, difficulty)
                        game_view = GameLevelView(screen, game_model)
                        state = STATE_GAME

            # ========== 游戏中 ==========
            elif state == STATE_GAME:
                if game_view is not None:
                    action = game_view.handle_event(event)
                    if action == "back":
                        state = STATE_LEVEL_SELECT
                        game_view = None
                    elif action == "next_level":
                        next_id = pending_level_id + 1
                        if next_id <= 4:
                            pending_level_id = next_id
                            game_model = GameLevelModel(level_id=next_id, difficulty=game_model.difficulty)
                            game_view = GameLevelView(screen, game_model)
                        else:
                            # 检查自定义关卡文件是否存在
                            file_path = os.path.join(config.saves_path, f"level{next_id}.txt")
                            if os.path.exists(file_path):
                                pending_level_id = next_id
                                game_model = GameLevelModel.load_from_custom_file(next_id, game_model.difficulty)
                                game_view = GameLevelView(screen, game_model)
                            else:
                                print("All levels complete!")
                                state = STATE_MAIN_MENU
                    elif action == "back_to_select":
                        state = STATE_LEVEL_SELECT

            # ========== 关卡编辑器 ==========
            elif state == STATE_EDITOR:
                if editor_view is not None:
                    action = editor_view.handle_event(event)
                    if action == "back_to_menu":
                        level_select_view.refresh_levels()
                        editor_view = None
                        state = STATE_MAIN_MENU
                    # 其他编辑器动作不改变状态

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()