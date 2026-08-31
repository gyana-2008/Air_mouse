# Air_mouse
a virtual computer vision controled mouse and shortcuts
============================================================
AIRMOUSE PRO - INSTRUCTIONS & DOCUMENTATION
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
* Python 3.12+ (if running from source)


------------------------------------------------------------
3. HOW TO INSTALL & RUN (FROM SOURCE)
------------------------------------------------------------
1. Clone or download this repository to your local machine.
2. Open a terminal inside the project directory and install the required dependencies:
   pip install opencv-python mediapipe pyautogui numpy
3. Run the application:
   python main.py


------------------------------------------------------------
4. HOW TO BUILD THE STANDALONE EXECUTABLE (.exe)
------------------------------------------------------------
If you want to compile the project into a standalone application so it runs without Python installed, you can use the automated build script (`build.bat`).

Create a file named `build.bat` in your root project folder and paste the following commands into it:

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

To build:
1. Double-click `build.bat` to automatically build the application.
2. Find your complete app folder inside `dist/AirMousePro`.


------------------------------------------------------------
5. HOW TO SHARE WITH FRIENDS
------------------------------------------------------------
1. Locate the "AirMousePro" folder inside the "dist/" directory after running the builder.
2. Compress the entire "AirMousePro" folder into a .zip file.
3. Send the .zip file to your friend.
4. IMPORTANT INSTRUCTION FOR USERS: Instruct your friend to extract/unzip the entire folder before opening it, then double-click "AirMousePro.exe" from inside that extracted folder to run it.
