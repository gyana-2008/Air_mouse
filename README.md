============================================================
AIRMOUSE PRO - README & DOCUMENTATION
============================================================

AirMouse Pro is an advanced, touchless computer vision control system built in Python. It allows you to control your Windows PC using your hands, nose, eyes, and mouth gestures via your webcam.


------------------------------------------------------------
1. FEATURES OVERVIEW
------------------------------------------------------------
* Hand & Gesture Tracking: Move the cursor using pinch gestures, perform multi-hand zooming, and trigger system macros using hand signs (peace sign, thumbs up/down, rock sign).
* Face & Nose Tracking: Use your nose as a virtual mouse pointer with an adjustable safety clutch.
* Eye & Mouth Tracking: Control clicks, scrolling, or media playback through custom eye blinks and mouth states.
* Low-Light Enhancement: Automatically boosts exposure and contrast in dark room environments.
* Dynamic Accuracy Modes: Easily switch between Normal Mode and High Precision depending on your performance needs.


------------------------------------------------------------
2. PREREQUISITES
------------------------------------------------------------
* Windows OS (64-bit)
* A working computer webcam
* Python 3.12+


------------------------------------------------------------
3. HOW TO INSTALL & RUN FROM SOURCE (GITHUB REPO)
------------------------------------------------------------
Since this repository contains the raw Python source files (.py), follow these steps to run the application on your computer:

1. Clone or download this repository to your local machine.
2. Open a terminal (Command Prompt or VS Code terminal) inside the project root directory.
3. Install the required Python dependencies by running:
   pip install opencv-python mediapipe pyautogui numpy
4. Run the application:
   python main.py


------------------------------------------------------------
4. HOW TO BUILD A STANDALONE EXECUTABLE (.exe) LOCALLY
------------------------------------------------------------
If you want to compile the Python source code into a standalone `.exe` application so it runs without needing a Python environment:

1. Create a file named `build.bat` in your root project folder (right next to `main.py` and `icon.ico`).
2. Paste the following commands into `build.bat`:

------------------------------------------------------------
@echo off
TITLE Building AirMouse Pro Executable...
echo [INFO] Cleaning old build files...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__

echo [INFO] Starting PyInstaller compilation with MediaPipe asset collection...
pyinstaller --noconsole --onedir --icon="icon.ico" --collect-all mediapipe --hidden-import="ui.tabs.tab_home" --hidden-import="ui.tabs.tab_hand_mouse" --hidden-import="ui.tabs.tab_face_mouse" --hidden-import="ui.tabs.tab_eye_mouth" --hidden-import="ui.tabs.tab_hand_gestures" --hidden-import="ui.tabs.tab_guide" --name="AirMousePro" main.py

echo ========================================================
echo [SUCCESS] Build process finished! 
echo Find your package inside the 'dist/AirMousePro' folder.
echo ========================================================
pause
------------------------------------------------------------

3. Double-click `build.bat` to automatically build the application.
4. Find your complete, runnable app folder inside `dist/AirMousePro`.
