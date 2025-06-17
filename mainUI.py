import pygame
from screen import Screen
from button import Button, IconButton
from numberPad import NumberPad
from inputBox import InputBox
from label import Label
from screen import logoScreenUpdate, pinScreenUpdate, mainScreenUpdate
from training import Training
from user import User, UserState, UserContainer
from photoScreen import PhotoScreen
from facerecognitionScreen import Facerecognition

class MainUI:

    addBtn = None
    removeBtn = None
    renameBtn = None
    makePhotos = None
    ignitionBtn = None

    photoNrLabel = None
    photoSubj = None
    checkBtn = None

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
        MainUI.makePhotos.onClick = MainUI.makePhotoClickHandler()
        MainUI.ignitionBtn = Button("FaceIgnition", (280, 310), (210, 50), mainScreen, font_size=32, color=(255, 255, 255), bg_color=(255, 150, 79))
        MainUI.ignitionBtn.onClick = MainUI.makeFaceIgnitionHandler()
        
        # Init the user container
        for user in User.allUsers:
            UserContainer.addUserButton(user, mainScreen)

        photoScreen = Screen("Photo", PhotoScreen.photoScreenUpdate)  # Placeholder for photo screen
        PhotoScreen.init()  # Initialize the photo screen (webcam, etc.)
        MainUI.photoSubj = Label("Making photos for: ", (10, 10), photoScreen, font_size=32, color=(239,81,130)) # Label to show the name of the subject user
        MainUI.photoNrLabel = Label("Photos taken: 0", (10, 40), photoScreen, font_size=32, color=(239,81,130)) # Label to show number of photos taken
        IconButton("res/camera.png", (600, 150), photoScreen, onClick=lambda: PhotoScreen.makePhoto())  # Camera icon button
        cancelBtn = IconButton("res/cancel.png", (20, 150), photoScreen)  # Cancel button to return to main screen
        cancelBtn.onClick = MainUI.makePhotoCancelHandler()  # Set the cancel button click handler
        MainUI.checkBtn = IconButton("res/bifa.png", (320, 300), photoScreen, visible=False)  # Check button to confirm photo
        MainUI.checkBtn.onClick = MainUI.makeCheckHandler()

        trainScreen = Screen("Train", background_image=backgroundImage, updateFunction=Training.trainingScreenUpdate)
        trainLabel = Label("Training",(0,0),trainScreen,font_size=64, color=(255,255,255))
        trainLabel.moveToCenter()

        faceRecScreen = Screen("FaceRec", updateFunction=Facerecognition.facerecognitionScreenUpdate)

        driveSafeScreen = Screen("Drive Safe",background_image=backgroundImage)
        driveSafeLabel = Label("Drive Safe!", (0,0), driveSafeScreen, font_size=128, color=(255,255,255))
        driveSafeLabel.moveToCenter()
        backToMainBtn = IconButton("res/sageata.png",(320,320),driveSafeScreen,onClick= lambda:Screen.setCurrentScreen("Main"))

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
            MainUI.makePhotos.setActive(True)

    def makeUserClickHandler(button):
        def handler():
            button.userButtonClick()
            MainUI.UpdateLeftButtons()
        return handler
    
    def makePhotoClickHandler():
        def handler():
            Screen.setCurrentScreen("Photo")
            PhotoScreen.reset()
        return handler
    
    def makePhotoCancelHandler():
        def handler():
            Screen.setCurrentScreen("Main")
            PhotoScreen.initialized = False  # Reset the photo screen state
            Button.onMouseMotion(None)  # Update hover state after click
        return handler
    
    def makeCheckHandler():
        def handler():
            PhotoScreen.savePhotos()
            Screen.setCurrentScreen("Train")
        return handler
    
    def makeFaceIgnitionHandler():
        def handler():
            Screen.setCurrentScreen("FaceRec")
            Facerecognition.init()
        return handler

