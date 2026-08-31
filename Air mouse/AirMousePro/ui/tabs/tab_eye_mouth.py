import tkinter as tk
from tkinter import ttk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="Eye, Mouth & Safety Protocols", font=("Segoe UI", 16, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10), anchor="w", padx=20)
             
    action_options = ["NONE", "MUTE", "PLAY_PAUSE", "SCROLL_UP", "SCROLL_DOWN", "ARROW_UP", "ARROW_DOWN", "SCREENSHOT"]
    
    # 1. Master Toggles (Fixed the unpacking error here)
    toggles = [
        ("eye_tracking_enabled", "Enable Eye Tracking (Blinks)"),
        ("mouth_tracking_enabled", "Enable Mouth Tracking (Open/Close)"),
        ("noface_enabled", "Enable 'No Face' Auto-Pause & Sleep")
    ]
    
    for key, label in toggles:
        row = tk.Frame(frame, bg="#151B2B")
        row.pack(fill="x", padx=25, pady=5)
        tk.Label(row, text=label, font=("Segoe UI", 11, "bold"), bg="#151B2B", fg="#E2E8F0").pack(side="left")
        
        is_on = settings.get(key, True)
        btn = tk.Button(row, text="ON" if is_on else "OFF", bg="#10B981" if is_on else "#EF4444", 
                        fg="#FFFFFF", font=("Segoe UI", 9, "bold"), width=8, relief="flat", cursor="hand2")
        btn.pack(side="left", padx=15)
        
        def make_toggle(b, k):
            def on_click():
                new_state = not settings.get(k, True)
                settings.set(k, new_state)
                b.config(text="ON" if new_state else "OFF", bg="#10B981" if new_state else "#EF4444")
            return on_click
        btn.config(command=make_toggle(btn, key))

    # 2. Facial Macro Routing
    tk.Label(frame, text="Facial Macro Routing", font=("Segoe UI", 12, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 5), anchor="w", padx=20)
             
    gestures = [
        {"id": "face_left_blink", "name": "Left Eye Blink 👁️", "default": "ARROW_UP"}, 
        {"id": "face_right_blink", "name": "Right Eye Blink 👁️", "default": "ARROW_DOWN"}, 
        {"id": "face_double_blink", "name": "Double Blink 😑", "default": "PLAY_PAUSE"},
        {"id": "face_mouth_open", "name": "Mouth Open 😮", "default": "MUTE"}
    ]
    
    for gest in gestures:
        row = tk.Frame(frame, bg="#151B2B")
        row.pack(fill="x", padx=25, pady=5)
        tk.Label(row, text=gest["name"], font=("Segoe UI", 10, "bold"), bg="#151B2B", fg="#E2E8F0", width=18, anchor="w").pack(side="left")
        
        cb = ttk.Combobox(row, values=action_options, state="readonly", width=15)
        cb.set(settings.get(f"{gest['id']}_action", gest["default"]))
        cb.pack(side="left", padx=10)
        
        def make_select(combo, key):
            def on_select(event): settings.set(key, combo.get())
            return on_select
        cb.bind("<<ComboboxSelected>>", make_select(cb, f"{gest['id']}_action"))

    # 3. No Face Sleep Timer
    tk.Label(frame, text="No-Face Sleep Timer (Minutes)", font=("Segoe UI", 12, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 5), anchor="w", padx=20)
             
    slider = ttk.Scale(frame, from_=1, to_=60, orient="horizontal")
    slider.set(settings.get("noface_timeout", 10))
    slider.pack(fill="x", padx=25, pady=5)
    
    def on_release(event): settings.set("noface_timeout", int(slider.get()))
    slider.bind("<ButtonRelease-1>", on_release)

    return frame