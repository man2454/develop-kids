import pygame
import os

class Player:
    def __init__(self, x, y, base_path_graphics="assets/graphics/"):
        self.x = x
        self.y = y
        self.hp = 100  # Initial HP
        self.base_path_graphics = base_path_graphics
        self.speed = 5  # Movement speed

        self.image_path = os.path.join(self.base_path_graphics, "player_back.png")

        try:
            self.image = pygame.image.load(self.image_path)
            # Scale the loaded image to a consistent size
            self.image = pygame.transform.scale(self.image, (50, 80)) # Width, Height
            self.rect = self.image.get_rect(center=(self.x, self.y))
            print(f"Player image loaded successfully from {self.image_path}")
        except pygame.error as e:
            print(f"Warning: Failed to load player image at {self.image_path}. Error: {e}")
            # Create a placeholder surface if image fails to load
            self.image = pygame.Surface((50, 80))  # Width, Height
            self.image.fill((0, 0, 255))  # Blue color for placeholder
            
            # Optional: Add a small border or text to the placeholder for better visibility
            placeholder_font = pygame.font.Font(None, 20) # Small font
            text_surf = placeholder_font.render("Player", True, (255, 255, 255)) # White text
            text_rect = text_surf.get_rect(center=(50 // 2, 80 // 2)) # Center on placeholder
            self.image.blit(text_surf, text_rect)
            
            self.rect = self.image.get_rect(center=(self.x, self.y))
            print("Created a blue placeholder for the player.")

    def draw(self, screen):
        """Draws the player on the given screen."""
        screen.blit(self.image, self.rect.topleft)

    def move(self, dx, dy):
        """Moves the player by dx and dy."""
        self.x += dx * self.speed # Apply speed to movement
        self.y += dy * self.speed # Apply speed to movement
        self.rect.center = (self.x, self.y)

    def take_damage(self, amount):
        """Reduces player's HP by the given amount."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"Player takes {amount} damage. HP is now {self.hp}")

    def heal(self, amount):
        """Increases player's HP by the given amount, up to a maximum (e.g., 100)."""
        self.hp += amount
        if self.hp > 100:  # Assuming max HP is 100
            self.hp = 100
        print(f"Player heals {amount} HP. HP is now {self.hp}")

if __name__ == '__main__':
    # This section is for basic testing of the Player class functionality.
    # It will only run if player.py is executed directly.
    pygame.init()
    pygame.font.init() # Ensure font module is initialized for placeholder text

    # Create a dummy screen for drawing
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Player Class Test")

    # Test player instantiation (image will fail to load, placeholder should be created)
    player = Player(screen_width // 2, screen_height // 2)

    # Test HP manipulation
    player.take_damage(20) # HP should be 80
    player.heal(10)      # HP should be 90
    player.heal(30)      # HP should be 100 (capped)
    player.take_damage(150) # HP should be 0 (floored)

    running = True
    clock = pygame.time.Clock()

    print("\nPlayer Class Test:")
    print("A blue placeholder with 'Player' text should be visible if image loading failed.")
    print("Check console output for HP changes.")
    print("Use arrow keys to move the player (if you uncomment movement handling).")


    # Basic event loop for testing
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Example movement (uncomment to test)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)

        # Drawing
        screen.fill((50, 50, 50))  # Dark grey background
        player.draw(screen)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    print("Player class test finished.")
