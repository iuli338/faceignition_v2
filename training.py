import face_recognition
from pathlib import Path
import cv2
import pickle
import os

class Training:

    initialized = False

    def trainingScreenUpdate():
        if Training.initialized == False:
            Training.initialized = True
            return
        else:
            # Initialize known encodings and names
            knownEncodings = []
            knownNames = []

            # Path to dataset
            dataset_dir = Path("dataset")
            print("[INFO] Starting face processing...")

            if os.path.isdir(dataset_dir) and not os.listdir(dataset_dir):
                print("[INFO] Dataset dir empty. Aborting training, removing encodings.")
                if os.path.isfile("encodings.pickle"):
                    os.remove("encodings.pickle")
            else:
                if not dataset_dir.is_dir():
                    print(f"[ERROR] Dataset directory '{dataset_dir}' does not exist.")
                else:
                    for user_dir in dataset_dir.iterdir():
                        if not user_dir.is_dir() or user_dir.name.startswith('.'):
                            continue

                        user_name = user_dir.name
                        print(f"[INFO] Processing images for user: {user_name}")

                        for image_path in user_dir.glob("*.jpg"):
                            print(f"[DEBUG] Processing image: {image_path.name}")

                            try:
                                image = cv2.imread(image_path)
                                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                                # Detect face locations
                                boxes = face_recognition.face_locations(rgb, model="hog")

                                # Encode face(s)
                                encodings = face_recognition.face_encodings(rgb, boxes)

                                for encoding in encodings:
                                    knownEncodings.append(encoding)
                                    knownNames.append(user_name)

                            except Exception as e:
                                print(f"[ERROR] Failed to process {image_path}: {e}")
                                continue

                if knownEncodings:
                    print("[INFO] Serializing encodings to 'encodings.pickle'...")
                    with open("encodings.pickle", "wb") as f:
                        pickle.dump({"encodings": knownEncodings, "names": knownNames}, f)
                    print("[INFO] Training complete.")
                else:
                    from user import User
                    User.removePhotos()
                    print("[WARNING] No encodings were found. Check your dataset images.")
            # End of training
            from screen import Screen
            from user import User, UserState, UserContainer
            Training.initialized = False
            if knownEncodings:
                if User.selectedUser is not None:
                    User.selectedUser.state = UserState.HAS_PHOTOS
                UserContainer.reRenderButtons()
            Screen.setCurrentScreen("Main")