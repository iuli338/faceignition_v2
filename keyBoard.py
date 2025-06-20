import pygame
from button import Button

class Keyboard:
    def __init__(self, screenPtr, onKeyPress, screen_size):
        self.screenPtr = screenPtr
        self.onKeyPress = onKeyPress
        self.buttons = []
        self.visible = False
        self.uppercase = True

        self.screen_width, self.screen_height = screen_size
        self.keyboard_top = self.screen_height // 2
        self.key_margin = 5

        self.key_rows = [
            list("1234567890"),
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            list("ZXCVBNM"),
        ]

        self.buildKeyboard()

        # Create this once during initialization
        self.overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # semi-transparent black, 180/255 alpha

        self.screenPtr.keyBoard = self

    def buildKeyboard(self):
        key_height = (self.screen_height - self.keyboard_top - (len(self.key_rows) + 4) * self.key_margin) // (len(self.key_rows) + 3)
        max_keys = max(len(row) for row in self.key_rows)
        key_width = (self.screen_width - (max_keys + 1) * self.key_margin) // max_keys

        self.letter_buttons = []

        # Create keys
        for row_index, row in enumerate(self.key_rows):
            y = self.keyboard_top + (key_height + self.key_margin) * row_index + self.key_margin
            row_len = len(row)
            total_row_width = row_len * (key_width + self.key_margin)
            x_start = (self.screen_width - total_row_width) // 2 + self.key_margin // 2
            for col_index, key in enumerate(row):
                x = x_start + col_index * (key_width + self.key_margin)
                btn = self.createKey(key, (x, y), (key_width, key_height))
                if key.isalpha():
                    self.letter_buttons.append(btn)

        # Add spacebar, erase, and shift (all in one row)
        y = self.keyboard_top + (key_height + self.key_margin) * len(self.key_rows) + self.key_margin
        shift_width = key_width * 2
        space_width = key_width * 5 + self.key_margin * 4
        erase_width = key_width * 2 + self.key_margin

        total_width = shift_width + space_width + erase_width + self.key_margin * 2
        x_start = (self.screen_width - total_width) // 2

        # SHIFT key
        shift_x = x_start
        self.shift_button = Button("SHIFT", (shift_x, y), (shift_width, key_height), self.screenPtr, font_size=32, onClick=self.toggleCase)

        # SPACE key
        space_x = shift_x + shift_width + self.key_margin
        self.createKey("SPACE", (space_x, y), (space_width, key_height))

        # ERASE key
        erase_x = space_x + space_width + self.key_margin
        self.createKey("ERASE", (erase_x, y), (erase_width, key_height))

        self.buttons.append(self.shift_button)

        # Add Cancel and Rename buttons at the bottom center
        y += key_height + self.key_margin
        button_width = key_width * 3
        button_spacing = self.key_margin * 4
        total_width = button_width * 2 + button_spacing
        x_start = (self.screen_width - total_width) // 2

        self.cancel_button = Button("CANCEL", (x_start, y), (button_width, key_height), self.screenPtr, font_size=32, onClick=self.cancelRename)
        self.rename_button = Button("RENAME", (x_start + button_width + button_spacing, y), (button_width, key_height), self.screenPtr, font_size=32, onClick=self.rename, bg_color=(239,81,130))

        self.buttons.extend([self.cancel_button, self.rename_button])

        self.hide()

    def createKey(self, key_label, pos, size):
        def onClick():
            if key_label == "SPACE":
                self.onKeyPress(" ")
            elif key_label == "ERASE":
                self.onKeyPress("ERASE")
            elif key_label.isalpha():
                self.onKeyPress(key_label.upper() if self.uppercase else key_label.lower())
            else:
                self.onKeyPress(key_label)

        key_button = Button(
            text=key_label,
            pos=pos,
            size=size,
            screenPtr=self.screenPtr,
            font_size=32,
            onClick=onClick
        )
        self.buttons.append(key_button)
        return key_button

    def toggleCase(self):
        self.uppercase = not self.uppercase
        for btn in self.letter_buttons:
            char = btn.text
            new_char = char.upper() if self.uppercase else char.lower()
            btn.text = new_char
            btn.renderText()

    def rename(self):
        from mainUI import MainUI
        # The new name should have at least one char
        if len(MainUI.newNameInput.text) < 1:
            return
        # The new name should not be the same
        if MainUI.newNameInput.text == MainUI.oldNameInput.text:
            return
        # New name should not be a name that already exists
        from user import UserContainer, User
        for user in User.allUsers:
            if user.name == MainUI.newNameInput.text:
                print("Name already exists.")
                return
        UserContainer.renameSelectedUser(MainUI.newNameInput.text)
        print("Renamed.")
        self.hide()
        MainUI.ActivateUI()
        from screen import Screen
        from user import User, UserState
        if User.selectedUser.state == UserState.HAS_PHOTOS:
            print("Retrain because user has photos.")
            Screen.setCurrentScreen("Train")
        else:
            print("No retrain because no photos.")

    def cancelRename(self):
        print("Canceled rename.")
        self.hide()
        from mainUI import MainUI
        MainUI.ActivateUI()

    def show(self):
        self.visible = True
        for button in self.buttons:
            button.visible = True

    def hide(self):
        self.visible = False
        for button in self.buttons:
            button.visible = False

    def makeXHandler():
        def handler():
            from mainUI import MainUI
            MainUI.ActivateUI()
            MainUI.keyBoard.setVisible(False)
        return handler
    
    def draw(self,screen):
        if not self.visible:
            return
        # Draw transparent black background
        # Just blit the prebuilt overlay
        screen.blit(self.overlay, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        from mainUI import MainUI
        MainUI.oldNameInput.draw(screen)
        MainUI.oldNameLabel.draw(screen)
        MainUI.newNameInput.draw(screen)
        MainUI.newNameLabel.draw(screen)