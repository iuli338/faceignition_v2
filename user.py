import pygame
import json
import os
import shutil

class UserState:
    NO_PHOTOS = 0
    HAS_PHOTOS = 1

class User:

    allUsers = []
    selectedUser = None

    def __init__(self, name):
        self.name = name
        self.state = UserState.NO_PHOTOS  # Default state
        User.allUsers.append(self)

    @staticmethod
    def removePhotos():
        folder = "dataset/"+User.selectedUser.name
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)
            print(f"Deleted photos of user {User.selectedUser.name} because no encodings.")

    @staticmethod
    def loadUsers():
        # Load users from json file if it exists
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                User.allUsers = [User(user['name']) for user in users_data]
                for user, data in zip(User.allUsers, users_data):
                    user.state = data.get('state', UserState.NO_PHOTOS)
            print("Users loaded from 'users.json'.")
        except FileNotFoundError:
            print("No users file found, starting with default users.")
            User.allUsers = [
            User("User 1"),
            User("User 2"),
            User("User 3")
            ]   
       
    @staticmethod
    def selectUser(user):
        if User.selectedUser == user:
            User.selectedUser = None  # Deselect if already selected
            print(f"User '{user.name}' deselected.")
            return
        print(f"User '{user.name}' selected.")
        User.selectedUser = user

    @staticmethod
    def saveUsers():
        # Save to json file
        users_data = [{'name': user.name, 'state': user.state} for user in User.allUsers]
        with open('users.json', 'w') as f:
            json.dump(users_data, f, indent=4)
        print("Users saved to 'users.json'.")
            
class UserButton:
    def __init__(self, user, button):
        self.user = user
        self.userName = user.name
        self.isSelected = False
        self.button = button  # Placeholder for button object
        self.button.atachUserButton(self)  # Attach this UserButton to the button

        self.renderText()

    def renderText(self):
        # Render the user name on the button
        font = pygame.font.Font(None, 36)
        font2 = pygame.font.Font(None, 18)
        self.text_surface = font.render(self.user.name, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.button.rect.centerx, self.button.rect.centery))
        self.text_surface2 = None
        self.text_rect2 = None
        self.text_surface3 = None
        self.text_rect3 = None
        text = ""
        color = None
        if (self.user.state == UserState.HAS_PHOTOS):
            text = "Has photos"
            color = (255, 255, 255)
        else:
            text = "No photos"
            color = (255, 0, 0)
        
        self.text_surface2 = font2.render(text, True, color)
        self.text_rect2 = self.text_surface2.get_rect(center=(self.button.rect.centerx, self.button.rect.centery + 18))
        self.text_surface3 = font2.render(text, True, (0,0,0))
        self.text_rect3 = self.text_surface2.get_rect(center=(self.button.rect.centerx+2, self.button.rect.centery + 20))


    def draw(self, screen):
        # Ensure the button is initialized before drawing
        if not self.button:
            return
        # Draw the user name
        screen.blit(self.text_surface, self.text_rect)
        
        # Draw the user state text if it exists
        if self.text_surface2 and self.text_rect2:
            screen.blit(self.text_surface3, self.text_rect3)
            screen.blit(self.text_surface2, self.text_rect2)

class UserContainer:

    allUserButtons = []
    maxUsers = 3

    @staticmethod
    def init():
        pass

    @staticmethod
    def setActive(active):
        for userButton in UserContainer.allUserButtons:
            userButton.button.setActive(active)
    
    @staticmethod
    def draw(screen):
        for userButton in UserContainer.allUserButtons:
            userButton.draw(screen)

    @staticmethod
    def reRenderButtons():
        for userButton in UserContainer.allUserButtons:
            userButton.renderText()

    @staticmethod
    def renameSelectedUser(newName):
        oldName = User.selectedUser.name
        if os.path.exists("dataset/"+oldName):
            os.rename("dataset/"+oldName, "dataset/"+newName)
            print("Folder renamed.")
        User.selectedUser.name = newName

        UserContainer.reRenderButtons()
        print(f"User renamed from {oldName} to {newName}.")
        User.saveUsers()

    @staticmethod
    def addUserButton(user,screenPtr):
        if len(UserContainer.allUserButtons) < UserContainer.maxUsers:
            from button import Button
            from mainUI import MainUI
            new_button = Button("", (80, 170 + len(UserContainer.allUserButtons) * 70), (200, 50), screenPtr, font_size=32, color=(255, 255, 255), bg_color=(80, 80, 80))
            new_button.onClick = MainUI.makeUserClickHandler(new_button)
            new_userButton = UserButton(user, new_button)
            UserContainer.allUserButtons.append(new_userButton)
            if len(UserContainer.allUserButtons) >= UserContainer.maxUsers:
                MainUI.addBtn.setActive(False)
            else:
                MainUI.addBtn.setActive(True)
    
    @staticmethod
    def generateName():
        existing_names = {user.name for user in User.allUsers}
        
        i = 1
        while True:
            candidate = f"New User {i}"
            if candidate not in existing_names:
                return candidate
            i += 1

    @staticmethod
    def addUser():
        name = UserContainer.generateName()
        from screen import Screen
        if len(User.allUsers) < UserContainer.maxUsers:
            new_user = User(name)
            UserContainer.addUserButton(new_user, Screen.currentScreen)
            print(f"User '{name}' added.")
        else:
            print("Maximum number of users reached. Cannot add more users.")

    @staticmethod
    def removeUser(user):
        if User.selectedUser is None:
            print("No selected user.")
            return
        from mainUI import MainUI
        for userButton in UserContainer.allUserButtons:
            if userButton.user == user:
                from screen import Screen
                Screen.currentScreen.allButtons.remove(userButton.button)
                UserContainer.allUserButtons.remove(userButton)
                User.allUsers.remove(userButton.user)
                # Remove images from dataset
                user_folder = os.path.join("dataset", User.selectedUser.name)
                # If the folder exists, clear it
                if os.path.exists(user_folder):
                    shutil.rmtree(user_folder)
                MainUI.UpdateLeftButtons()
                print(f"User '{user.name}' removed.")
                if len(UserContainer.allUserButtons) < UserContainer.maxUsers:
                    MainUI.addBtn.setActive(True)
                # Update user buttons positions
                for i, userButton in enumerate(UserContainer.allUserButtons):
                    userButton.button.rect.topleft = (80, 170 + i * 70)
                    userButton.renderText()
                if User.selectedUser.state == UserState.HAS_PHOTOS:
                    Screen.setCurrentScreen("Train")
                from button import Button
                from mainUI import MainUI
                User.selectedUser = None
                MainUI.UpdateLeftButtons()
                Button.userButtonUpdateColor()
                User.saveUsers()
                return
        print(f"User '{user.name}' not found.")

        