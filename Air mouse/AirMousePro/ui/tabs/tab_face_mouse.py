import tkinter as tk
from tkinter import ttk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="Face & Nose Tracking", font=("Segoe UI", 16, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10), anchor="w", padx=20)
             
    # =========================================
    # 1. Master & Clutch Toggles
    # =========================================
    toggle_frame = tk.Frame(frame, bg="#151B2B")
    toggle_frame.pack(fill="x", padx=25, pady=5)
    
    # Face Engine Master Toggle
    tk.Label(toggle_frame, text="Enable Face Mouse (Nose Movement):", 
             font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
             
    is_face = settings.get("face_mouse_enabled", False)
    btn_face = tk.Button(toggle_frame, text="ON" if is_face else "OFF", 
                         bg="#10B981" if is_face else "#EF4444", fg="#FFFFFF", 
                         font=("Segoe UI", 9, "bold"), width=8, relief="flat", cursor="hand2")
    btn_face.pack(side="left", padx=15)
    
    def toggle_face():
        new_state = not settings.get("face_mouse_enabled", False)
        settings.set("face_mouse_enabled", new_state)
        btn_face.config(text="ON" if new_state else "OFF", bg="#10B981" if new_state else "#EF4444")
    btn_face.config(command=toggle_face)

    # Clutch Toggle (Require Pinch)
    toggle_frame2 = tk.Frame(frame, bg="#151B2B")
    toggle_frame2.pack(fill="x", padx=25, pady=10)
    
    tk.Label(toggle_frame2, text="Safety Clutch (Require Hand Pinch to Move):", 
             font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
             
    is_clutch = settings.get("face_clutch_enabled", True)
    btn_clutch = tk.Button(toggle_frame2, text="ON" if is_clutch else "OFF", 
                           bg="#10B981" if is_clutch else "#EF4444", fg="#FFFFFF", 
                           font=("Segoe UI", 9, "bold"), width=8, relief="flat", cursor="hand2")
    btn_clutch.pack(side="left", padx=15)
    
    def toggle_clutch():
        new_state = not settings.get("face_clutch_enabled", True)
        settings.set("face_clutch_enabled", new_state)
        btn_clutch.config(text="ON" if new_state else "OFF", bg="#10B981" if new_state else "#EF4444")
    btn_clutch.config(command=toggle_clutch)

    # =========================================
    # 2. NEW: QUICK EYE ACTION PRESET SWITCH
    # =========================================
    toggle_frame3 = tk.Frame(frame, bg="#151B2B")
    toggle_frame3.pack(fill="x", padx=25, pady=5)
    
    tk.Label(toggle_frame3, text="Eye Wink Action Preset:", 
             font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
             
    # Read current state from settings
    current_left_action = settings.get("face_left_blink_action", "LEFT_CLICK")
    is_click_mode = (current_left_action == "LEFT_CLICK")
    
    btn_eye_mode = tk.Button(toggle_frame3, text="MOUSE CLICKS" if is_click_mode else "SCROLLING", 
                             bg="#3B82F6" if is_click_mode else "#8B5CF6", fg="#FFFFFF", 
                             font=("Segoe UI", 9, "bold"), width=15, relief="flat", cursor="hand2")
    btn_eye_mode.pack(side="left", padx=15)

    def toggle_eye_mode():
        # Check current state again on click
        current = settings.get("face_left_blink_action", "LEFT_CLICK")
        if current == "LEFT_CLICK":
            # Switch to Scrolling (ARROW_UP/DOWN)
            settings.set("face_left_blink_action", "ARROW_UP")
            settings.set("face_right_blink_action", "ARROW_DOWN")
            btn_eye_mode.config(text="SCROLLING", bg="#8B5CF6")
        else:
            # Switch to Mouse Clicks
            settings.set("face_left_blink_action", "LEFT_CLICK")
            settings.set("face_right_blink_action", "RIGHT_CLICK")
            btn_eye_mode.config(text="MOUSE CLICKS", bg="#3B82F6")
            
    btn_eye_mode.config(command=toggle_eye_mode)

    # =========================================
    # Helper function for sliders
    # =========================================
    def make_slider(label_text, setting_key, from_val, to_val, default_val, is_float=False):
        sub_frame = tk.Frame(frame, bg="#151B2B")
        sub_frame.pack(fill="x", padx=25, pady=10)
        
        tk.Label(sub_frame, text=label_text, font=("Segoe UI", 10, "bold"), 
                 bg="#151B2B", fg="#E2E8F0").pack(anchor="w")
                 
        slider = ttk.Scale(sub_frame, from_=from_val, to_=to_val, orient="horizontal")
        slider.set(settings.get(setting_key, default_val))
        slider.pack(fill="x", pady=5)
        
        def on_release(event):
            val = float(slider.get())
            if not is_float: val = int(val)
            else: val = round(val, 2)
            settings.set(setting_key, val)
            
        slider.bind("<ButtonRelease-1>", on_release)

    # =========================================
    # Face Physics Sliders
    # =========================================
    make_slider("Face DPI (Higher = Less neck movement needed)", "face_dpi", 1.0, 5.0, 2.5, is_float=True)
    make_slider("Face Smoothening (Higher = Slower/Smoother)", "face_smoothening", 2, 12, 6)
    
    return frame