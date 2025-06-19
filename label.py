import pygame

class Label:
    def __init__(self, text, pos, screenPtr, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80), visible=True):
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.color = color
        self.visible = visible
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(None, self.font_size)
        self.screenPtr = screenPtr

        ## Register this Label with the screen
        if not hasattr(screenPtr, 'allLabels'):
            screenPtr.allLabels = []
        screenPtr.allLabels.append(self)

        self.renderText()

    def moveToCenter(self):
        screen_size = pygame.display.get_surface().get_size()
        screen_rect = pygame.Rect(0, 0, *screen_size)
        self.text_rect = self.text_surface.get_rect(center=screen_rect.center)
        self.shadow_rect = self.text_rect.move(2, 2)
        self.pos = self.text_rect.topleft

    def setVisible(self,visible):
        self.visible = visible

    def renderText(self):
        shadow_offset = (2, 2)
        shadow_color = (30, 30, 30)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(topleft=self.pos)
        self.shadow_surface = self.font.render(self.text, True, shadow_color)
        self.shadow_rect = self.text_rect.move(shadow_offset)

    def draw(self, screen):
        if not self.visible:
            return
        # Draw shadow
        screen.blit(self.shadow_surface, self.shadow_rect)
        # Draw text
        screen.blit(self.text_surface, self.text_rect)
    
    def updateText(self, new_text):
        self.text = new_text
        self.renderText()