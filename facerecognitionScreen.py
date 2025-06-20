import cv2
import time
import threading
import pickle
import pygame
import os
from multiprocessing import Process, Queue, set_start_method

# Prevent extra window on Windows when using multiprocessing
try:
    set_start_method('spawn')
except RuntimeError:
    pass

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
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    last_processed_frame = None
    processed_surface = None
    cap = None
    frame_queue = Queue(maxsize=1)
    result_queue = Queue()
    recognition_process = None

    # Shared data between threads
    shared_data = {
        "frame": None,
        "rgb_frame": None,
        "boxes": [],
        "names": [],
        "lock": threading.Lock(),
    }

    text_cache = {}

    def get_text_surface(name, font):
        if name not in Facerecognition.text_cache:
            Facerecognition.text_cache[name] = [None,None]
            Facerecognition.text_cache[name][0] = font.render(name, True, (0, 255, 255))
            Facerecognition.text_cache[name][1] = font.render(name, True, (0, 0, 0))
        return (Facerecognition.text_cache[name][0],Facerecognition.text_cache[name][1])

    def startThreads():
        Facerecognition.stop_event.clear()
        Facerecognition.camera_thread = threading.Thread(target=Facerecognition.camera_feed_thread, daemon=True)
        Facerecognition.result_thread = threading.Thread(target=Facerecognition.result_receiver_thread, daemon=True)
        Facerecognition.recognition_process = Process(target=Facerecognition.face_recognition_process, args=(Facerecognition.frame_queue, Facerecognition.result_queue))
        Facerecognition.camera_thread.start()
        Facerecognition.result_thread.start()
        Facerecognition.recognition_process.start()

    def stopThreads():
        Facerecognition.stop_event.set()
        if Facerecognition.camera_thread is not None:
            Facerecognition.camera_thread.join()
        if Facerecognition.result_thread is not None:
            Facerecognition.result_thread.join()
        if Facerecognition.recognition_process is not None:
            Facerecognition.recognition_process.terminate()
            Facerecognition.recognition_process.join()
            Facerecognition.recognition_process = None
        Facerecognition.started = False
        if Facerecognition.cap is not None:
            Facerecognition.cap.release()
            Facerecognition.cap = None

    def init():
        if Facerecognition.started == False:
            print("FaceDetection init.")
            Facerecognition.currentname = "unknown"
            Facerecognition.encodingsP = "encodings.pickle"
            # Reset last processed frame & surface so no stale image shows
            Facerecognition.last_processed_frame = None
            Facerecognition.processed_surface = None
            with Facerecognition.shared_data["lock"]:
                Facerecognition.shared_data["names"] = []
                Facerecognition.shared_data["boxes"] = []
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

            Facerecognition.startThreads()
            Facerecognition.started = True

    def camera_feed_thread():
        while not Facerecognition.stop_event.is_set():
            # Attempt to (re)initialize the camera if needed
            if Facerecognition.cap is None or not Facerecognition.cap.isOpened():
                print("[INFO] Attempting to open camera...")
                Facerecognition.cap = cv2.VideoCapture(0)
                time.sleep(1)
                continue

            ret, frame = Facerecognition.cap.read()
            if not ret or frame is None:
                print("[WARN] Failed to grab frame.")
                Facerecognition.cap.release()
                Facerecognition.cap = None
                time.sleep(0.5)
                continue

            with Facerecognition.shared_data["lock"]:
                Facerecognition.shared_data["frame"] = frame.copy()
                Facerecognition.shared_data["rgb_frame"] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if not Facerecognition.frame_queue.full():
                try:
                    Facerecognition.frame_queue.put_nowait(frame.copy())
                except:
                    pass
            time.sleep(0.01)

        if Facerecognition.cap is not None:
            Facerecognition.cap.release()
            Facerecognition.cap = None

    def face_recognition_process(frame_queue, result_queue):
        import cv2
        import face_recognition
        import pickle
        import os

        if os.path.exists("encodings.pickle"):
            with open("encodings.pickle", "rb") as f:
                data = pickle.load(f)
        else:
            data = {"encodings": [], "names": []}

        while True:
            try:
                frame = frame_queue.get(timeout=1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb_frame)
                encodings = face_recognition.face_encodings(rgb_frame, boxes)
                names = []

                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"], encoding)
                    name = "Unknown"
                    if True in matches:
                        matchedIdxs = [i for i, b in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                            n = data["names"][i]
                            counts[n] = counts.get(n, 0) + 1
                        name = max(counts, key=counts.get)
                    names.append(name)

                result_queue.put((boxes, names))
            except:
                time.sleep(0.01)

    def result_receiver_thread():
        while not Facerecognition.stop_event.is_set():
            try:
                boxes, names = Facerecognition.result_queue.get(timeout=1)
                with Facerecognition.shared_data["lock"]:
                    Facerecognition.shared_data["boxes"] = boxes
                    Facerecognition.shared_data["names"] = names
            except:
                time.sleep(0.01)

    def end():
        Facerecognition.stopThreads()
        Facerecognition.last_processed_frame = None
        Facerecognition.processed_surface = None
        Facerecognition.ActivateTimer = 0.0
        Facerecognition.BlockTimer = 0.0

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
                    frame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))

                    Facerecognition.last_processed_frame = frame_ref
                    Facerecognition.processed_surface = frame_surface

                except Exception as e:
                    print("Error processing frame:", e)
                    Facerecognition.processed_surface = None
        else:
            Facerecognition.processed_surface = None

        if Facerecognition.processed_surface is not None:
            screen.blit(Facerecognition.processed_surface, (0, 0))
        else:
            screen.fill((20,20,20))

        for ((top, right, bottom, left), name) in zip(boxes, names):
            text_surface1 , text_surface2 = Facerecognition.get_text_surface(name, Facerecognition.font)
            screen.blit(text_surface2, (left+2, top - text_surface2.get_height() - 3))
            screen.blit(text_surface1, (left, top - text_surface1.get_height() - 5))

    def facerecognitionScreenUpdate():
        delta_time = Facerecognition.clock.tick(60) / 1000.0

        with Facerecognition.shared_data["lock"]:
            names = Facerecognition.shared_data["names"]

        if any(name != "Unknown" for name in names):
            Facerecognition.ActivateTimer += delta_time
            Facerecognition.BlockTimer = 0.0
            if Facerecognition.ActivateTimer >= Facerecognition.timeToActivate:
                from screen import Screen
                Facerecognition.end()
                Screen.setCurrentScreen("Drive Safe")
                return
        elif any(name == "Unknown" for name in names) and len(names) > 0:
            Facerecognition.ActivateTimer = 0.0
            Facerecognition.BlockTimer += delta_time
            if Facerecognition.BlockTimer >= Facerecognition.timeToBlock:
                from screen import Screen
                Facerecognition.end()
                Screen.setCurrentScreen("Intruder")
                return
        else:
            Facerecognition.ActivateTimer = 0.0
            Facerecognition.BlockTimer = 0.0