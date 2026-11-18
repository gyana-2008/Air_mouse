# AIRMOUSE PRO – README & DOCUMENTATION

AirMouse Pro is an advanced, touchless computer vision control system built in Python. It allows you to control your Windows PC using your hands, nose, eyes, and mouth gestures via your webcam.

---

## 1. FEATURES OVERVIEW

- **Hand & Gesture Tracking:** Move the cursor using pinch gestures, perform multi-hand zooming, and trigger system macros using hand signs (peace sign, thumbs up/down, rock sign).
- **Face & Nose Tracking:** Use your nose as a virtual mouse pointer with an adjustable safety clutch.
- **Eye & Mouth Tracking:** Control clicks, scrolling, or media playback through custom eye blinks and mouth states.
- **Low-Light Enhancement:** Automatically boosts exposure and contrast in dark room environments.
- **Dynamic Accuracy Modes:** Switch between Normal Mode and High Precision depending on your performance needs.

---

## 2. PREREQUISITES

- Windows OS (64-bit)
- A working computer webcam

**For running the prebuilt executable:**
- No Python installation required.

**For running from source:**
- Python 3.12+

---

## 3. DOWNLOAD & RUN THE APPLICATION (.EXE)

AirMouse Pro includes a prebuilt Windows executable, allowing users to run the application without installing Python or manually configuring dependencies.

### Steps:

1. Open the GitHub repository.
2. Navigate to the executable distribution folder or the repository's Releases section.
3. Download the provided AirMouse Pro executable package.
4. If downloading a ZIP package, extract it completely.
5. Open the extracted folder.
6. Double-click `AirMousePro.exe` to launch the application.
7. Allow webcam access if Windows requests permission.

**Important:**
- Keep the complete application folder intact when using the executable.
- Do not move the `.exe` separately from its supporting files when using an onedir build.
- Windows SmartScreen may display a security warning for an unsigned executable. Only run it if you downloaded it from the official project repository.

---

## 4. HOW TO INSTALL & RUN FROM SOURCE (GITHUB REPOSITORY)

If you prefer to run the application using its original Python source code:

1. Clone or download this repository to your local machine.
2. Open a terminal (Command Prompt or VS Code terminal) inside the project root directory.
3. Install the required Python dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

4. Run the application:

```bash
python main.py
```

---

## 5. HOW TO BUILD A STANDALONE EXECUTABLE (.EXE) LOCALLY

If you want to compile the Python source code into your own standalone executable:

### Step 1: Prepare the project

Ensure the following files and folders are present:

- `main.py`
- `icon.ico`
- `ui/`
- All required Python source files

### Step 2: Create `build.bat`

Create a file named `build.bat` in the project root directory, alongside `main.py` and `icon.ico`.

Paste the following commands:

```bat
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
```

### Step 3: Build the application

Double-click `build.bat` to automatically compile the project.

### Step 4: Locate the executable

Once the build completes successfully, navigate to:

```text
dist/AirMousePro/
```

Your executable and its supporting files will be available inside this folder.

---

## 6. IMPORTANT NOTES

- The prebuilt executable is intended for Windows 64-bit systems.
- A working webcam is required for camera-based functionality.
- The executable package should be distributed with all its supporting files.
- Running from source requires Python and the appropriate dependencies.
- Building the executable locally requires PyInstaller and the project dependencies.

---

**AirMouse Pro – Experience a new way to interact with your computer, completely touch-free.**
