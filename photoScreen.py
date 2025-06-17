import cv2
import pygame
import time
import os
import shutil

class PhotoScreen:
    webcam_recorder = None
    noWebCamImage = None
    frame = None
    photos = []  # List to store captured photos
    initialized = False

    def init():
        PhotoScreen.webcam_recorder = cv2.VideoCapture(0)
        PhotoScreen.noWebCamImage = pygame.image.load("res/nowebcam.png").convert_alpha()  # Load no webcam image

    @staticmethod
    def reset():
        PhotoScreen.photos = []  # Reset the list of photos
        from mainUI import MainUI
        from user import User
        MainUI.photoNrLabel.updateText("Photos taken: 0")  # Reset the photo count label
        MainUI.photoSubj.updateText(f"Making photos for: {User.selectedUser.name}")
        MainUI.checkBtn.setVisible(False)
        from button import IconButton
        IconButton.onMouseMotion(None)  # Update hover state after click
    
    @staticmethod
    def photoScreenUpdate():
        # Ensure webcam is opened
        if PhotoScreen.webcam_recorder is None or not PhotoScreen.webcam_recorder.isOpened():
            print("Attempting to open webcam...")
            PhotoScreen.webcam_recorder = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not PhotoScreen.webcam_recorder.isOpened():
                print("Failed to open webcam. Retrying in 1 second...")
                PhotoScreen.webcam_recorder.release()
                PhotoScreen.webcam_recorder = None
                time.sleep(1)
                return

        # Try reading a frame
        ret, frame = PhotoScreen.webcam_recorder.read()

        if not ret or frame is None or frame.size == 0:
            print("Webcam read failed. Restarting webcam...")
            PhotoScreen.webcam_recorder.release()
            PhotoScreen.webcam_recorder = None
            time.sleep(1)
            return

        try:
            height, width, _ = frame.shape
            crop_width = 800

            if width >= crop_width:
                x_start = (width - crop_width) // 2
                x_end = x_start + crop_width
                cropped_frame = frame[:, x_start:x_end]
            else:
                pad_left = (crop_width - width) // 2
                pad_right = crop_width - width - pad_left
                cropped_frame = cv2.copyMakeBorder(
                    frame, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=(0, 0, 0)
                )

            resized_frame = cv2.resize(cropped_frame, (800, 480))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            PhotoScreen.frame = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))

        except Exception as e:
            print(f"Error processing frame: {e}")
            PhotoScreen.frame = None

        time.sleep(0.01)  # Sleep to reduce CPU usage
        
        if (PhotoScreen.initialized is False):
            PhotoScreen.initialized = True
    
    @staticmethod
    def makePhoto():
        # Take the current frame and save it in a list, later used to save the photos
        if PhotoScreen.frame is not None:
            PhotoScreen.photos.append(PhotoScreen.frame)
            from mainUI import MainUI
            MainUI.photoNrLabel.updateText(f"Photos taken: {len(PhotoScreen.photos)}")
            if (len(PhotoScreen.photos) >= 5):
                MainUI.checkBtn.setVisible(True)

    @staticmethod
    def savePhotos():
        from user import User
        user_folder = os.path.join("dataset", User.selectedUser.name)

        # If the folder exists, clear it
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
        os.makedirs(user_folder, exist_ok=True)

        for idx, photo_surface in enumerate(PhotoScreen.photos, start=1):
            # Convert pygame surface to numpy array and then to BGR for OpenCV
            photo_array = pygame.surfarray.array3d(photo_surface).swapaxes(0, 1)
            photo_bgr = cv2.cvtColor(photo_array, cv2.COLOR_RGB2BGR)
            image_path = os.path.join(user_folder, f"image{idx}.jpg")
            cv2.imwrite(image_path, photo_bgr)
        
        print(f"Photos of user {User.selectedUser.name} saved to dataset/{User.selectedUser.name}.")