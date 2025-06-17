import cv2
import time
import threading
import imutils
import face_recognition
import pickle
import pygame
import os

pygame.font.init()

class Facerecognition:
    currentname = None
    encodingsP = None
    data = None
    started = False
    timeToActivate = 6.0
    timeToBlock = 6.0
    ActivateTimer = 0.0
    BlockTimer = 0.0
    stop_event = threading.Event()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    last_processed_frame = None
    processed_surface = None
    cap = None

    # Shared data between threads
    shared_data = {
        "frame": None,         # Current camera frame (BGR)
        "rgb_frame": None,     # Current RGB frame for recognition
        "boxes": [],           # Detected face boxes
        "names": [],           # Detected names
        "lock": threading.Lock(),
    }

    text_cache = {}

    def get_text_surface(name, font):
        if name not in Facerecognition.text_cache:
            Facerecognition.text_cache[name] = font.render(name, True, (0, 255, 255))
        return Facerecognition.text_cache[name]

    def startThreads():
        # Start threads
        Facerecognition.stop_event.clear()  # Clear stop flag
        camera_thread = threading.Thread(target=Facerecognition.camera_feed_thread, daemon=True)
        recognition_thread = threading.Thread(target=Facerecognition.face_recognition_thread,daemon=True)
        camera_thread.start()
        recognition_thread.start()

    def stopThreads():
        Facerecognition.stop_event.set()  # Signal threads to stop

    def init():
        # Initialize 'currentname' to trigger only when a new person is identified.
        Facerecognition.currentname = "unknown"
        Facerecognition.encodingsP = "encodings.pickle"

        # Load the known faces and embeddings along with the face detector
        print("[INFO] loading encodings + face detector...")
        if os.path.exists(Facerecognition.encodingsP):
            with open(Facerecognition.encodingsP, "rb") as f:
                Facerecognition.data = pickle.load(f)
        else:
            print("[WARN] Encodings file not found. No known faces loaded.")
            Facerecognition.data = {
                "encodings": [],
                "names": []
            }
        
        # Start the camera feed thread
        
        Facerecognition.startThreads()

    def camera_feed_thread():
        if Facerecognition.cap is None or not Facerecognition.cap.isOpened():
            Facerecognition.cap = cv2.VideoCapture(0)
        while not Facerecognition.stop_event.is_set():
            ret, frame = Facerecognition.cap.read()
            if not ret or frame is None:
                print("[WARN] Failed to grab frame.")
                time.sleep(0.1)
                continue

            frame = imutils.resize(frame, width=480)

            with Facerecognition.shared_data["lock"]:
                Facerecognition.shared_data["frame"] = frame.copy()
                Facerecognition.shared_data["rgb_frame"] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            time.sleep(0.01)
        if Facerecognition.cap is not None:
            Facerecognition.cap.release()
            Facerecognition.cap = None

    def face_recognition_thread():
        last_recognition_time = 0
        recognition_interval = 0.1  # seconds between recognition attempts

        while not Facerecognition.stop_event.is_set():
            current_time = time.time()

            # Only process every `recognition_interval` seconds
            if current_time - last_recognition_time >= recognition_interval:
                with Facerecognition.shared_data["lock"]:
                    rgb_frame = Facerecognition.shared_data["rgb_frame"].copy() if Facerecognition.shared_data["rgb_frame"] is not None else None

                if rgb_frame is not None:
                    boxes = face_recognition.face_locations(rgb_frame)
                    encodings = face_recognition.face_encodings(rgb_frame, boxes)
                    names = []

                    for encoding in encodings:
                        matches = face_recognition.compare_faces(Facerecognition.data["encodings"], encoding)
                        name = "Unknown"
                        if True in matches:
                            matchedIdxs = [i for i, b in enumerate(matches) if b]
                            counts = {}
                            for i in matchedIdxs:
                                n = Facerecognition.data["names"][i]
                                counts[n] = counts.get(n, 0) + 1
                            name = max(counts, key=counts.get)

                        names.append(name)

                    with Facerecognition.shared_data["lock"]:
                        Facerecognition.shared_data["boxes"] = boxes
                        Facerecognition.shared_data["names"] = names

                last_recognition_time = current_time

            time.sleep(1)  # Prevent CPU spinning

    def facerecognitionDraw(screen):
        with Facerecognition.shared_data["lock"]:
            frame_ref = Facerecognition.shared_data["frame"]
            boxes = Facerecognition.shared_data["boxes"]
            names = Facerecognition.shared_data["names"]

        if frame_ref is not None:
            if Facerecognition.last_processed_frame is None or not (frame_ref is Facerecognition.last_processed_frame):
                frame = frame_ref.copy()

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
                    frame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))  # Make sure axes are swapped

                    # Save processed versions
                    Facerecognition.last_processed_frame = frame_ref
                    Facerecognition.processed_surface = frame_surface

                except Exception as e:
                    print("Error processing frame:", e)
                    Facerecognition.processed_surface = None
        else:
            Facerecognition.processed_surface = None

        # Blit if surface is ready
        if Facerecognition.processed_surface is not None:
            screen.blit(Facerecognition.processed_surface, (0, 0))

        # Overlay face names
        for ((top, right, bottom, left), name) in zip(boxes, names):
            text_surface = Facerecognition.get_text_surface(name, Facerecognition.font)
            screen.blit(text_surface, (800 - (right * 1.5), bottom - 100))

    def facerecognitionScreenUpdate():
        delta_time = Facerecognition.clock.tick(60) / 1000.0  # Limit to 60 FPS, returns ms -> convert to seconds

        with Facerecognition.shared_data["lock"]:
            names = Facerecognition.shared_data["names"]

        # Timer logic for known and unknown users
        if any(name != "Unknown" for name in names):
            Facerecognition.ActivateTimer += delta_time
            Facerecognition.BlockTimer = 0.0  # Reset intruder timer if known user detected
            if Facerecognition.ActivateTimer >= Facerecognition.timeToActivate:
                from screen import Screen
                Screen.setCurrentScreen("Drive Safe")
                Facerecognition.stopThreads()
                Facerecognition.last_processed_frame = None
                Facerecognition.processed_surface = None
                Facerecognition.ActivateTimer = 0.0
                Facerecognition.BlockTimer = 0.0
                return
        elif any(name == "Unknown" for name in names) and len(names) > 0:
            Facerecognition.ActivateTimer = 0.0
            Facerecognition.BlockTimer += delta_time
            if Facerecognition.BlockTimer >= Facerecognition.timeToBlock:
                from screen import Screen
                Screen.setCurrentScreen("Intruder")
                Facerecognition.stopThreads()
                Facerecognition.last_processed_frame = None
                Facerecognition.processed_surface = None
                Facerecognition.ActivateTimer = 0.0
                Facerecognition.BlockTimer = 0.0
                return
        else:
            Facerecognition.ActivateTimer = 0.0
            Facerecognition.BlockTimer = 0.0