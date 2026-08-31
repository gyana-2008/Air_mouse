import tkinter as tk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="AirMouse Pro Dashboard", font=("Segoe UI", 18, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10))
             
    tk.Label(frame, text="System Status: ONLINE", font=("Segoe UI", 12), 
             fg="#10B981", bg="#151B2B").pack()

    # --- ENGINES CONTAINER ---
    engines_frame = tk.Frame(frame, bg="#151B2B")
    engines_frame.pack(fill="x", padx=40, pady=(30, 10))
    
    def make_engine_row(parent_frame, title, setting_key):
        row = tk.Frame(parent_frame, bg="#1E293B", pady=10, padx=15)
        row.pack(fill="x", pady=5)
        
        tk.Label(row, text=title, font=("Segoe UI", 12, "bold"), 
                 fg="#E2E8F0", bg="#1E293B").pack(side="left")
                 
        is_on = settings.get(setting_key, True)
        
        btn = tk.Button(row, text="ENGINE ONLINE" if is_on else "ENGINE OFFLINE", 
                        bg="#10B981" if is_on else "#EF4444", fg="#FFFFFF", 
                        font=("Segoe UI", 10, "bold"), width=15, relief="flat", cursor="hand2")
        btn.pack(side="right")
        
        def toggle():
            new_state = not settings.get(setting_key, True)
            settings.set(setting_key, new_state)
            btn.config(text="ENGINE ONLINE" if new_state else "ENGINE OFFLINE", 
                       bg="#10B981" if new_state else "#EF4444")
                       
        btn.config(command=toggle)

    # These keys map directly to the engines!
    make_engine_row(engines_frame, "Hand & Gesture Tracking Engine", "hand_mouse_enabled")
    make_engine_row(engines_frame, "Face & Nose Tracking Engine", "face_mouse_enabled")
    make_engine_row(engines_frame, "Eye & Mouth Tracking Engine", "eye_mouth_enabled")

    # --- PERFORMANCE & ACCURACY CONTAINER ---
    perf_frame = tk.Frame(frame, bg="#151B2B")
    perf_frame.pack(fill="x", padx=40, pady=10)
    
    perf_row = tk.Frame(perf_frame, bg="#1E293B", pady=10, padx=15)
    perf_row.pack(fill="x", pady=5)
    
    tk.Label(perf_row, text="AI Tracking Accuracy Mode", font=("Segoe UI", 12, "bold"), 
             fg="#00E5FF", bg="#1E293B").pack(side="left")
             
    # Read current state (Defaults to NORMAL)
    current_mode = settings.get("tracking_accuracy", "NORMAL")
    is_high = (current_mode == "HIGH")
    
    btn_acc = tk.Button(perf_row, text="HIGH PRECISION" if is_high else "NORMAL MODE", 
                        bg="#8B5CF6" if is_high else "#3B82F6", fg="#FFFFFF", 
                        font=("Segoe UI", 10, "bold"), width=15, relief="flat", cursor="hand2")
    btn_acc.pack(side="right")
    
    def toggle_accuracy():
        curr = settings.get("tracking_accuracy", "NORMAL")
        if curr == "NORMAL":
            settings.set("tracking_accuracy", "HIGH")
            btn_acc.config(text="HIGH PRECISION", bg="#8B5CF6") # Purple for High Precision
        else:
            settings.set("tracking_accuracy", "NORMAL")
            btn_acc.config(text="NORMAL MODE", bg="#3B82F6") # Blue for Normal Mode
            
    btn_acc.config(command=toggle_accuracy)

    return frame