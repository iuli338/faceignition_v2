import pygame
from screen import Screen
from button import Button, IconButton
from numberPad import NumberPad
from inputBox import InputBox
from label import Label
from screen import logoScreenUpdate, pinScreenUpdate, mainScreenUpdate
from training import Training
from user import User, UserContainer
from photoScreen import PhotoScreen
from facerecognitionScreen import Facerecognition
from keyBoard import Keyboard
from iconImage import IconImage

class MainUI:

    pinInput = None

    addBtn = None
    removeBtn = None
    renameBtn = None
    makePhotos = None
    ignitionBtn = None
    keyBoard = None

    photoNrLabel = None
    photoSubj = None
    checkBtn = None

    oldNameLabel = None
    oldNameInput = None
    newNameLabel = None
    newNameInput = None

    pinDelay = 1000
    pinState = True
    pinTimer = 0

    #### Initialize Screens and Buttons
    def initUI():
        ## Logo Screen
        logoImage = pygame.image.load("res/logo_back.jpg").convert_alpha()  # Load logo image
        logoScreen = Screen("Logo", logoScreenUpdate, logoImage)

        ## Pin Screen
        pinScreen = Screen("Pin",pinScreenUpdate,background_color=(20,20,20))
        NumberPad((200, 100), (200, 300), pinScreen, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.pinInput = InputBox((480, 100), (200, 50), pinScreen, maxChar=4, font_size=48, color=(255, 255, 255), bg_color=(80, 80, 80))
        Label("Insert PIN:", (200, 50), pinScreen, font_size=32, color=(255, 255, 255))

        ## Main Screen
        backgroundImage = pygame.image.load("res/backround_image.jpg").convert_alpha()  # Load main screen background image
        mainScreen = Screen("Main",mainScreenUpdate,backgroundImage)
        Label("Users:", (80, 130), mainScreen, font_size=32, color=(255, 255, 255))
        IconImage("res/small_logo_ui.png",(5,5),mainScreen)
        MainUI.addBtn = Button("Add User", (520, 100), (200, 50), mainScreen, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.addBtn.onClick = MainUI.makeAddHandler()
        MainUI.removeBtn = Button("Remove User", (520, 170), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.removeBtn.onClick = MainUI.makeRemoveHandler()
        MainUI.renameBtn = Button("Rename User", (520, 240), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.renameBtn.onClick = MainUI.makeRenameHandler()
        MainUI.makePhotos = Button("Make Photos", (520, 310), (200, 50), mainScreen, active=False, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
        MainUI.makePhotos.onClick = MainUI.makePhotoClickHandler()
        MainUI.ignitionBtn = IconButton("res/ignition.png", (290, 300), mainScreen)
        MainUI.ignitionBtn.onClick = MainUI.makeFaceIgnitionHandler()
        MainUI.keyBoard = Keyboard(mainScreen,MainUI.onKeyboardKeyPress,(800,480))
        MainUI.oldNameLabel = Label("Old username:",(300, 20),mainScreen,font_size=32, color=(255, 255, 255),visible=False)
        MainUI.oldNameInput = InputBox((300, 60), (200, 40),mainScreen, maxChar=15, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80), visible=False)
        MainUI.newNameLabel = Label("New username:",(300, 130),mainScreen,font_size=32, color=(255, 255, 255),visible=False)
        MainUI.newNameInput = InputBox((300, 170), (200, 40),mainScreen, maxChar=15, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80), visible=False)
        
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
        Label("Scan your face: ", (10, 10), faceRecScreen, font_size=32, color=(239,81,130)) # Label to show the name of the subject user
        cancelBtn2 = IconButton("res/cancel.png", (20, 150), faceRecScreen)  # Cancel button to return to main screen
        cancelBtn2.onClick = MainUI.makeFaceRecCancelHandler()  # Set the cancel button click handler


        driveSafeScreen = Screen("Drive Safe",background_image=backgroundImage)
        driveSafeLabel = Label("Drive Safe!", (0,0), driveSafeScreen, font_size=64, color=(255,255,255))
        driveSafeLabel.moveToCenter()
        backToMainBtn1 = IconButton("res/sageata.png",(320,320),driveSafeScreen,onClick= lambda:Screen.setCurrentScreen("Main"))

        intruderScreen = Screen("Intruder",background_image=backgroundImage)
        intruderLabel = Label("Intruder Alert!", (0,0), intruderScreen, font_size=64, color=(255,255,255))
        intruderLabel.moveToCenter()
        backToMainBtn = IconButton("res/sageata.png",(320,320),intruderScreen,onClick= lambda:Screen.setCurrentScreen("Main"))

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

    def makeFaceRecCancelHandler():
        def handler():
            Facerecognition.end()
            Screen.setCurrentScreen("Main")
        return handler

    def makeRemoveHandler():
        def handler():
            if MainUI.keyBoard.visible:
                return
            UserContainer.removeUser(User.selectedUser)  # Remove selected user
        return handler

    def makeAddHandler():
        def handler():
            if MainUI.keyBoard.visible:
                return
            UserContainer.addUser()  # Add a new user when clicked
        return handler

    def makeUserClickHandler(button):
        def handler():
            if MainUI.keyBoard.visible:
                return
            button.userButtonClick()
            MainUI.UpdateLeftButtons()
        return handler
    
    def makePhotoClickHandler():
        def handler():
            if MainUI.keyBoard.visible:
                return
            if User.selectedUser is None:
                print("No selected user.")
                return
            Screen.setCurrentScreen("Photo")
            PhotoScreen.reset()     # Reset photos and UI labels
            # Optional: ensure camera is closed before starting fresh (safe)
            PhotoScreen.shutdown()
            # Initialize PhotoScreen state (loads images, resets vars, but does NOT open camera)
            PhotoScreen.init()
        return handler
    
    def makePhotoCancelHandler():
        def handler():
            Screen.setCurrentScreen("Main")
            PhotoScreen.close_camera()
            PhotoScreen.initialized = False  # Reset the photo screen state
            Button.onMouseMotion(None)  # Update hover state after click
        return handler
    
    def makeCheckHandler():
        def handler():
            PhotoScreen.savePhotos()
            PhotoScreen.close_camera()
            Screen.setCurrentScreen("Train")
        return handler
    
    def makeFaceIgnitionHandler():
        def handler():
            if MainUI.keyBoard.visible:
                return
            Screen.setCurrentScreen("FaceRec")
            Facerecognition.init()
        return handler
    
    def makeRenameHandler():
        def handler():
            if MainUI.keyBoard.visible:
                return
            if User.selectedUser is None:
                print("No selected user.")
                return
            MainUI.keyBoard.show()
            MainUI.removeBtn.setActive(False)
            MainUI.renameBtn.setActive(False)
            MainUI.makePhotos.setActive(False)
            MainUI.addBtn.setActive(False)
            MainUI.ignitionBtn.setActive(False)
            UserContainer.setActive(False)
            MainUI.oldNameInput.setVisible(True)
            MainUI.oldNameInput.text = User.selectedUser.name
            MainUI.newNameInput.setVisible(True)
            MainUI.newNameInput.text = User.selectedUser.name
            MainUI.oldNameLabel.setVisible(True)
            MainUI.newNameLabel.setVisible(True)
        return handler

    @staticmethod
    def ActivateUI():
        MainUI.removeBtn.setActive(True)
        MainUI.renameBtn.setActive(True)
        MainUI.makePhotos.setActive(True)
        MainUI.addBtn.setActive(True)
        MainUI.ignitionBtn.setActive(True)
        UserContainer.setActive(True)
        MainUI.oldNameInput.setVisible(False)
        MainUI.newNameInput.setVisible(False)
        MainUI.oldNameLabel.setVisible(False)
        MainUI.newNameLabel.setVisible(False)

    def onKeyboardKeyPress(key_label):
        #print(key_label)
        if key_label == "ERASE" and len(MainUI.newNameInput.text) > 0:
            MainUI.newNameInput.text = MainUI.newNameInput.text[:-1]
            return
        if len(MainUI.newNameInput.text) < 15 and key_label != "ERASE":
            MainUI.newNameInput.text += key_label
