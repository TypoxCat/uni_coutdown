import rumps
import time
import threading
import os
import subprocess
import sys

class CatPomodoroApp(rumps.App):
    def __init__(self):
        super().__init__("🐾 Pomocat", quit_button="Give up")
        self.menu = ["Start Pomodoro", None, "Stats", None, "Reset"]
        self.focus_duration = 0
        self.rest_duration = 0
        self.total_sessions = 0
        self.sessions_completed = 0
        self.active = False

    def ask_user_config(self):
        try:
            self.focus_duration = int(rumps.Window(
                "Focus duration (minutes):", "Setup").run().text)
            self.rest_duration = int(rumps.Window(
                "Rest duration (seconds):", "Setup").run().text)
            self.total_sessions = int(rumps.Window(
                "How many focus sessions today?", "Setup").run().text)
        except:
            return False
        return True

    @rumps.clicked("Start Pomodoro")
    def start_pomodoro(self, _=None):
        if self.active:
            return
        if not self.ask_user_config():
            return
        
        self.active = True
        self.sessions_completed = 0
        self.update_menu()
        threading.Thread(target=self.run_pomodoro).start()

    def update_menu(self):
        self.menu["Stats"].title = f"Session: {self.sessions_completed}/{self.total_sessions}"


    def run_pomodoro(self):
        for _ in range(self.total_sessions):
            if not self.timer(self.focus_duration * 60, "focus"):
                return
            self.sessions_completed += 1
            self.update_menu()

            # Get the absolute path to blackout.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            blackout_path = os.path.join(script_dir, "blackout.py")
            subprocess.Popen([sys.executable, blackout_path, str(self.rest_duration)])
            if not self.timer(self.rest_duration, "rest"):
                return
        self.active = False
        self.title = "🐾 Pomocat"

    def timer(self, duration, mode):
        start = time.time()
        end = start + duration
        while time.time() < end:

            remaining = int(end - time.time())
            mins = remaining // 60
            secs = remaining % 60
            label = f"🐾 {mode.title()}: {mins:02}:{secs:02}"
            self.title = label
            time.sleep(1)

        self.title = "🐾 Pomocat"
        return True

    @rumps.clicked("Reset")
    def reset_app(self, _=None):
        self.active = False
        self.sessions_completed = 0
        self.menu["Start Pomodoro"].set_callback(self.start_pomodoro)
        self.update_menu()
    

if __name__ == "__main__":
    CatPomodoroApp().run()
