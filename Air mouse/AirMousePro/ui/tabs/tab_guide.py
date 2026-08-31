import tkinter as tk

def create_tab(parent, settings):
    frame = tk.Frame(parent, bg="#151B2B")
    
    tk.Label(frame, text="System Manual & Guide", font=("Segoe UI", 16, "bold"), 
             fg="#00E5FF", bg="#151B2B").pack(pady=(20, 10), anchor="w", padx=20)

    guide_text = """
WELCOME TO AIRMOUSE PRO OS

1. TRACKPAD CONTROLS (Pinch Actions)
• Move Cursor: Pinch Thumb & Index finger.
• Left Click / Drag: Pinch Thumb & Middle finger. Hold to drag.
• Zoom: Pinch Middle fingers on BOTH hands and pull apart.

2. FACE & EYE TRACKING (Hybrid Control)
• Nose Mouse: Turn on in the UI. Keep your hand pinched (Clutch) to move the cursor with your head.
• YouTube Shorts Scrolling: Wink Left Eye to scroll Up. Wink Right Eye to scroll Down. 
• Auto-Sleep: If no face is detected, media pauses instantly. PC sleeps after the custom UI timer.

3. TROUBLESHOOTING & LIMITATIONS
• Lighting & Clarity: The AI requires moderate room lighting. Severe backlighting or deep shadows will cause the face mesh to lose eye tracking. 
• Glasses: Thick-rimmed glasses or glare on lenses may interfere with blink detection.
• Multiple Persons: The AI is hardcoded to track a single face for cursor stability. If a second person enters the frame, the tracking may aggressively jump between you.
• Jittery Cursor? Increase 'Face Smoothening' in the settings.
    """
    
    # Using a Text widget so it's easy to read and scroll if needed
    text_box = tk.Text(frame, bg="#0B0F19", fg="#E2E8F0", font=("Consolas", 11), 
                       wrap="word", bd=1, relief="solid", padx=15, pady=15)
    text_box.insert("1.0", guide_text)
    text_box.config(state="disabled") # Make it read-only so user can't type in it
    text_box.pack(fill="both", expand=True, padx=25, pady=(0, 25))
    
    return frame