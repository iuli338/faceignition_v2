import pygame

class InputBox:
    def __init__(self, pos, size, screenPtr, maxChar = 4, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80)):
        self.pos = pos
        self.size = size
        self.screenPtr = screenPtr
        self.maxChar = maxChar
        self.font_size = font_size
        self.color = color
        self.bg_color = bg_color
        self.hover_color = (120, 120, 120)
        self.curr_color = bg_color
        self.font = pygame.font.SysFont(None, self.font_size)
        self.rect = pygame.Rect(pos, size)
        self.text = ""

        # Register this InputBox with the screen
        screenPtr.inputBox = self

    def onChar(self,char):
        if char == "<-":  # Handle backspace
            if self.text:
                self.text = self.text[:-1]
            return
        if len(self.text) < self.maxChar:
            self.text += char

    def draw(self, screen):
        # Draw shadow for the background rectangle
        margin = 16
        shadow_offset = (6, 6)
        shadow_color = (30, 30, 30)
        bg_rect = pygame.Rect(
            self.pos[0] - margin,
            self.pos[1] - margin,
            self.size[0] + 2 * margin,
            self.size[1] + 2 * margin
        )
        pygame.draw.rect(screen, shadow_color, bg_rect, border_radius=10)
        
        # Draw the input box background and text
        pygame.draw.rect(screen, self.curr_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)