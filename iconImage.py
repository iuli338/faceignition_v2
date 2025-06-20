import pygame

class IconImage:

    def __init__(self,imgPath,pos,screenPtr):
        self.imgPath = imgPath
        self.pos = pos
        self.img = pygame.image.load(imgPath)
        self.rect = pygame.Rect(pos, self.img.get_size())
        self.screenPtr = screenPtr

        if not hasattr(self.screenPtr, 'allIconImages'):
            self.screenPtr.allIconImages = []
        self.screenPtr.allIconImages.append(self)  # Register this button with the screen
    
    def draw(self,screen):
        screen.blit(self.img, self.rect.topleft)
    