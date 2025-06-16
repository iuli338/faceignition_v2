import pygame
from screen import Screen
from user import User

class Button:

    selectedButton = None

    def __init__(self, text, pos, size, screenPtr, active=True, font_size=48, color=(255, 255, 255), bg_color=(80 , 80, 80), onClick = None):
        self.text = text
        self.pos = pos
        self.size = size
        self.screenPtr = screenPtr
        self.font_size = font_size
        self.color = color
        self.bg_color = bg_color
        self.curr_color = bg_color  # Current color for the button
        self.hover_color = pygame.Color(bg_color) + pygame.Color(40,40,40) # Slightly lighter color for hover effect
        self.font = pygame.font.SysFont(None, self.font_size)
        self.rect = pygame.Rect(pos, size)
        self.renderText()
        self.onClick = onClick  # Placeholder for click handler
        self.active = active
        if not active:
            self.setActive(active)
        self.screenPtr.allButtons.append(self)  # Register this button with the screen

    ####

    def setActive(self,state):
        self.active = state
        if (state):
            self.changeColor((80 , 80, 80))
            self.color = (255, 255, 255)
        else:
            self.changeColor((40, 40, 40))
            self.color = (80, 80, 80)
        self.renderText()


    def onHover(self,event):
        if not self.active: return

        if self.rect.collidepoint(event.pos):
            self.curr_color = self.hover_color
        else:
            self.curr_color = self.bg_color

    def renderText(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Draw shadow
        shadow_offset = (4, 4)
        shadow_color = (30, 30, 30)
        shadow_rect = self.rect.move(shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
        # Draw button
        pygame.draw.rect(screen, self.curr_color, self.rect, border_radius=10)
        screen.blit(self.text_surface, self.text_rect)

    def changeColor(self,newColor):
        self.bg_color = newColor
        self.curr_color = newColor  # Current color for the button
        self.hover_color = pygame.Color(newColor) + pygame.Color(40,40,40) # Slightly lighter color for hover effect

    def userButtonClick(self):
        User.selectUser(self.userButton.user)  # Set the selected user based on button text
        if User.selectedUser is not None:
            if User.selectedUser.name == self.userButton.user.name:
                # Change selected button
                # Deselect the prev selected button
                if Button.selectedButton != None:
                    Button.selectedButton.changeColor((80,80,80))
                # Select the new button
                Button.selectedButton = self
                self.changeColor((239,81,130))
            else:
                self.changeColor((80,80,80))
        else:
            self.changeColor((80,80,80))

    @staticmethod
    def userButtonUpdateColor():
        for button in Screen.currentScreen.allButtons:
            if hasattr(button, 'userButton'):
                button.changeColor((80,80,80))

    def atachUserButton(self, userButton):
        self.userButton = userButton

    #### Static methods to manage buttons

    @staticmethod
    def onMouseButtonDown(event):
        for button in Screen.currentScreen.allButtons:
            if button.rect.collidepoint(event.pos):
                if button.onClick and button.active:
                    button.onClick()
                    Button.onMouseMotion(event)  # Update hover state after click
                    return  # Exit after handling the first button clicked

    @staticmethod
    def onMouseMotion(event):
        for button in Screen.currentScreen.allButtons:
            button.onHover(event)