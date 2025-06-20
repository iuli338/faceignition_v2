**Hachathon 2024 - Face Recognition App (v2)**

**Introduction**

This project was originally developed during the "Hackathon" 2024 edition [more info...](https://aciee.ugal.ro/studenti/hackathon), a 48-hour coding competition held last autumn. Due to the limited time, the first version of the app was functional but messy and difficult to maintain.

We are proud to share that our app received **3rd place** in the competition, which motivated us to revisit and improve it further.

After the event, the decision was made to completely rewrite the app, keeping the same core functionality but improving the code readability, modularity, and structure. The result is this v2 version, which preserves the original idea while making the project easier to understand, extend, and maintain.

**Project Concept**

The application is a prototype of an in-vehicle face recognition system designed to run as a system app on the infotainment unit of a car. It would automatically launch when the car key is inserted, acting as an additional security layer to verify that the driver is the car's registered owner.

If the driver is recognized successfully, the system can proceed to automatically start the engine. If not, intruder alerts can be triggered — for example, by sending an SMS notification to the car owner's phone.

This concept aims to enhance vehicle security using biometric verification.

**How It Works**

The app uses your webcam to perform face recognition in real-time. It maintains and updates several data files to manage user information:

  - `users.json` — Stores usernames and their current state.
  - `encodings.pickle` — Stores the facial encodings for all known users.
  - `dataset/` — Contains individual folders for each user, with their saved face images.

All of these files are automatically created and managed by the app. You don’t need to manually edit or organize them.

For privacy reasons, all three are included in .gitignore and are not tracked in version control.

**Features**

- Face recognition using webcam
- Custom-built UI system (no external GUI frameworks)
- Fully modular architecture
- Responsive controls for user interaction

**Requirements**

Make sure the following Python libraries are installed:

```
pip install dlib opencv-python pygame face_recognition
```

Other standard modules used:

- multiprocessing
- pickle

**Custom UI Elements**

Instead of using an external GUI toolkit, we developed our own UI system using Pygame. Each UI component is implemented in a separate file for clarity and reuse:

- `button.py` — Clickable buttons
- `label.py` — Static or dynamic text elements
- `inputBox.py` — Text input fields
- `numberPad.py` — On-screen numeric keypad
- `keyboard.py` — Full on-screen keyboard

All these components are assembled and managed in `mainUI.py` to form the complete interface.

**How to Run**

To start the application, run:

```
python main.py
```

- `main.py` handles the app's main execution loop.
- `mainUI.py` constructs and manages the UI logic.

**Team & Credits**

Developed by team **Hackstreet Boys**

**Disclaimer**

This project was created solely for educational and non-commercial purposes during the Hachathon 2024 competition. Our team does not intend to generate any revenue from it.

If any fonts, images, or other assets used in the project are under a license we may have overlooked, we sincerely apologize. We are more than willing to remove or replace any such content upon request.

Please feel free to contact us with any concerns regarding copyright or attribution.

![Main Screen](https://github.com/user-attachments/assets/b881be55-a763-42a5-9de4-7f4e6607f96b)
![Screens Layout](https://github.com/user-attachments/assets/56b85183-adc9-44f8-833c-f5d2efe1bce5)
