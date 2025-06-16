import pygame
from screen import Screen
from button import Button
from numberPad import NumberPad
from inputBox import InputBox
from label import Label
from screen import logoScreenUpdate, pinScreenUpdate, mainScreenUpdate
from user import User, UserState, UserContainer
from photoScreen import PhotoScreen

class MainUI:

    addBtn = None
    removeBtn = None
    renameBtn = None
    makePhotos = None
    ignitionBtn = None

    #### Initialize Screens and Buttons
    def initUI():
        ## Logo Screen
        logoImage = pygame.image.load("res/logo_back.jpg").convert_alpha()  # Load logo image
        logoScreen = Screen("Logo", logoScreenUpdate, logoImage)
        ## Pin Screen
        pinScreen = Screen("Pin",pinScreenUpdate)
        NumberPad((200, 100), (200, 300), pinScreen, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80))
        InputBox((480, 100), (200, 50), pinScreen, maxChar=4, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80))
        ## Main Screen
        backgroundImage = pygame.image.load("res/backround_image.jpg").convert_alpha()  # Load main screen background image
        mainScreen = Screen("Main",mainScreenUpdate,backgroundImage)
        Label("Users:", (100, 110), mainScreen, font_size=32, color=(255, 255, 255))

        MainUI.addBtn = Button("Add User", (520, 100), (200, 50), mainScreen, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.addBtn.onClick = lambda: UserContainer.addUser()  # Add a new user when clicked
        MainUI.removeBtn = Button("Remove User", (520, 170), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.removeBtn.onClick = lambda: UserContainer.removeUser(User.selectedUser)  # Remove selected user
        MainUI.renameBtn = Button("Rename User", (520, 240), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.makePhotos = Button("Make Photos", (520, 310), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.makePhotos.onClick = lambda: Screen.setCurrentScreen("Photo")  # Switch to photo screen when clicked
        MainUI.ignitionBtn = Button("FaceIgnition", (280, 310), (210, 50), mainScreen, font_size=32, color=(255, 255, 255), bg_color=(255, 150, 79))
        
        # Init the user container
        for user in User.allUsers:
            UserContainer.addUserButton(user, mainScreen)

        photoScreen = Screen("Photo", PhotoScreen.photoScreenUpdate)  # Placeholder for photo screen
        PhotoScreen.init()  # Initialize the photo screen (webcam, etc.)

        Screen.currentScreen = logoScreen
    
    @staticmethod
    def UpdateLeftButtons():
        if User.selectedUser is None:
            MainUI.removeBtn.setActive(False)
            MainUI.renameBtn.setActive(False)
            MainUI.makePhotos.setActive(False)
        else:
            MainUI.removeBtn.setActive(True)
            MainUI.renameBtn.setActive(True)
            if User.selectedUser.state == UserState.NO_PHOTOS:
                MainUI.makePhotos.setActive(True)

    def makeUserClickHandler(button):
        def handler():
            button.userButtonClick()
            MainUI.UpdateLeftButtons()
        return handler 