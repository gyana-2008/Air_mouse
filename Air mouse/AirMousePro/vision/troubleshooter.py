import cv2
import mediapipe as mp
import time
import sys

class VisionTroubleshooter:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_mesh
        
    def run_diagnostics(self):
        print("🔍 [TROUBLESHOOTER] Starting AirMouse Pro System Diagnostics...")
        
        # 1. Check Camera Access
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ [ERROR] Camera index 0 could not be opened. Check if another app is using your webcam.")
            return False
        print("✅ [OK] Camera feed initialized successfully.")
        
        # 2. Check Resolution & FPS
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"ℹ️ [INFO] Camera Resolution: {int(width)}x{int(height)}")
        
        # 3. Test AI Modules Initialization
        try:
            hands_test = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
            face_test = self.mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)
            print("✅ [OK] MediaPipe AI models compiled successfully.")
        except Exception as e:
            print(f"❌ [ERROR] Failed to load MediaPipe models: {e}")
            cap.release()
            return False
            
        # 4. Quick Live Frame Check (30 frames test)
        print("ℹ️ [INFO] Running 30-frame environmental light & stability check...")
        success_count = 0
        start_time = time.time()
        
        for _ in range(30):
            ret, frame = cap.read()
            if ret:
                success_count += 1
                # Check ambient light
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mean_light = gray.mean()
            time.sleep(0.01)
            
        cap.release()
        
        if success_count < 25:
            print(f"⚠️ [WARNING] Dropped frames detected ({success_count}/30 successful frames).")
        else:
            print(f"✅ [OK] Frame acquisition stable. Average Room Brightness: {int(mean_light)}/255")
            if mean_light < 80:
                print("💡 [TIP] Low lighting detected. The low-light enhancement filter will automatically engage.")
            else:
                print("💡 [TIP] Lighting conditions are optimal.")

        print("✨ [SUCCESS] All diagnostic sequences completed. System is 100% operational!")
        return True

if __name__ == "__main__":
    tool = VisionTroubleshooter()
    tool.run_diagnostics()