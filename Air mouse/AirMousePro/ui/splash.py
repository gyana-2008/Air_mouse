import tkinter as tk
from tkinter import ttk

class SplashApp:
    def __init__(self, on_finish):
        self.root = tk.Tk()
        self.on_finish = on_finish
        
        # Remove standard window borders and title bar
        self.root.overrideredirect(True)
        
        # Center the splash screen on a standard 1080p monitor
        self.root.geometry("480x280+500+250")
        self.root.configure(bg="#0B0F19") 

        # Draw the logo using Canvas
        c = tk.Canvas(self.root, width=100, height=80, bg="#0B0F19", highlightthickness=0)
        c.pack(pady=(30, 10))
        c.create_polygon(30, 25, 35, 15, 65, 15, 70, 25, outline="#00E5FF", width=2, fill="#0B0F19")
        c.create_rectangle(15, 25, 85, 70, outline="#00E5FF", width=2, fill="#151B2B")
        c.create_oval(35, 32, 65, 62, outline="#10B981", width=3)
        c.create_oval(45, 42, 55, 52, fill="#10B981")
        c.create_oval(70, 32, 76, 38, fill="#00E5FF")

        # Labels
        tk.Label(self.root, text="AIRMOUSE PRO", font=("Segoe UI", 18, "bold"), fg="#FFFFFF", bg="#0B0F19").pack()
        self.lbl_status = tk.Label(self.root, text="Waking Neural Vision Engine...", font=("Segoe UI", 9), fg="#00E5FF", bg="#0B0F19")
        self.lbl_status.pack(pady=(5, 15))

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=380, mode="determinate")
        self.progress.pack()
        
        self.step = 0
        self.animate()
        
    def run(self):
        # Start the Tkinter loop for the splash screen
        self.root.mainloop()

    def animate(self):
        self.step += 12
        self.progress['value'] = self.step
        
        # Update status text as it loads
        stages = {
            30: "Calibrating Optical Sensors...", 
            60: "Loading Spatial Meshes...", 
            90: "Locking User Targets..."
        }
        for k, v in stages.items():
            if self.step >= k: 
                self.lbl_status.config(text=v)
        
        # Loop animation or finish
        if self.step < 100: 
            self.root.after(200, self.animate)
        else: 
            self.root.after(300, self.finish)

    def finish(self):
        # Destroy the splash screen and trigger the main app
        self.root.destroy()
        self.on_finish()