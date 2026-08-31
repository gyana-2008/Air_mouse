import queue
import threading
from settingmanager import SettingsManager
from ui.app import AirMouseUI
from core.action_executor import ActionExecutor
from vision.vision_engine import VisionEngine
from ui.splash import SplashApp  # Import the new splash screen

def main():
    print("Initializing Core Systems...")
    settings = SettingsManager()
    
    # Create the central communication hub
    command_queue = queue.Queue()
    
    # Start Thread 3 (Action Executor)
    executor = ActionExecutor(command_queue, settings)
    executor_thread = threading.Thread(target=executor.run, daemon=True)
    executor_thread.start()
    
    # Start Thread 2 (Vision Engine)
    vision = VisionEngine(settings, command_queue)
    vision.start()
    
    # Define what happens AFTER the splash screen finishes
    def launch_main_app():
        # Start Thread 1 (Main UI)
        app = AirMouseUI(settings)
        app.root.mainloop()

        # Clean up background threads when the main UI closes
        vision.stop()
        executor.running = False
        print("AirMouse Pro shut down cleanly.")

    # Show splash screen first, then launch main app
    splash = SplashApp(on_finish=launch_main_app)
    splash.run()

if __name__ == "__main__":
    main()