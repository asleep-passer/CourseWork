"""Main application entry point for the Road Builder game.

This module initializes Pygame, sets up the display, and manages the state machine
that controls navigation between views such as the main menu, level selection,
difficulty screen, gameplay, level editor, and story intro.

The application uses a simple integer-based state system to switch between screens,
with each view handling its own rendering and input logic.
"""

import pygame
import sys
import os
from models.gamemodel import GameLevelModel, Difficulty
from view.main_menu_view import MainMenuView
from view.level_select_view import LevelSelectView
from view.difficulty_select_view import DifficultySelectView
from view.game_level_view import GameLevelView
from view.LevelEditorView import LevelEditorView
from view.story_intro_view import StoryIntroView
import config

# State constants
STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_DIFFICULTY = 2
STATE_GAME = 3
STATE_EDITOR = 4
STATE_STORY = 5


def main():
    """Run the main game loop and manage application state transitions.

    Initializes Pygame, creates the display window, and instantiates all necessary
    view objects. The loop handles events, updates the current view, and renders
    the appropriate screen based on the current state.

    Supported states include:
        - Main menu
        - Story introduction
        - Level selection (built-in and custom)
        - Difficulty selection
        - Gameplay
        - Level editor

    The function also manages background music playback (main menu only) and
    proper cleanup on exit.

    Returns:
        None
    """
    pygame.init()
    try:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.4)
    except Exception as e:
        print(f"[main] Audio initialization failed: {e}")

    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("Road Builder")
    clock = pygame.time.Clock()

    state = STATE_MAIN_MENU
    pending_level_id = 1

    main_menu_view = MainMenuView(1000, 650)
    story_view = StoryIntroView(1000, 650)
    level_select_view = LevelSelectView(1000, 650, saves_path=config.saves_path)
    difficulty_select_view = DifficultySelectView(1000, 650)
    game_view = None
    game_model = None
    editor_view = None

    main_music_playing = False

    running = True
    while running:
        clock.tick(60)

        # Manage main menu music
        if state == STATE_MAIN_MENU and not main_music_playing:
            if pygame.mixer.get_init():
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("view/assets/Sounds/main_menu.mp3")
                    pygame.mixer.music.play(-1)
                    main_music_playing = True
                except Exception as e:
                    print(f"[main] Failed to play main menu music: {e}")
        elif state != STATE_MAIN_MENU and main_music_playing:
            if pygame.mixer.get_init():
                try:
                    pygame.mixer.music.stop()
                    main_music_playing = False
                except Exception as e:
                    print(f"[main] Failed to stop main menu music: {e}")

        # Render current view
        if state == STATE_MAIN_MENU:
            main_menu_view.draw(screen)
        elif state == STATE_STORY:
            story_view.update()
            story_view.draw(screen)
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

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == STATE_MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = main_menu_view.handle_click(event.pos)
                    if result == "Start Game":
                        state = STATE_STORY
                        story_view.reset()
                    elif result == "Level Editor":
                        editor_view = LevelEditorView(screen)
                        state = STATE_EDITOR
                    elif result == "Quit":
                        running = False

            elif state == STATE_STORY:
                result = story_view.handle_event(event)
                if result == "done":
                    state = STATE_LEVEL_SELECT

            elif state == STATE_LEVEL_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = level_select_view.handle_click(event.pos)
                    if result is None:
                        continue

                    if result.startswith("play_builtin_"):
                        pending_level_id = int(result.split("_")[-1])
                        state = STATE_DIFFICULTY

                    elif result.startswith("play_custom_"):
                        pending_level_id = int(result.split("_")[-1])
                        state = STATE_DIFFICULTY

                    elif result.startswith("edit_custom_"):
                        level_id = int(result.split("_")[-1])
                        editor_view = LevelEditorView(screen)
                        editor_view.load_level(level_id)
                        state = STATE_EDITOR

                    elif result.startswith("delete_custom_"):
                        level_id = int(result.split("_")[-1])
                        file_path = os.path.join(config.saves_path, f"level{level_id}.txt")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        level_select_view.refresh_levels()

                    elif result == "back_to_menu":
                        state = STATE_MAIN_MENU

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

                        if pending_level_id <= 4:
                            game_model = GameLevelModel(level_id=pending_level_id, difficulty=difficulty)
                        else:
                            game_model = GameLevelModel.load_from_custom_file(pending_level_id, difficulty)
                        game_view = GameLevelView(screen, game_model)
                        state = STATE_GAME

            elif state == STATE_GAME:
                if game_view is not None:
                    action = game_view.handle_event(event)
                    if action == "back":
                        game_view.stop_music()
                        state = STATE_LEVEL_SELECT
                        game_view = None
                    elif action == "next_level":
                        game_view.stop_music()
                        next_id = pending_level_id + 1
                        if next_id <= 4:
                            pending_level_id = next_id
                            game_model = GameLevelModel(level_id=next_id, difficulty=game_model.difficulty)
                            game_view = GameLevelView(screen, game_model)
                        else:
                            file_path = os.path.join(config.saves_path, f"level{next_id}.txt")
                            if os.path.exists(file_path):
                                pending_level_id = next_id
                                game_model = GameLevelModel.load_from_custom_file(next_id, game_model.difficulty)
                                game_view = GameLevelView(screen, game_model)
                            else:
                                print("All levels complete!")
                                game_view.stop_music()
                                game_view = None
                                state = STATE_MAIN_MENU
                    elif action == "back_to_select":
                        game_view.stop_music()
                        state = STATE_LEVEL_SELECT
                        game_view = None

            elif state == STATE_EDITOR:
                if editor_view is not None:
                    action = editor_view.handle_event(event)
                    if action == "back_to_menu":
                        level_select_view.refresh_levels()
                        editor_view = None
                        state = STATE_MAIN_MENU

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()