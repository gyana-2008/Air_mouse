import mediapipe as mp
import numpy as np
import pyautogui
import time
import cv2
import math
import os

class FaceTracker:
    def __init__(self, settings, command_queue):
        self.settings = settings
        self.queue = command_queue
        
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # Read initial accuracy setting and load model
        self.current_acc_mode = self.settings.get("tracking_accuracy", "NORMAL")
        self._init_model()
        
        self.screen_w, self.screen_h = pyautogui.size()
        self.plocX, self.plocY = 0, 0
        self.prev_nose_x, self.prev_nose_y = 0, 0
        self.virtual_x, self.virtual_y = 0, 0
        
        # Facial Gesture States
        self.last_facial_gesture_time = 0
        self.left_macro_time = 0
        self.right_macro_time = 0
        
        self.double_blink_start_time = 0
        self.is_double_blinking = False
        
        self.is_eye_l_clicking = False
        self.is_eye_r_clicking = False
        
        self.face_was_present = True
        self.no_face_start_time = 0
        
        self.left_ear_history = []
        self.right_ear_history = []
        
        # CPU Optimizations
        self.frame_counter = 0
        self.is_room_dark = False

    def _init_model(self):
        """Dynamically loads the AI based on the UI Accuracy Mode."""
        # FIX 3: Prevent memory leaks by closing the old AI model before loading a new one
        if hasattr(self, 'face_mesh') and self.face_mesh is not None:
            self.face_mesh.close()
            
        # FIX 1 & 2: Restored our stable 0.65 baseline, and set HIGH to a realistic 0.75
        conf = 0.75 if self.current_acc_mode == "HIGH" else 0.65
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, 
            refine_landmarks=True, 
            min_detection_confidence=conf, 
            min_tracking_confidence=conf
        )

    def _enhance_low_light(self, img):
        """CPU Optimized: Only checks room brightness once every 30 frames."""
        self.frame_counter += 1
        if self.frame_counter % 30 == 0:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            self.is_room_dark = np.mean(gray) < 80
            
        if self.is_room_dark:
            return cv2.convertScaleAbs(img, alpha=1.4, beta=35)
        return img
        
    def process_frame(self, rgb_img, draw_img, is_clutch_pinched=False):
        master_eye_mouth = self.settings.get("eye_mouth_enabled", True)
        mouse_enabled = self.settings.get("face_mouse_enabled", False)
        noface_enabled = self.settings.get("noface_enabled", True)
        
        if not (master_eye_mouth or mouse_enabled or noface_enabled):
            return draw_img 
            
        target_mode = self.settings.get("tracking_accuracy", "NORMAL")
        if target_mode != self.current_acc_mode:
            self.current_acc_mode = target_mode
            self._init_model() 

        optimized_img = self._enhance_low_light(rgb_img)
        results = self.face_mesh.process(optimized_img)
        
        if not results.multi_face_landmarks:
            if noface_enabled and master_eye_mouth:
                if self.face_was_present:
                    self.face_was_present = False
                    self.no_face_start_time = time.time()
                    self.queue.put(("ROUTED_ACTION", "PLAY_PAUSE"))
                
                timeout_minutes = int(self.settings.get("noface_timeout", 10))
                time_missing = time.time() - self.no_face_start_time
                
                cv2.putText(draw_img, f"NO FACE - SLEEP IN {int((timeout_minutes*60) - time_missing)}s", 
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                if time_missing > (timeout_minutes * 60):
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    self.no_face_start_time = time.time() 
            return draw_img

        if not self.face_was_present:
            self.face_was_present = True

        for face_lms in results.multi_face_landmarks:
            self.detect_face_actions(face_lms, draw_img, is_clutch_pinched, master_eye_mouth, mouse_enabled)
                
        return draw_img

    def get_aspect_ratio(self, face_lms, top_id, bottom_id, left_id, right_id):
        top = face_lms.landmark[top_id]
        bottom = face_lms.landmark[bottom_id]
        left = face_lms.landmark[left_id]
        right = face_lms.landmark[right_id]
        
        height = math.sqrt((top.x - bottom.x)**2 + (top.y - bottom.y)**2 + (top.z - bottom.z)**2)
        width = math.sqrt((left.x - right.x)**2 + (left.y - right.y)**2 + (left.z - right.z)**2)
        
        return height / width if width > 0 else 0
        
    def detect_face_actions(self, face_lms, draw_img, is_clutch_pinched, master_eye_mouth, mouse_enabled):
        img_h, img_w, _ = draw_img.shape
        current_time = time.time()
        
        if master_eye_mouth:
            eyes_enabled = self.settings.get("eye_tracking_enabled", True)
            mouth_enabled = self.settings.get("mouth_tracking_enabled", True)
            
            raw_left_ear = self.get_aspect_ratio(face_lms, 159, 145, 33, 133)
            raw_right_ear = self.get_aspect_ratio(face_lms, 386, 374, 362, 263)
            mouth_mar = self.get_aspect_ratio(face_lms, 13, 14, 78, 308)

            self.left_ear_history.append(raw_left_ear)
            self.right_ear_history.append(raw_right_ear)
            if len(self.left_ear_history) > 3: self.left_ear_history.pop(0)
            if len(self.right_ear_history) > 3: self.right_ear_history.pop(0)
            
            left_eye_ear = sum(self.left_ear_history) / len(self.left_ear_history)
            right_eye_ear = sum(self.right_ear_history) / len(self.right_ear_history)

            BLINK_THRESH = 0.20
            OPEN_THRESH = 0.23 
            MOUTH_THRESH = 0.15

            if mouth_enabled and mouth_mar > MOUTH_THRESH:
                if current_time - self.last_facial_gesture_time > 0.8:
                    action = self.settings.get("face_mouth_open_action", "MUTE")
                    if action != "NONE":
                        self.queue.put(("ROUTED_ACTION", action))
                        self.last_facial_gesture_time = current_time
                    cv2.putText(draw_img, "MOUTH OPEN", (20, 160), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
            
            elif eyes_enabled:
                is_left_closed = left_eye_ear < BLINK_THRESH
                is_right_closed = right_eye_ear < BLINK_THRESH
                is_left_open = left_eye_ear > OPEN_THRESH
                is_right_open = right_eye_ear > OPEN_THRESH

                left_action = self.settings.get("face_left_blink_action", "LEFT_CLICK")
                right_action = self.settings.get("face_right_blink_action", "RIGHT_CLICK")

                # --- LEFT EYE ---
                if is_left_closed and is_right_open:
                    self.is_double_blinking = False
                    if left_action in ["LEFT_CLICK", "RIGHT_CLICK"]:
                        if not self.is_eye_l_clicking:
                            cmd = "LEFT_DOWN" if left_action == "LEFT_CLICK" else "RIGHT_DOWN"
                            self.queue.put((cmd,))
                            self.is_eye_l_clicking = True
                    else:
                        if current_time - self.left_macro_time > 0.8:
                            self.queue.put(("ROUTED_ACTION", left_action))
                            self.left_macro_time = current_time
                    cv2.putText(draw_img, f"LEFT EYE: {left_action}", (20, 160), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                else:
                    if self.is_eye_l_clicking:
                        cmd = "LEFT_UP" if left_action == "LEFT_CLICK" else "RIGHT_UP"
                        self.queue.put((cmd,))
                        self.is_eye_l_clicking = False

                # --- RIGHT EYE ---
                if is_right_closed and is_left_open:
                    self.is_double_blinking = False
                    if right_action in ["LEFT_CLICK", "RIGHT_CLICK"]:
                        if not self.is_eye_r_clicking:
                            cmd = "RIGHT_DOWN" if right_action == "RIGHT_CLICK" else "LEFT_DOWN"
                            self.queue.put((cmd,))
                            self.is_eye_r_clicking = True
                    else:
                        if current_time - self.right_macro_time > 0.8:
                            self.queue.put(("ROUTED_ACTION", right_action))
                            self.right_macro_time = current_time
                    cv2.putText(draw_img, f"RIGHT EYE: {right_action}", (20, 190), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                else:
                    if self.is_eye_r_clicking:
                        cmd = "RIGHT_UP" if right_action == "RIGHT_CLICK" else "LEFT_UP"
                        self.queue.put((cmd,))
                        self.is_eye_r_clicking = False

                # --- DOUBLE BLINK ---
                if is_left_closed and is_right_closed:
                    if not self.is_double_blinking:
                        self.is_double_blinking = True
                        self.double_blink_start_time = current_time
                    elif current_time - self.double_blink_start_time > 0.3:
                        action = self.settings.get("face_double_blink_action", "PLAY_PAUSE")
                        if action != "NONE" and current_time - self.last_facial_gesture_time > 1.0:
                            self.queue.put(("ROUTED_ACTION", action))
                            self.last_facial_gesture_time = current_time
                        cv2.putText(draw_img, "DOUBLE BLINK", (20, 220), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                        self.is_double_blinking = False
                else:
                    self.is_double_blinking = False

        if mouse_enabled:
            face_dpi = float(self.settings.get("face_dpi", 2.5))
            smoothening = max(1.0, float(self.settings.get("face_smoothening", 6)))
            clutch_enabled = self.settings.get("face_clutch_enabled", True)
            
            nx, ny = int(face_lms.landmark[4].x * img_w), int(face_lms.landmark[4].y * img_h)
            cv2.circle(draw_img, (nx, ny), 5, (0, 255, 255), cv2.FILLED)

            can_move = not clutch_enabled or is_clutch_pinched

            if can_move:
                if self.prev_nose_x == 0 or self.prev_nose_y == 0:
                    c_x, c_y = pyautogui.position()
                    self.virtual_x, self.virtual_y = c_x, c_y
                    self.plocX, self.plocY = c_x, c_y
                    self.prev_nose_x, self.prev_nose_y = nx, ny
                
                delta_x = nx - self.prev_nose_x
                delta_y = ny - self.prev_nose_y
                
                self.virtual_x += delta_x * (face_dpi * 4.0)
                self.virtual_y += delta_y * (face_dpi * 4.0)
                self.virtual_x = max(0, min(self.screen_w, self.virtual_x))
                self.virtual_y = max(0, min(self.screen_h, self.virtual_y))
                
                clocX = self.plocX + (self.virtual_x - self.plocX) / smoothening
                clocY = self.plocY + (self.virtual_y - self.plocY) / smoothening
                
                self.queue.put(("MOVE", clocX, clocY))
                self.plocX, self.plocY = clocX, clocY
                self.prev_nose_x, self.prev_nose_y = nx, ny
                cv2.putText(draw_img, "FACE MOVEMENT: ACTIVE", (20, 120), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            else:
                self.prev_nose_x, self.prev_nose_y = 0, 0 
                cv2.putText(draw_img, "FACE MOVEMENT: CLUTCHED (Pinch to move)", (20, 120), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 165, 255), 2)