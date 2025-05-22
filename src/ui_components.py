import pygame
import os

class Button: # Keep the original Button class as it might be used elsewhere or for other UI
    def __init__(self, x, y, width, height, text, color, text_color, font_size=30, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        
        if not pygame.font.get_init():
            pygame.font.init()
            
        self.font = pygame.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
                    return True
        return False

class ImageButton:
    def __init__(self, x, y, width, height, image_path, hover_image_path=None, action=None, text="", placeholder_text="Button"):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.is_hovered = False
        self.normal_image = None
        self.hover_image = None
        self.text = text 
        self.placeholder_text = placeholder_text

        if not pygame.font.get_init(): 
            pygame.font.init()
        self.font = pygame.font.Font(None, 30) 

        try:
            self.normal_image = pygame.image.load(image_path)
            self.normal_image = pygame.transform.scale(self.normal_image, (width, height))
        except pygame.error as e:
            print(f"Warning: Failed to load image at {image_path}. Error: {e}")
            self.normal_image = self._create_placeholder(width, height, (100, 100, 100), self.placeholder_text)

        if hover_image_path:
            try:
                self.hover_image = pygame.image.load(hover_image_path)
                self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
            except pygame.error as e:
                print(f"Warning: Failed to load hover image at {hover_image_path}. Error: {e}")
                self.hover_image = self._create_placeholder(width, height, (150, 150, 150), self.placeholder_text)
        else:
            # If no hover image, create a slightly different placeholder or use normal for hover effect
            # For simplicity, we can just make hover_image same as normal if not provided,
            # or create a modified version of normal_image (e.g. brighter)
             pass # self.hover_image will be None, draw will handle it

        if self.text:
            self._render_text_on_images()


    def _create_placeholder(self, width, height, color, text_on_placeholder):
        placeholder_surface = pygame.Surface((width, height))
        placeholder_surface.fill(color)
        
        if text_on_placeholder: 
            font = pygame.font.Font(None, 36) 
            text_surf = font.render(text_on_placeholder, True, (255, 255, 255)) 
            text_rect = text_surf.get_rect(center=(width // 2, height // 2))
            placeholder_surface.blit(text_surf, text_rect)
        return placeholder_surface

    def _render_text_on_images(self):
        if not self.text:
            return
        text_color = (255, 255, 255) 

        if self.normal_image:
            img_copy_normal = self.normal_image.copy()
            lines = self.text.split('\\n') 
            y_offset = 0
            if len(lines) > 1 : y_offset = - (self.font.get_height() * (len(lines) -1) /2) 
            
            for i, line in enumerate(lines):
                text_surf = self.font.render(line, True, text_color)
                text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2 + y_offset + i * self.font.get_height()))
                img_copy_normal.blit(text_surf, text_rect)
            self.normal_image = img_copy_normal

        if self.hover_image and self.hover_image is not self.normal_image : # Check if hover_image is distinct
            img_copy_hover = self.hover_image.copy()
            y_offset = 0 # Recalculate for hover image if needed
            if len(lines) > 1 : y_offset = - (self.font.get_height() * (len(lines) -1) /2)

            for i, line in enumerate(lines):
                text_surf = self.font.render(line, True, text_color) 
                text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2 + y_offset + i * self.font.get_height()))
                img_copy_hover.blit(text_surf, text_rect)
            self.hover_image = img_copy_hover


    def draw(self, screen):
        current_image = self.normal_image
        if self.is_hovered and self.hover_image:
            current_image = self.hover_image
        
        if current_image: # Ensure there is an image to draw
            screen.blit(current_image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: 
                if self.action:
                    self.action()
                return True 
        return False 

    def update_text(self, new_text):
        self.text = new_text
        # Simplified: re-create images with new text.
        # This assumes original image_path is stored or placeholders are always fine to recreate.
        # For this version, we'll assume it's okay to re-render on current surfaces or re-create placeholders.
        # A more robust solution might store original paths or have separate methods for image loading.
        
        # Re-create placeholders if normal_image was a placeholder
        # This check is heuristic. A better way: self.is_placeholder flag set during __init__.
        is_placeholder = not hasattr(self, 'original_image_path') or self.original_image_path is None
        
        if is_placeholder: # If it was a placeholder, recreate it with new text
            self.normal_image = self._create_placeholder(self.rect.width, self.rect.height, (100,100,100), self.placeholder_text) # Recreate placeholder before rendering text
            if self.hover_image: # If hover image was also placeholder-based
                self.hover_image = self._create_placeholder(self.rect.width, self.rect.height, (150,150,150), self.placeholder_text)
        # else:
            # If loaded from file, ideally reload image then render text.
            # For now, this will render on top of already text-rendered image if not placeholder.
            # This part needs refinement if images are complex and text updates frequently.

        self._render_text_on_images()

class HealthBar:
    def __init__(self, x, y, width, height, max_hp):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_hp = max_hp
        self.current_hp = max_hp  # Start with full HP
        
        self.border_color = (50, 50, 50)  # Dark gray
        self.health_color_good = (0, 255, 0)  # Green
        self.health_color_medium = (255, 255, 0)  # Yellow
        self.health_color_low = (255, 0, 0)  # Red
        self.background_color = (100, 100, 100)  # Gray background for the bar

        if not pygame.font.get_init(): # Ensure font module is initialized
            pygame.font.init()
        self.font = pygame.font.Font(None, 24)  # Font for HP text

    def update_hp(self, new_hp_value):
        self.current_hp = max(0, min(new_hp_value, self.max_hp))

    def draw(self, screen):
        # Draw the background rectangle
        pygame.draw.rect(screen, self.background_color, self.rect)

        # Calculate health fill width
        if self.max_hp > 0 : # Avoid division by zero if max_hp is somehow 0
            fill_width = (self.current_hp / self.max_hp) * self.rect.width
        else:
            fill_width = 0
        
        fill_width = max(0, fill_width) # Ensure fill_width is not negative

        # Determine health color
        if self.max_hp > 0:
            hp_percentage = self.current_hp / self.max_hp
        else:
            hp_percentage = 0

        if hp_percentage > 0.6:
            color = self.health_color_good
        elif hp_percentage > 0.3:
            color = self.health_color_medium
        else:
            color = self.health_color_low
        
        # Create and draw the health fill rectangle
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(fill_width), self.rect.height)
        pygame.draw.rect(screen, color, fill_rect)

        # Draw the border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)  # Border thickness 2

        # Render and display HP text (e.g., "80/100")
        hp_text = f"{int(self.current_hp)}/{int(self.max_hp)}"
        text_surf = self.font.render(hp_text, True, (255, 255, 255))  # White text
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
```
