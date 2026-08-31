import tkinter as tk
from tkinter import ttk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="Hand Mouse Tuning", font=("Segoe UI", 16, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10), anchor="w", padx=20)
             
    # =========================================
    # 1. Master Toggles (Left & Right Hand Roles)
    # =========================================
    toggle_frame = tk.Frame(frame, bg="#151B2B")
    toggle_frame.pack(fill="x", padx=25, pady=5)
    
    # Right Hand Toggle
    tk.Label(toggle_frame, text="Track RIGHT Hand (Cursor & Clicks):", 
             font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
             
    is_right = settings.get("enable_right_hand", True)
    btn_right = tk.Button(toggle_frame, text="ON" if is_right else "OFF", 
                           bg="#10B981" if is_right else "#EF4444", fg="#FFFFFF", 
                           font=("Segoe UI", 9, "bold"), width=8, relief="flat", cursor="hand2")
    btn_right.pack(side="left", padx=15)
    
    def toggle_right():
        new_state = not settings.get("enable_right_hand", True)
        settings.set("enable_right_hand", new_state)
        btn_right.config(text="ON" if new_state else "OFF", bg="#10B981" if new_state else "#EF4444")
    btn_right.config(command=toggle_right)

    # Left Hand Toggle
    toggle_frame2 = tk.Frame(frame, bg="#151B2B")
    toggle_frame2.pack(fill="x", padx=25, pady=5)
    
    tk.Label(toggle_frame2, text="Track LEFT Hand (Macros & Modifiers):", 
             font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
             
    is_left = settings.get("enable_left_hand", True)
    btn_left = tk.Button(toggle_frame2, text="ON" if is_left else "OFF", 
                          bg="#10B981" if is_left else "#EF4444", fg="#FFFFFF", 
                          font=("Segoe UI", 9, "bold"), width=8, relief="flat", cursor="hand2")
    btn_left.pack(side="left", padx=15)
    
    def toggle_left():
        new_state = not settings.get("enable_left_hand", True)
        settings.set("enable_left_hand", new_state)
        btn_left.config(text="ON" if new_state else "OFF", bg="#10B981" if new_state else "#EF4444")
    btn_left.config(command=toggle_left)

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
            if not is_float:
                val = int(val)
            else:
                val = round(val, 2)
            settings.set(setting_key, val)
            
        slider.bind("<ButtonRelease-1>", on_release)

    # =========================================
    # The Physics Sliders
    # =========================================
    make_slider("DPI / Sensitivity (Higher = Less physical movement needed)", "mouse_dpi", 0.5, 2.5, 1.0, is_float=True)
    make_slider("Smoothness vs Speed (Lower = Faster/Jittery, Higher = Slower/Smoother)", "smoothening", 2, 12, 5)
    make_slider("Scroll Sensitivity", "scroll_speed", 1, 15, 5)
    make_slider("Pinch Threshold (Lower = Requires hard pinch, Higher = Easy grab)", "pinch_threshold", 20, 80, 40)
    
    return frame