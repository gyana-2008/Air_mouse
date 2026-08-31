import pyautogui
import queue
import time

class ActionExecutor:
    def __init__(self, command_queue, settings):
        self.queue = command_queue
        self.settings = settings
        self.running = True
        
        pyautogui.FAILSAFE = False 
        pyautogui.PAUSE = 0  

    def run(self):
        while self.running:
            try:
                cmd = self.queue.get(timeout=0.1)
                self.process_command(cmd)
            except queue.Empty:
                continue

    def process_command(self, cmd):
        action = cmd[0]
        
        if action != "MOVE":
            print(f"⚙️ EXECUTING COMMAND: {cmd}")
        
        # ==========================================
        # 1. CORE MOUSE ACTIONS (Including Holds)
        # ==========================================
        if action == "MOVE":
            _, x, y = cmd
            pyautogui.moveTo(x, y)
        elif action == "LEFT_DOWN":
            pyautogui.mouseDown(button='left')
        elif action == "LEFT_UP":
            pyautogui.mouseUp(button='left')
        elif action == "RIGHT_DOWN":
            pyautogui.mouseDown(button='right')
        elif action == "RIGHT_UP":
            pyautogui.mouseUp(button='right')
            
        elif action == "LEFT_CLICK":
            pyautogui.click()
        elif action == "DOUBLE_CLICK":
            pyautogui.doubleClick()
        elif action == "RIGHT_CLICK":
            pyautogui.rightClick()
        elif action == "MIDDLE_CLICK":
            pyautogui.middleClick()
        elif action == "SCROLL":
            _, amount = cmd
            pyautogui.scroll(amount)
            
        # ==========================================
        # 2. WINDOWS SHORTCUTS
        # ==========================================
        elif action == "ALT_TAB":
            pyautogui.keyDown('alt')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.keyUp('alt')
            
        elif action == "WIN_TAB":
            pyautogui.keyDown('win')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.keyUp('win')
            
        elif action == "HOTKEY":
            _, *keys = cmd
            pyautogui.hotkey(*keys)
            
        elif action == "PRESS":
            _, key = cmd
            pyautogui.press(key)
            
        elif action == "SCREENSHOT":
            pyautogui.screenshot(f"AirMouse_Capture_{int(time.time())}.png")
            
        # ==========================================
        # 3. DYNAMIC ROUTED ACTIONS (UI MACROS)
        # ==========================================
        elif action == "ROUTED_ACTION":
            _, routed_cmd = cmd
            
            # --- EYE CLICK FALLBACKS ---
            # If the user sets an eye to "click" but the logic sends it here
            if routed_cmd == "LEFT_CLICK": pyautogui.click()
            elif routed_cmd == "RIGHT_CLICK": pyautogui.rightClick()
            
            # --- STANDARD MACROS ---
            elif routed_cmd == "MUTE": pyautogui.press('volumemute')
            elif routed_cmd == "ESC": pyautogui.press('esc')
            elif routed_cmd == "TASK_VIEW": pyautogui.hotkey('win', 'tab')
            elif routed_cmd == "SCREENSHOT": pyautogui.screenshot(f"AirMouse_Capture_{int(time.time())}.png")
            elif routed_cmd == "PLAY_PAUSE": pyautogui.press('playpause')
            elif routed_cmd == "VOLUME_UP": pyautogui.press('volumeup')
            elif routed_cmd == "VOLUME_DOWN": pyautogui.press('volumedown')
            elif routed_cmd == "NEXT_TRACK": pyautogui.press('nexttrack')
            elif routed_cmd == "PREV_TRACK": pyautogui.press('prevtrack')
            
            elif routed_cmd == "ARROW_UP": pyautogui.press('up')
            elif routed_cmd == "ARROW_DOWN": pyautogui.press('down') 
            
            # --- CUSTOM USER MACROS ---
            elif routed_cmd == "MACRO_1":
                # Example: Copy
                pyautogui.hotkey('ctrl', 'c')
            elif routed_cmd == "MACRO_2":
                # Example: Paste
                pyautogui.hotkey('ctrl', 'v')
            elif routed_cmd == "MACRO_3":
                # Example: Open Notepad
                pyautogui.hotkey('win', 'r')
                time.sleep(0.2)
                pyautogui.write('notepad\n')
            elif routed_cmd == "MACRO_4":
                # Example: Save File
                pyautogui.hotkey('ctrl', 's')