import cv2
import threading
from vision.hand_tracker import HandTracker
from vision.face_tracker import FaceTracker  # 1. Import FaceTracker

class VisionEngine:
    def __init__(self, settings, command_queue):
        self.settings = settings
        self.queue = command_queue
        self.running = False
        
        # Initialize trackers
        self.hand_tracker = HandTracker(settings, command_queue)
        self.face_tracker = FaceTracker(settings, command_queue) # 2. Initialize FaceTracker

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _run_loop(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera.")
            self.running = False
            return

        while self.running:
            success, img = cap.read()
            if not success:
                continue

            # Mirror the image for intuitive movement
            img = cv2.flip(img, 1)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 1. Route frame to Hand Tracker
            img = self.hand_tracker.process_frame(rgb_img, img)

            # 2. Get the Clutch State (Is the hand pinching?)
            is_pinched = getattr(self.hand_tracker, 'is_movement_pinched', False)

            # 3. Route frame to Face Tracker, passing the clutch state!
            img = self.face_tracker.process_frame(rgb_img, img, is_clutch_pinched=is_pinched)

            # Debug HUD
            cv2.putText(img, "AirMouse Engine Running", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 229, 255), 2)
            cv2.imshow("AirMouse Pro - Vision", img)
            
            # Allow clean exit if user closes the OpenCV window manually
            if cv2.waitKey(1) & 0xFF == 27: 
                break
                
        cap.release()
        cv2.destroyAllWindows()