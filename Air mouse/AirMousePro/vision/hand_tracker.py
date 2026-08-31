import mediapipe as mp
import math
import numpy as np
import pyautogui
import time
import cv2  

class HandTracker:
    def __init__(self, settings, command_queue):
        self.settings = settings
        self.queue = command_queue
        
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        # Read initial accuracy setting and load model
        self.current_acc_mode = self.settings.get("tracking_accuracy", "NORMAL")
        self._init_model()
        
        self.screen_w, self.screen_h = pyautogui.size()
        
        self.plocX, self.plocY = 0, 0
        self.is_left_clicking = False
        
        self.is_index_pinched = False
        self.is_middle_pinched = False
        
        self.prev_hand_x, self.prev_hand_y = 0, 0
        self.virtual_x, self.virtual_y = 0, 0
        
        self.last_right_click = 0
        self.last_mid_click = 0
        self.last_swipe_time = 0
        self.last_gesture_time = 0 
        
        self.prev_swipe_x = 0
        self.prev_scroll_y = 0
        self.prev_zoom_dist = 0
        
        self.hud_text = ""
        self.hud_timer = 0
        
        # CPU Optimizations
        self.frame_counter = 0
        self.is_room_dark = False

    def _init_model(self):
        """Dynamically loads the AI based on the UI Accuracy Mode."""
        # FIX: Prevent memory leaks by closing the old AI model before loading a new one
        if hasattr(self, 'hands') and self.hands is not None:
            self.hands.close()
            
        # FIX: Restored our stable 0.65 baseline, and set HIGH to a realistic 0.75
        conf = 0.75 if self.current_acc_mode == "HIGH" else 0.65
        self.hands = self.mp_hands.Hands(
            max_num_hands=2, 
            min_detection_confidence=conf, 
            min_tracking_confidence=conf
        )

    def set_hud(self, text):
        self.hud_text = text
        self.hud_timer = time.time()

    def _enhance_low_light(self, img):
        """CPU Optimized: Only checks room brightness once every 30 frames."""
        self.frame_counter += 1
        if self.frame_counter % 30 == 0:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            self.is_room_dark = np.mean(gray) < 80
            
        if self.is_room_dark:
            return cv2.convertScaleAbs(img, alpha=1.4, beta=35)
        return img
        
    def process_frame(self, rgb_img, draw_img):
        # 1. Master Toggle Check
        is_enabled = self.settings.get("hand_mouse_enabled", True)
        if str(is_enabled).lower() == "false" or not is_enabled:
            cv2.putText(draw_img, "ENGINE PAUSED (Check UI Settings)", (20, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            return draw_img

        # 2. Dynamic Accuracy Check
        target_mode = self.settings.get("tracking_accuracy", "NORMAL")
        if target_mode != self.current_acc_mode:
            self.current_acc_mode = target_mode
            self._init_model() # Instantly reload AI with new confidence

        # Apply the Low-Light Enhancer
        optimized_img = self._enhance_low_light(rgb_img)
        results = self.hands.process(optimized_img)
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_lms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(draw_img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
            
            self.detect_mouse_actions(results.multi_hand_landmarks, results.multi_handedness, draw_img.shape)
                
        if time.time() - self.hud_timer < 1.5:
            cv2.putText(draw_img, f"Action: {self.hud_text}", (20, 90), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 229, 255), 2, cv2.LINE_AA)
                
        return draw_img

    def _get_hand_state(self, hand_lms, img_w, img_h, pinch_thresh):
        def get_coords(lm): return int(lm.x * img_w), int(lm.y * img_h)
        
        def dist_3d(lm1, lm2):
            return math.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2 + (lm1.z - lm2.z)**2)

        tx, ty = get_coords(hand_lms.landmark[4])  
        thumb_mcp_y = int(hand_lms.landmark[2].y * img_h) 
        ix, iy = get_coords(hand_lms.landmark[8])  
        mx, my = get_coords(hand_lms.landmark[12]) 
        
        fingers_up = [
            hand_lms.landmark[8].y < hand_lms.landmark[5].y,  
            hand_lms.landmark[12].y < hand_lms.landmark[9].y, 
            hand_lms.landmark[16].y < hand_lms.landmark[13].y, 
            hand_lms.landmark[20].y < hand_lms.landmark[17].y  
        ]

        thumb_is_up = (ty < thumb_mcp_y - 20)
        thumb_is_down = (ty > thumb_mcp_y + 20)
        all_fingers_down = not any(fingers_up)
        
        thresh_3d = pinch_thresh / 1000.0

        return {
            'fingers_up': fingers_up,
            'is_thumb_up': all_fingers_down and thumb_is_up,
            'is_thumb_down': all_fingers_down and thumb_is_down,
            'all_fingers_down': all_fingers_down,
            'dist_index_3d': dist_3d(hand_lms.landmark[4], hand_lms.landmark[8]),
            'dist_middle_3d': dist_3d(hand_lms.landmark[4], hand_lms.landmark[12]),
            'pinched_ring': dist_3d(hand_lms.landmark[4], hand_lms.landmark[16]) < thresh_3d,
            'pinched_pinky': dist_3d(hand_lms.landmark[4], hand_lms.landmark[20]) < thresh_3d,
            'ix': ix, 'iy': iy, 'mx': mx, 'my': my, 'ty': ty,
            'wrist_x': int(hand_lms.landmark[0].x * img_w)
        }
        
    def detect_mouse_actions(self, multi_hand_lms, multi_handedness, img_shape):
        img_h, img_w, _ = img_shape
        current_time = time.time()
        
        cursor_enabled = self.settings.get("cursor_enabled", True)
        enable_right_hand = self.settings.get("enable_right_hand", True)
        enable_left_hand = self.settings.get("enable_left_hand", True)
        mouse_dpi = float(self.settings.get("mouse_dpi", 1.0))
        pinch_thresh = float(self.settings.get("pinch_threshold", 40))
        smoothening = max(1.0, float(self.settings.get("smoothening", 5)))
        scroll_mult = float(self.settings.get("scroll_speed", 5))

        right_hand_lms = None
        left_hand_lms = None
        
        for idx, handedness in enumerate(multi_handedness):
            label = handedness.classification[0].label
            if label == "Right": right_hand_lms = multi_hand_lms[idx]
            elif label == "Left": left_hand_lms = multi_hand_lms[idx]

        if not enable_right_hand: right_hand_lms = None
        if not enable_left_hand: left_hand_lms = None

        p_state = self._get_hand_state(right_hand_lms, img_w, img_h, pinch_thresh) if right_hand_lms else None
        s_state = self._get_hand_state(left_hand_lms, img_w, img_h, pinch_thresh) if left_hand_lms else None

        def fire_gesture(gest_id, fallback):
            if self.settings.get(f"{gest_id}_enabled", True):
                action = self.settings.get(f"{gest_id}_action", fallback)
                if action != "NONE":
                    self.queue.put(("ROUTED_ACTION", action))
                    self.set_hud(f"Action: {action}")
                    self.last_gesture_time = current_time - 1.0 

        is_swipe_pose = False
        is_scroll_pose = False
        
        if p_state:
            is_swipe_pose = p_state['fingers_up'] == [True, True, True, False]
            is_scroll_pose = p_state['fingers_up'] == [True, True, False, False]
            
            thresh_3d = pinch_thresh / 1000.0
            release_buffer_3d = 0.015 
            
            if p_state['dist_index_3d'] < thresh_3d: 
                self.is_index_pinched = True
            elif p_state['dist_index_3d'] > thresh_3d + release_buffer_3d: 
                self.is_index_pinched = False
                
            if p_state['dist_middle_3d'] < thresh_3d: 
                self.is_middle_pinched = True
            elif p_state['dist_middle_3d'] > thresh_3d + release_buffer_3d: 
                self.is_middle_pinched = False

        if cursor_enabled:
            primary_wants_click = p_state and self.is_middle_pinched and not is_swipe_pose
            secondary_wants_click = s_state and (s_state['dist_index_3d'] < (pinch_thresh / 1000.0))
            
            if primary_wants_click or secondary_wants_click:
                if not self.is_left_clicking:
                    self.queue.put(("LEFT_DOWN",))
                    self.is_left_clicking = True
                    self.set_hud("Left Click (Held)")
            else:
                if self.is_left_clicking:
                    self.queue.put(("LEFT_UP",))
                    self.is_left_clicking = False
                    self.set_hud("Released Click")

        is_doing_dual_action = False
        
        if p_state and s_state:
            if self.is_middle_pinched and (s_state['dist_middle_3d'] < (pinch_thresh / 1000.0)):
                is_doing_dual_action = True
                curr_dist = math.hypot(p_state['mx'] - s_state['mx'], p_state['my'] - s_state['my'])
                if self.prev_zoom_dist == 0: self.prev_zoom_dist = curr_dist
                delta_dist = curr_dist - self.prev_zoom_dist
                
                if abs(delta_dist) > 15: 
                    if delta_dist > 0:
                        self.queue.put(("HOTKEY", "ctrl", "+"))
                        self.set_hud("Zoom In")
                    else:
                        self.queue.put(("HOTKEY", "ctrl", "-"))
                        self.set_hud("Zoom Out")
                    self.prev_zoom_dist = curr_dist
            else:
                self.prev_zoom_dist = 0

            if current_time - self.last_gesture_time > 1.5 and not is_doing_dual_action:
                is_dual_peace = (p_state['fingers_up'] == [True, True, False, False] and s_state['fingers_up'] == [True, True, False, False])
                is_dual_thumb = (p_state['is_thumb_up'] and s_state['is_thumb_up'])
                is_dual_rock = (p_state['fingers_up'] == [True, False, False, True] and s_state['fingers_up'] == [True, False, False, True])
                
                if is_dual_peace:
                    fire_gesture("gest_dual_peace", "TASK_VIEW")
                    is_doing_dual_action = True
                elif is_dual_thumb:
                    fire_gesture("gest_dual_thumb", "PLAY_PAUSE")
                    is_doing_dual_action = True
                elif is_dual_rock:
                    fire_gesture("gest_dual_rock", "ESC")
                    is_doing_dual_action = True
        else:
            self.prev_zoom_dist = 0

        # Primary Hand Logic
        if p_state and cursor_enabled and not is_doing_dual_action:
            is_safety_lock = p_state['all_fingers_down'] and not p_state['is_thumb_up'] and not p_state['is_thumb_down'] and not (self.is_index_pinched or self.is_middle_pinched or p_state['pinched_ring'] or p_state['pinched_pinky'])
            
            if is_safety_lock:
                self.prev_hand_x, self.prev_hand_y = 0, 0
                self.set_hud("SAFETY LOCK ACTIVE")
                self.is_movement_pinched = False
            else:
                self.is_movement_pinched = (self.is_index_pinched or self.is_middle_pinched) and not is_swipe_pose
                face_mouse_active = self.settings.get("face_mouse_enabled", False)

                if self.is_movement_pinched:
                    if not face_mouse_active:
                        track_x, track_y = (p_state['mx'], p_state['my']) if self.is_middle_pinched else (p_state['ix'], p_state['iy'])
                        
                        if self.prev_hand_x == 0 or self.prev_hand_y == 0:
                            c_x, c_y = pyautogui.position()
                            self.virtual_x, self.virtual_y = c_x, c_y
                            self.plocX, self.plocY = c_x, c_y
                            self.prev_hand_x, self.prev_hand_y = track_x, track_y
                        
                        delta_x = track_x - self.prev_hand_x
                        delta_y = track_y - self.prev_hand_y
                        
                        self.virtual_x += delta_x * (mouse_dpi * 2.5)
                        self.virtual_y += delta_y * (mouse_dpi * 2.5)
                        self.virtual_x = max(0, min(self.screen_w, self.virtual_x))
                        self.virtual_y = max(0, min(self.screen_h, self.virtual_y))
                        
                        clocX = self.plocX + (self.virtual_x - self.plocX) / smoothening
                        clocY = self.plocY + (self.virtual_y - self.plocY) / smoothening
                        
                        self.queue.put(("MOVE", clocX, clocY))
                        self.plocX, self.plocY = clocX, clocY
                        self.prev_hand_x, self.prev_hand_y = track_x, track_y
                else:
                    self.prev_hand_x, self.prev_hand_y = 0, 0 

                if not is_scroll_pose and not is_swipe_pose:
                    if p_state['pinched_ring'] and (current_time - self.last_right_click > 0.5):
                        self.queue.put(("RIGHT_CLICK",))
                        self.last_right_click = current_time
                        self.set_hud("Right Click")

                    if p_state['pinched_pinky'] and (current_time - self.last_mid_click > 0.5):
                        self.queue.put(("MIDDLE_CLICK",))
                        self.last_mid_click = current_time
                        self.set_hud("Middle Click")

                # Scroll & Swipe Gestures
                if is_swipe_pose:
                    if self.prev_swipe_x == 0: self.prev_swipe_x = p_state['wrist_x']
                    delta_swipe_x = self.prev_swipe_x - p_state['wrist_x']
                    
                    if current_time - self.last_swipe_time > 1.0:
                        if delta_swipe_x > 60: 
                            self.queue.put(("ALT_TAB",))
                            self.last_swipe_time = current_time
                            self.prev_swipe_x = p_state['wrist_x']
                            self.set_hud("Swipe Left")
                        elif delta_swipe_x < -60: 
                            self.queue.put(("WIN_TAB",))
                            self.last_swipe_time = current_time
                            self.prev_swipe_x = p_state['wrist_x']
                            self.set_hud("Swipe Right")
                else:
                    self.prev_swipe_x = 0

                if not self.is_movement_pinched and not is_swipe_pose:
                    if is_scroll_pose:
                        if self.prev_scroll_y == 0: self.prev_scroll_y = p_state['iy']
                        delta_scroll_y = self.prev_scroll_y - p_state['iy']
                        
                        if abs(delta_scroll_y) > 4: 
                            self.queue.put(("SCROLL", int(delta_scroll_y * scroll_mult))) 
                            self.prev_scroll_y = p_state['iy']
                            self.set_hud("Scrolling")
                    else:
                        self.prev_scroll_y = 0

        # Left Hand Only (Macros)
        if s_state and not is_doing_dual_action and (current_time - self.last_gesture_time > 1.5):
            is_gun_sign = s_state['fingers_up'] == [True, False, False, False] and (s_state['ty'] < s_state['iy'] + 20) and not s_state['all_fingers_down']
            is_ok_sign = s_state['fingers_up'] == [False, True, True, True] 

            if s_state['fingers_up'] == [True, False, False, True]: fire_gesture("gest_rock", "SCREENSHOT")
            elif s_state['is_thumb_up']: fire_gesture("gest_thumb_up", "VOLUME_UP")
            elif s_state['is_thumb_down']: fire_gesture("gest_thumb_down", "VOLUME_DOWN")
            elif s_state['fingers_up'] == [False, False, False, True]: fire_gesture("gest_pinky", "MUTE")
            elif is_gun_sign: fire_gesture("gest_gun", "PLAY_PAUSE")
            elif is_ok_sign: fire_gesture("gest_ok", "NONE")