import tkinter as tk
from tkinter import ttk

# Import the tab modules
from ui.tabs import tab_home, tab_hand_mouse, tab_hand_gestures, tab_face_mouse, tab_eye_mouth, tab_guide

class AirMouseUI:
    def __init__(self, settings_manager):
        self.settings = settings_manager
        
        self.root = tk.Tk()
        self.root.title("AirMouse Pro - Workspace for G.R.Parida")
        self.root.geometry("900x700")
        self.root.configure(bg="#0B0F19")

        self.setup_styles()

        # Create Notebook (Tab Container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.build_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#0B0F19", borderwidth=0)
        style.configure("TNotebook.Tab", background="#151B2B", foreground="#64748B", 
                        padding=[20, 10], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#00E5FF")], foreground=[("selected", "#0B0F19")])

    def build_tabs(self):
        # Load each tab from its respective file
        t_home = tab_home.create_tab(self.notebook, self.settings)
        t_hand = tab_hand_mouse.create_tab(self.notebook, self.settings)
        t_gest = tab_hand_gestures.create_tab(self.notebook, self.settings)
        t_face = tab_face_mouse.create_tab(self.notebook, self.settings)
        t_eye = tab_eye_mouth.create_tab(self.notebook, self.settings)
        t_guide = tab_guide.create_tab(self.notebook, self.settings)

        # Add them to the notebook
        self.notebook.add(t_home, text="Home")
        self.notebook.add(t_hand, text="Hand Mouse")
        self.notebook.add(t_gest, text="Hand Gestures")
        self.notebook.add(t_face, text="Face Mouse")
        self.notebook.add(t_eye, text="Eye & Mouth")
        self.notebook.add(t_guide, text="Guide")