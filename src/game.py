import pygame
from src.ui_components import Button, ImageButton, HealthBar # Import HealthBar
from src.sound_manager import SoundManager
from src.player import Player
from src.question_loader import QuestionLoader 

class Game:
    def __init__(self, screen_width, screen_height):
        self.is_running = True
        self.current_scene = "title_screen"
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_BLUE = (173, 216, 230)
        self.GREEN = (0, 200, 0)
        self.DARK_GRAY = (50, 50, 50) 
        self.RED = (200, 0, 0) 

        # Initialize SoundManager
        self.sound_manager = SoundManager(base_path_audio="assets/audio/")
        self.sound_manager.load_sound("begin", "begin.mp3")
        self.sound_manager.load_sound("start", "start.mp3")
        self.sound_manager.load_sound("correct", "correct.mp3") 
        self.sound_manager.load_sound("wrong", "wrong.mp3")
        self.sound_manager.play_sound("begin")

        # Player Initialization
        player_initial_x = self.screen_width // 2
        player_initial_y = self.screen_height + 80 // 2 
        self.player = Player(x=player_initial_x, y=player_initial_y, base_path_graphics="assets/graphics/")
        self.player_target_y = self.screen_height - 150 
        self.player_animation_speed = 2 

        # HealthBar Initialization
        hb_width = 200
        hb_height = 25
        hb_x = 10 
        hb_y = 10
        # Player.hp is initial HP (100), which HealthBar will take as current and max
        self.health_bar = HealthBar(hb_x, hb_y, hb_width, hb_height, self.player.hp) 

        # Question Logic Initialization
        self.question_loader = QuestionLoader()
        self.question_loader.load_questions("assets/questions/questions.txt")
        self.current_question_index = 0
        self.current_question = None
        self.feedback_text = ""
        self.feedback_text_timer = 0
        self.feedback_duration = 120 

        # Fonts
        self.question_font = pygame.font.Font(None, 42) 
        self.answer_font = pygame.font.Font(None, 28) 
        self.feedback_font = pygame.font.Font(None, 48)

        # Door Buttons (ImageButton)
        door_width, door_height = 150, 250
        padding = 100 
        total_doors_width = (door_width * 2) + padding
        left_door_x = (screen_width - total_doors_width) // 2
        right_door_x = left_door_x + door_width + padding
        door_y = screen_height - door_height - 70 

        self.door1 = ImageButton(
            left_door_x, door_y, door_width, door_height,
            "assets/graphics/door_left.png", 
            hover_image_path=None, 
            action=lambda: self.select_answer("A1"),
            text="", 
            placeholder_text="Door 1" 
        )
        self.door2 = ImageButton(
            right_door_x, door_y, door_width, door_height,
            "assets/graphics/door_right.png", 
            hover_image_path=None,
            action=lambda: self.select_answer("A2"),
            text="", 
            placeholder_text="Door 2"
        )
        self.door1.font = self.answer_font 
        self.door2.font = self.answer_font

        button_width = 250
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        button_y = (self.screen_height - button_height) // 2 + 150
        self.start_button = Button(
            x=button_x, y=button_y, width=button_width, height=button_height,
            text="Start Game", color=self.GREEN, text_color=self.WHITE,
            font_size=40, action=self.start_game_action
        )

    def start_game_action(self):
        print("Start button clicked! Starting player enter animation...")
        self.sound_manager.play_sound("start")
        self.player.x = self.screen_width // 2
        self.player.y = self.screen_height + self.player.rect.height // 2
        self.player.rect.center = (self.player.x, self.player.y)
        self.current_scene = "player_enter_animation"

    def start_question_scene(self):
        self.player.rect.centery = self.player_target_y 
        self.player.y = self.player_target_y 
        self.feedback_text = "" 
        self.feedback_text_timer = 0
        self.health_bar.update_hp(self.player.hp) # Ensure HB is synced at start of scene
        self.load_current_question()

    def load_current_question(self):
        self.current_question = self.question_loader.get_question(self.current_question_index)
        if self.current_question is None:
            print("No more questions. Game Over or Victory scene next.")
            self.current_scene = "victory" 
            self.sound_manager.speak("You have answered all questions! Congratulations!", lang="en") 
            return False
        
        self.door1.update_text(self.current_question.answer1_text.replace(" ", "\\n"))
        self.door2.update_text(self.current_question.answer2_text.replace(" ", "\\n"))

        self.sound_manager.speak(self.current_question.text, lang="th")
        self.sound_manager.speak(f"Door 1: {self.current_question.answer1_text}", lang="th")
        self.sound_manager.speak(f"Door 2: {self.current_question.answer2_text}", lang="th")
        return True

    def select_answer(self, selected_id):
        if not self.current_question or self.feedback_text_timer > 0: 
            return

        is_correct = (selected_id == self.current_question.correct_answer_id)
        
        if is_correct:
            self.feedback_text = "Correct!"
            self.sound_manager.play_sound("correct")
            self.player.heal(10) 
            print(f"Answer {selected_id} is correct. Player HP: {self.player.hp}")
        else:
            self.feedback_text = "Wrong!"
            self.sound_manager.play_sound("wrong")
            self.player.take_damage(20) 
            print(f"Answer {selected_id} is wrong. Correct was {self.current_question.correct_answer_id}. Player HP: {self.player.hp}")
        
        self.health_bar.update_hp(self.player.hp) # Update health bar after HP change
        self.feedback_text_timer = self.feedback_duration 
        self.current_question_index += 1
        
        # Check for game over condition
        if self.player.hp <= 0:
            self.current_scene = "game_over"
            self.sound_manager.speak("Oh no, you have run out of health! Game Over.", lang="en")
            print("Player has run out of HP. Game Over.")


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            if self.current_scene == "title_screen":
                self.start_button.is_clicked(event) 
            elif self.current_scene == "question_scene":
                if self.feedback_text_timer <= 0 and self.player.hp > 0: # Prevent action if feedback or game over
                    self.door1.handle_event(event)
                    self.door2.handle_event(event)
            elif self.current_scene == "game_over" or self.current_scene == "victory":
                # Optional: Allow click to restart or exit
                if event.type == pygame.MOUSEBUTTONDOWN:
                     # For now, just quit or go to title. Could add a restart button.
                     # self.current_scene = "title_screen" 
                     # self.reset_game_state() # Would need a method to reset HP, questions etc.
                     self.is_running = False # Simple exit for now
    
    def run(self, screen):
        self.handle_events() 

        if not self.is_running:
            return

        if self.current_scene == "title_screen":
            screen.fill(self.LIGHT_BLUE)
            title_font = pygame.font.Font(None, 90)
            title_text_surface = title_font.render("Quest of Knowledge", True, self.BLACK)
            title_text_rect = title_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
            screen.blit(title_text_surface, title_text_rect)
            self.start_button.draw(screen)
        
        elif self.current_scene == "player_enter_animation":
            screen.fill(self.BLACK) 
            self.player.y -= self.player_animation_speed 
            self.player.rect.centery = self.player.y
            self.player.draw(screen)
            if self.player.rect.centery <= self.player_target_y:
                self.player.rect.centery = self.player_target_y
                self.player.y = self.player_target_y
                self.current_scene = "question_scene"
                self.start_question_scene() 
                print("Player animation complete. Transitioning to question scene.")
        
        elif self.current_scene == "question_scene":
            screen.fill(self.DARK_GRAY)
            self.player.draw(screen) 
            self.health_bar.draw(screen) # Draw health bar

            if self.player.hp <= 0: # If HP dropped to 0 during feedback phase before scene change
                self.current_scene = "game_over"
                # TTS for game over already handled in select_answer or will be in game_over scene logic
                # return # Skip rest of question scene drawing if game over
            
            if self.current_question:
                max_text_width = self.screen_width - 40 
                question_lines = []
                words = self.current_question.text.split(' ')
                current_line = ""
                for word in words:
                    test_line = current_line + word + " "
                    if self.question_font.size(test_line)[0] < max_text_width:
                        current_line = test_line
                    else:
                        question_lines.append(current_line.strip())
                        current_line = word + " "
                question_lines.append(current_line.strip())

                line_y_offset = 0
                for i, line_text in enumerate(question_lines):
                    q_surf = self.question_font.render(line_text, True, self.WHITE)
                    q_rect = q_surf.get_rect(center=(self.screen_width // 2, 50 + i * (self.question_font.get_height() + 2) )) 
                    screen.blit(q_surf, q_rect)
                    line_y_offset = 50 + i * (self.question_font.get_height() + 2)

                self.door1.draw(screen)
                self.door2.draw(screen)

            if self.feedback_text_timer > 0:
                self.feedback_text_timer -= 1
                feedback_color = self.GREEN if self.feedback_text == "Correct!" else self.RED
                feedback_surf = self.feedback_font.render(self.feedback_text, True, feedback_color)
                feedback_rect = feedback_surf.get_rect(center=(self.screen_width // 2, line_y_offset + 80)) 
                screen.blit(feedback_surf, feedback_rect)
                if self.feedback_text_timer == 0: 
                    self.feedback_text = "" 
                    if self.player.hp > 0 : # Only load next question if player is alive
                         self.load_current_question() 
                    # If player HP is 0, game over scene will be handled by next frame's run()
            
        elif self.current_scene == "victory":
            screen.fill(self.LIGHT_BLUE)
            font = pygame.font.Font(None, 74)
            text_surface = font.render("Congratulations! You finished the quest!", True, self.BLACK)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
            self.player.draw(screen) 
            self.health_bar.draw(screen) # Show health bar in victory too

        elif self.current_scene == "game_over":
            screen.fill(self.BLACK) # Dark theme for game over
            font_large = pygame.font.Font(None, 74)
            font_small = pygame.font.Font(None, 48)
            
            text_surface_large = font_large.render("Game Over", True, self.RED)
            text_rect_large = text_surface_large.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
            screen.blit(text_surface_large, text_rect_large)
            
            text_surface_small = font_small.render("Click to exit", True, self.WHITE)
            text_rect_small = text_surface_small.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
            screen.blit(text_surface_small, text_rect_small)

            self.player.draw(screen) # Show player's final state
            self.health_bar.draw(screen) # Show final health (empty)
```
