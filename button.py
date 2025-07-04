import pygame
from screen import Screen
from user import User

class Button:

    selectedButton = None

    selectedBgColor = (239,81,130)

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
        self.inactive_color = pygame.Color(bg_color) - pygame.Color(60, 60, 60)
        self.font = pygame.font.SysFont(None, self.font_size)
        self.rect = pygame.Rect(pos, size)
        self.renderText()
        self.onClick = onClick  # Placeholder for click handler
        self.active = active
        if not active:
            self.setActive(active)
        self.screenPtr.allButtons.append(self)  # Register this button with the screen
        self.visible = True

    ####

    def setActive(self,state):
        self.active = state
        if (state):
            self.changeColor(self.bg_color)
            self.color = (255, 255, 255)
        else:
            self.changeColor(self.inactive_color)
            self.color = (80, 80, 80)
        self.renderText()

    def onHover(self,event):
        if not self.visible:
            return
        if event is None:
            for button in Screen.currentScreen.allButtons:
                button.curr_color = button.bg_color
            return
        
        if not self.active: return

        if self.rect.collidepoint(event.pos):
            self.curr_color = self.hover_color
        else:
            self.curr_color = self.bg_color

    def renderText(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        if not self.visible:
            return
        # Draw shadow
        shadow_offset = (4, 4)
        shadow_color = (30, 30, 30)
        shadow_rect = self.rect.move(shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
        # Draw button
        pygame.draw.rect(screen, self.curr_color, self.rect, border_radius=10)
        screen.blit(self.text_surface, self.text_rect)

    def changeBgColor(self,newColor):
        self.bg_color = newColor
        self.curr_color = newColor  # Current color for the button
        self.hover_color = pygame.Color(newColor) + pygame.Color(40,40,40) # Slightly lighter color for hover effect
        self.inactive_color = pygame.Color(self.bg_color) - pygame.Color(60, 60, 60)

    def changeColor(self,newColor):
        self.curr_color = newColor  # Current color for the button
        self.hover_color = pygame.Color(newColor) + pygame.Color(40,40,40) # Slightly lighter color for hover effect

    def userButtonClick(self):
        User.selectUser(self.userButton.user)  # Set the selected user based on button text
        if User.selectedUser is not None:
            if User.selectedUser.name == self.userButton.user.name:
                # Change selected button
                # Deselect the prev selected button
                if Button.selectedButton != None:
                    Button.selectedButton.changeBgColor(pygame.Color(80, 80, 80))
                # Select the new button
                Button.selectedButton = self
                self.changeBgColor(Button.selectedBgColor)
            else:
                self.changeBgColor(pygame.Color(80, 80, 80))
        else:
            self.changeBgColor(pygame.Color(80, 80, 80))

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
                if button.onClick and button.active and button.visible:
                    button.onClick()
                    Button.onMouseMotion(event)  # Update hover state after click
                    return  # Exit after handling the first button clicked

    @staticmethod
    def onMouseMotion(event):
        for button in Screen.currentScreen.allButtons:
            button.onHover(event)

class IconButton():
    def __init__(self, icon_path, pos, screenPtr, visible = True, onClick=None, active=True):
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.saved_icon = self.icon.copy()
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.screenPtr = screenPtr
        self.onClick = onClick
        self.active = active
        self.visible = visible  # Icon buttons are visible by default

        if not hasattr(self.screenPtr, 'allIconButtons'):
            self.screenPtr.allIconButtons = []
        self.screenPtr.allIconButtons.append(self)  # Register this button with the screen

        # Make the icon lighter on hover by creating a lighter surface
        self.lighter_icon = self.icon.copy()
        self.lighter_icon.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.icon_hover = self.lighter_icon

    def onHover(self, event):
        if not self.active:
            return
        if self.rect.collidepoint(event.pos):
            self.icon = self.icon_hover
        else:
            self.icon = self.saved_icon
            
    def draw(self, screen):
        if not self.visible:
            return
        screen.blit(self.icon, self.rect.topleft)

    def setVisible(self,state):
        self.visible = state

    def setActive(self,active):
        self.active = active

    @staticmethod
    def onMouseButtonDown(event):
        from photoScreen import PhotoScreen  # Import PhotoScreen to access its attributes
        if Screen.currentScreen.name == "Photo" and not PhotoScreen.initialized:
            return  # Do not handle clicks if PhotoScreen is not initialized
        if not hasattr(Screen.currentScreen, 'allIconButtons'):
            return
        for iconButton in Screen.currentScreen.allIconButtons:
            if iconButton.rect.collidepoint(event.pos):
                if iconButton.onClick and iconButton.active and iconButton.visible:
                    iconButton.onClick()
                    IconButton.onMouseMotion(event)  # Update hover state after click
                    return  # Exit after handling the first button clicked

    @staticmethod
    def onMouseMotion(event):
        if event is None:
            for iconButton in Screen.currentScreen.allIconButtons:
                iconButton.icon = iconButton.saved_icon
            return
        if not hasattr(Screen.currentScreen, 'allIconButtons'):
            return
        for iconButton in Screen.currentScreen.allIconButtons:
            iconButton.onHover(event)