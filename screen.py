import time
from user import UserContainer
from photoScreen import PhotoScreen

class Screen:

    allScreens = []
    currentScreen = None

    logoTime = 1.0 # Duration for the logo screen in seconds

    def __init__(self, name, updateFunction=None, background_image=None):
        self.name = name
        self.allButtons = []
        self.background_color = (40, 40, 40)
        self.updateFunction = updateFunction  # Function to call for updates, if any
        self.background_image = background_image  # Optional background image
        Screen.allScreens.append(self)

    @staticmethod
    def getScreenByName(name):
        for screen in Screen.allScreens:
            if screen.name == name:
                return screen
        return None
    
    @staticmethod
    def setCurrentScreen(screen):
        if isinstance(screen, Screen):
            # If screen is already a Screen object, set it directly
            Screen.currentScreen = screen
        else:
            # If screen is a string, find the Screen object by name
            Screen.currentScreen = Screen.getScreenByName(screen)
        if Screen.currentScreen is None:
            raise ValueError(f"Screen '{screen}' not found.")
        
    @staticmethod
    def updateCurrentScreen():
        if Screen.currentScreen is None:
            raise ValueError("No current screen set.")
        if Screen.currentScreen.updateFunction is None:
            return
        # Call the update function of the current screen if it exists
        Screen.currentScreen.updateFunction()

    @staticmethod
    def drawCurrentScreen(screen):
        if Screen.currentScreen is None:
            raise ValueError("No current screen set.")
        # Draw the background color or image
        if Screen.currentScreen.background_image:
            screen.blit(Screen.currentScreen.background_image, (0, 0))
        else:
            screen.fill(Screen.currentScreen.background_color)
        
        # Draw the number pad if it exists
        if hasattr(Screen.currentScreen, 'numberPad'):
            Screen.currentScreen.numberPad.draw(screen)

        # Draw the nowebcam image if the current screen is the photo screen
        if Screen.currentScreen.name == "Photo":
            if PhotoScreen.webcam_recorder is not None and PhotoScreen.webcam_recorder.isOpened():
                if PhotoScreen.frame is not None:
                    # If the webcam is available and there is a frame, draw the webcam frame
                    screen.blit(PhotoScreen.frame, (0, 0))
                else:
                    # If the frame is not available, draw the no webcam image
                    screen.blit(PhotoScreen.noWebCamImage, (0, 0))
            else:
                # If the webcam is not available, draw the no webcam image
                screen.blit(PhotoScreen.noWebCamImage, (0, 0))

        # Draw the input box if it exists
        if hasattr(Screen.currentScreen, 'inputBox'):
            Screen.currentScreen.inputBox.draw(screen)

        # Draw label if it exists
        if hasattr(Screen.currentScreen, 'allLabels'):
            for label in Screen.currentScreen.allLabels:
                label.draw(screen)

        # Draw all buttons on the current screen
        for button in Screen.currentScreen.allButtons:
            button.draw(screen)

        # Draw the user container if it exists and the current screen is the main screen
        if Screen.currentScreen.name == "Main":
           UserContainer.draw(screen)

        if hasattr(Screen.currentScreen, 'allIconButtons'):
            for iconButton in Screen.currentScreen.allIconButtons:
                iconButton.draw(screen)

#### Update function for the screens

def logoScreenUpdate():
    if not hasattr(logoScreenUpdate, "start_time"):
        logoScreenUpdate.start_time = time.time()

    elapsed = time.time() - logoScreenUpdate.start_time
    if elapsed >= Screen.logoTime:
        # Change to the Pin screen after the logo duration
        Screen.setCurrentScreen("Pin")

PASS = "1234" # Placeholder for the PIN

def pinScreenUpdate():
    if Screen.currentScreen.inputBox.text == PASS:
        # If the PIN is correct, switch to the main screen
        Screen.setCurrentScreen("Main")
    elif len(Screen.currentScreen.inputBox.text) == Screen.currentScreen.inputBox.maxChar:
        # If the PIN is incorrect, reset the input box
        Screen.currentScreen.inputBox.text = ""
    pass

def photoScreenUpdate():
    pass

def mainScreenUpdate():
    pass