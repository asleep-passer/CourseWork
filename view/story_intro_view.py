import pygame
import os


class StoryIntroView:
    """
    View component for displaying the animated story introduction dialogue sequence.
    Handles typewriter text animation, dialogue box UI, portrait display, and user input.
    """
    def __init__(self, width, height):
        """
        Initialize the story intro view with UI assets, animations, and dialogue lines.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.width = width
        self.height = height

        self.dialogues = [
            "MAYOR: Listen up, rookie!",
            "MAYOR: The city's traffic has been paralyzed for 30 days! It's a total disaster!",
            "MAYOR: Take these asphalt blocks and fix it! NOW!",
            "MAYOR: And please... don't let the cars fall into the water... AGAIN!"
        ]

        self.current_line = 0
        self.current_char = 0
        self.char_timer = 0
        self.text_speed = 30
        self.last_update_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks() 

      
        self.bg = pygame.image.load(os.path.join("view", "assets", "backgrounds", "story_background.jpg")).convert()
        self.bg = pygame.transform.scale(self.bg, (width, height))

       
        try:
            portrait_path = os.path.join("view", "assets","backgrounds","portrait.png")
            self.portrait = pygame.image.load(portrait_path).convert_alpha()
            self.portrait = pygame.transform.scale(self.portrait, (100, 100))
        except FileNotFoundError:
            
            self.portrait = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.rect(self.portrait, (50, 50, 60, 255), (0, 0, 100, 100), border_radius=10)
            pygame.draw.rect(self.portrait, (100, 100, 120, 255), (0, 0, 100, 100), width=3, border_radius=10)

        
        font_path = os.path.join("view", "assets", "Font", "Kenney Future.ttf")
        self.font = pygame.font.Font(font_path, 20)
        self.small_font = pygame.font.Font(font_path, 14)

     
        self.tap_sound = pygame.mixer.Sound(os.path.join("view", "assets", "Sounds", "tap-a.ogg"))
        self.tap_sound.set_volume(0.2)

    def update(self):
        """
        Update typewriter text animation progress and character reveal timer.
        Plays typing sound for each new character.
        """
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        text = self.dialogues[self.current_line]

        if self.current_char < len(text):
            self.char_timer += dt
            if self.char_timer >= self.text_speed:
                chars_to_add = int(self.char_timer // self.text_speed)
                self.current_char = min(self.current_char + chars_to_add, len(text))
                self.char_timer = 0

                if text[self.current_char - 1] != ' ':
                    self.tap_sound.play()

    def get_wrapped_lines(self, text, max_width):
        """
        Automatically wrap text into multiple lines to fit within a given width.

        Args:
            text: Input text string to wrap
            max_width: Maximum pixel width per line

        Returns:
            list[str]: List of wrapped text lines
        """
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        return lines

    def draw_text_with_shadow(self, surface, text, font, color, x, y):
        """
        Render text with a black drop shadow for better readability.

        Args:
            surface: Target surface to draw on
            text: Text string to render
            font: Font used for rendering
            color: Text color (RGB)
            x: X position
            y: Y position
        """
       
       
        shadow_surface = font.render(text, True, (0, 0, 0))
        surface.blit(shadow_surface, (x + 2, y + 2))
  
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))

    def draw(self, screen):
        """
        Render the full intro UI: background, animated dialog box, portrait,
        typewriter text, and prompt hint.
        """
       
        screen.blit(self.bg, (0, 0))
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((253, 245, 230, 40))  
        screen.blit(overlay, (0, 0))

    
        time_elapsed = pygame.time.get_ticks() - self.start_time
        anim_duration = 400.0  
        progress = min(time_elapsed / anim_duration, 1.0)
       
        ease_out_y = 1 - (1 - progress) * (1 - progress)

   
        box_width, box_height = 700, 160
        box_x = (self.width - box_width) // 2

        target_box_y = self.height - box_height - 30
        start_box_y = self.height + 50
        box_y = start_box_y + (target_box_y - start_box_y) * ease_out_y

    
        dialog_bg = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(dialog_bg, (245, 222, 179, 220), (0, 0, box_width, box_height), border_radius=8)
  
        pygame.draw.rect(dialog_bg, (139, 115, 85, 200), (0, 0, box_width, box_height), width=2, border_radius=8)
        screen.blit(dialog_bg, (box_x, box_y))

    
        if progress >= 1.0:
     
            portrait_x = box_x + 30
            portrait_y = box_y + 30
            screen.blit(self.portrait, (portrait_x, portrait_y))
  
            pygame.draw.rect(screen, (200, 200, 200), (portrait_x - 2, portrait_y - 2, 104, 104), 2)

         
            text_start_x = portrait_x + 100 + 30
            text_start_y = box_y + 30
            max_text_width = box_width - (text_start_x - box_x) - 30
            line_spacing = 30

            full_text = self.dialogues[self.current_line]
            wrapped_lines = self.get_wrapped_lines(full_text, max_text_width)

            chars_left_to_draw = self.current_char

            for i, line in enumerate(wrapped_lines):
                if chars_left_to_draw <= 0:
                    break
                if chars_left_to_draw >= len(line):
                    display_text = line
                    chars_left_to_draw -= len(line)
                else:
                    display_text = line[:chars_left_to_draw]
                    chars_left_to_draw = 0

       
                self.draw_text_with_shadow(screen, display_text, self.font, (255, 255, 255), text_start_x,
                                           text_start_y + i * line_spacing)

       
            if self.current_char >= len(full_text):
          
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    self.draw_text_with_shadow(screen, "Click or Space...", self.small_font, (200, 200, 0),
                                               box_x + box_width - 200, box_y + box_height - 30)

    def handle_event(self, event):
        """
        Handle user input to advance dialogue or skip intro.

        Args:
            event: Pygame input event

        Returns:
            str: 'done' when all dialogues are completed; None otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.advance()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                return self.advance()
            elif event.key == pygame.K_ESCAPE:
                return "done"
        return None

    def advance(self):
        """
        Advance to next character or line. Skip typing if clicked mid-line.

        Returns:
            str: 'done' if all lines are finished; None otherwise
        """
        text = self.dialogues[self.current_line]
        if self.current_char < len(text):
            self.current_char = len(text)
            return None
        else:
            self.current_line += 1
            self.current_char = 0
            if self.current_line >= len(self.dialogues):
                return "done"
            return None

    def reset(self):
        """Reset dialogue sequence to the first line and restart animations."""
        self.current_line = 0
        self.current_char = 0
        self.start_time = pygame.time.get_ticks() 
        self.last_update_time = pygame.time.get_ticks()