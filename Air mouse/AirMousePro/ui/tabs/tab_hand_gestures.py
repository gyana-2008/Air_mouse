import tkinter as tk
from tkinter import ttk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="Gestures & Macros", font=("Segoe UI", 16, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10), anchor="w", padx=20)
             
    # Options for the dropdown menu
    action_options = [
        "NONE", "MUTE", "ESC", "TASK_VIEW", "SCREENSHOT", 
        "PLAY_PAUSE", "VOLUME_UP", "VOLUME_DOWN", "NEXT_TRACK", 
        "PREV_TRACK", "MACRO_1", "MACRO_2", "MACRO_3", "MACRO_4"
    ]
    
    # List of all gestures (Single and Dual hand)
    gestures = [
        {"id": "gest_thumb_up", "name": "Thumb Up 👍", "default": "VOLUME_UP"},
        {"id": "gest_thumb_down", "name": "Thumb Down 👎", "default": "VOLUME_DOWN"},
        {"id": "gest_rock", "name": "Rock Sign 🤟", "default": "SCREENSHOT"},
        {"id": "gest_pinky", "name": "Pinky Up 🤙", "default": "MUTE"},
        {"id": "gest_gun", "name": "Gun Sign 👈", "default": "PLAY_PAUSE"},
        {"id": "gest_ok", "name": "OK Sign 👌", "default": "NONE"},
        {"id": "gest_dual_peace", "name": "Dual Peace ✌️✌️", "default": "TASK_VIEW"},
        {"id": "gest_dual_thumb", "name": "Dual Thumbs 👍👍", "default": "PLAY_PAUSE"},
        {"id": "gest_dual_rock", "name": "Dual Rock 🤟🤟", "default": "ESC"}
    ]
    
    # Create a scrollable canvas since the list of gestures is long
    canvas = tk.Canvas(frame, bg="#151B2B", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    matrix_frame = tk.Frame(canvas, bg="#151B2B")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y", padx=5, pady=5)
    canvas.pack(side="left", fill="both", expand=True, padx=25, pady=10)
    canvas.create_window((0, 0), window=matrix_frame, anchor="nw")
    
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    matrix_frame.bind("<Configure>", on_configure)

    # Generate a row for every gesture
    for i, gest in enumerate(gestures):
        row_frame = tk.Frame(matrix_frame, bg="#151B2B")
        row_frame.pack(fill="x", pady=8)
        
        # 1. Gesture Name Label
        tk.Label(row_frame, text=gest["name"], font=("Segoe UI", 11, "bold"), 
                 bg="#151B2B", fg="#E2E8F0", width=18, anchor="w").pack(side="left")
                 
        # 2. ON/OFF Toggle Button
        toggle_key = f"{gest['id']}_enabled"
        is_enabled = settings.get(toggle_key, True)
        
        btn = tk.Button(row_frame, text="ON" if is_enabled else "OFF", 
                        bg="#10B981" if is_enabled else "#EF4444", 
                        fg="#FFFFFF", font=("Segoe UI", 9, "bold"), 
                        width=6, relief="flat", cursor="hand2")
        btn.pack(side="left", padx=15)
        
        def make_toggle(b, key):
            def on_click():
                new_state = not settings.get(key, True)
                settings.set(key, new_state)
                b.config(text="ON" if new_state else "OFF", 
                           bg="#10B981" if new_state else "#EF4444")
            return on_click
            
        btn.config(command=make_toggle(btn, toggle_key))
        
        # 3. Action Dropdown Menu
        action_key = f"{gest['id']}_action"
        current_action = settings.get(action_key, gest["default"])
        
        cb = ttk.Combobox(row_frame, values=action_options, state="readonly", width=15)
        cb.set(current_action)
        cb.pack(side="left", padx=10)
        
        def make_select(combo, key):
            def on_select(event):
                settings.set(key, combo.get())
            return on_select
            
        cb.bind("<<ComboboxSelected>>", make_select(cb, action_key))

    return frame