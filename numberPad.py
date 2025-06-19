import pygame
from button import Button

class NumberPad:
    def __init__(self, pos, size, screenPtr, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80)):
        self.pos = pos
        self.size = size
        self.screenPtr = screenPtr
        self.font_size = font_size
        self.color = color
        self.bg_color = bg_color
        self.hover_color = (120, 120, 120)
        self.curr_color = bg_color
        self.font = pygame.font.SysFont(None, self.font_size)
        self.rect = pygame.Rect(pos, size)

        screenPtr.numberPad = self  # Register this NumberPad with the screen
        
        # Create buttons for numbers 1-9 in a 3x3 grid
        self.buttons = []
        for i in range(9):
            btn_text = str(i + 1)
            col = i % 3
            row = i // 3
            btn_pos = (
            pos[0] + col * (size[0] // 3),
            pos[1] + row * (size[1] // 4)
            )
            btn_size = (size[0] // 3 - 10, size[1] // 4 - 10)
            btn = Button(btn_text, btn_pos, btn_size, screenPtr, font_size=font_size,
                 color=color, bg_color=bg_color)
            btn.onClick = lambda text=btn_text: self.onButtonClick(text)
            self.buttons.append(btn)

        # Create button for 0 at the bottom center
        zero_col = 1  # middle column
        zero_row = 3  # bottom row
        zero_text = "0"
        zero_pos = (
            pos[0] + zero_col * (size[0] // 3),
            pos[1] + zero_row * (size[1] // 4)
        )
        zero_size = (size[0] // 3 - 10, size[1] // 4 - 10)
        zero_btn = Button(zero_text, zero_pos, zero_size, screenPtr, font_size=font_size,
                  color=color, bg_color=bg_color)
        zero_btn.onClick = lambda text=zero_text: self.onButtonClick(text)
        self.buttons.append(zero_btn)

        # Create button for '<-' to the right of the 0 button
        clear_col = 2  # rightmost column
        clear_row = 3  # bottom row
        clear_text = "<-"
        clear_pos = (
            pos[0] + clear_col * (size[0] // 3),
            pos[1] + clear_row * (size[1] // 4)
        )
        clear_size = (size[0] // 3 - 10, size[1] // 4 - 10)
        clear_btn = Button(clear_text, clear_pos, clear_size, screenPtr, font_size=font_size,
                           color=color, bg_color=bg_color)

        clear_btn.onClick = lambda text=zero_text: self.onButtonClick(clear_text)
        self.buttons.append(clear_btn)

    def onButtonClick(self, text):
        if hasattr(self.screenPtr, 'allInputs'):
            from mainUI import MainUI
            MainUI.pinInput.onChar(text)

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
        shadow_rect = bg_rect.move(shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=18)
        # Draw background rectangle
        bg_color = (60, 60, 60)
        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=18)