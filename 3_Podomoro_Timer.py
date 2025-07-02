import rumps
import time
import threading
import random
import subprocess

class CatPomodoroApp(rumps.App):
    def __init__(self):
        super().__init__("🐾 Pomocat", quit_button="Give up")
        self.menu = ["Start Pomodoro", None, "Stats", None, "Reset"]
        self.cat_state = "🐱"
        self.focus_duration = 0
        self.rest_duration = 0
        self.total_sessions = 0
        self.sessions_completed = 0
        self.active = False
        self.cancel_count = 0
        self.cat_growth = ["(・ω・)", "(=^･ω･^=)", "(=①ω①=)", "(=^･^=)"]
        self.notification_thread = None

    def notify(self, title, message):
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "{title}"'
        ])

    def ask_user_config(self):
        try:
            self.focus_duration = int(rumps.Window(
                "Focus duration (minutes):", "Setup").run().text)
            self.rest_duration = int(rumps.Window(
                "Rest duration (seconds):", "Setup").run().text)
            self.total_sessions = int(rumps.Window(
                "How many focus sessions today?", "Setup").run().text)
        except:
            self.notify("Pomocat", "Invalid input. Try again.")
            return False
        return True

    @rumps.clicked("Start Pomodoro")
    def start_pomodoro(self, _=None):
        if self.active:
            self.notify("Pomocat", "Already running!")
            return
        if not self.ask_user_config():
            return
        self.active = True
        self.sessions_completed = 0
        self.cancel_count = 0
        self.update_menu()
        threading.Thread(target=self.run_pomodoro).start()
        self.notification_thread = threading.Thread(target=self.random_motivation)
        self.notification_thread.daemon = True
        self.notification_thread.start()

    def update_menu(self):
        progress = f"{self.cat_growth[min(self.sessions_completed, len(self.cat_growth)-1)]} {self.sessions_completed}/{self.total_sessions} sessions"
        self.menu["Stats"].title = progress
        self.update_touchbar_progress()

    def update_touchbar_progress(self):  # 👈 NEW
        kaomojis = self.cat_growth
        foods = ["🍚", "🍖", "🍗", "🥩", "🍣"]
        goal = "[🏁]"

        done = self.sessions_completed
        total = self.total_sessions

        food_trail = " ".join(foods[i % len(foods)] for i in range(done))
        cat = kaomojis[min(done, len(kaomojis) - 1)]

        if done >= total:
            text = f"{cat}💤 Full & proud!"
        else:
            empty = "▫️ " * (total - done)
            text = f"{food_trail} {cat} {empty}{goal}"

        subprocess.run([
            "osascript", "-e",
            f'tell application "BetterTouchTool" to update_touch_bar_widget "pomocat_progress" text "{text.strip()}"'
        ])

    def random_motivation(self):
        quotes = [
            "Keep going, hooman. I'm watching you 👁️",
            "No slacking. Cat is judging 😼",
            "Your success feeds me. Literally 🍖",
            "You want treats or regrets? Work. 🐾",
            "Procrastinate again and I'm napping on your keyboard."
        ]
        while self.active:
            time.sleep(300)
            if self.active:
                self.notify("Pomocat Motivation", random.choice(quotes))

    def run_pomodoro(self):
        for _ in range(self.total_sessions):
            self.notify("Pomocat", "Focus time starts now!")
            if not self.timer(self.focus_duration * 60, "focus"):
                return
            self.sessions_completed += 1
            self.update_menu()
            self.notify("Pomocat", "Focus done! Time to rest your eyes 😴")
            if not self.timer(self.rest_duration, "rest"):
                return
        self.notify("Pomocat", "All sessions done! Cat is proud 😻")
        self.active = False
        self.title = "🐾 Pomocat"

    def timer(self, duration, mode):
        start = time.time()
        end = start + duration
        while time.time() < end:
            if not self.active:
                self.notify("Pomocat", f"Canceled {mode}. Cat is disappointed 😾")
                self.cancel_count += 1
                if self.cancel_count >= 3:
                    self.notify("Pomocat", "Too many cancels. Cat refuses to restart.")
                    self.menu["Start Pomodoro"].set_callback(None)
                self.title = "🐾 Pomocat"
                return False

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
        self.cancel_count = 0
        self.menu["Start Pomodoro"].set_callback(self.start_pomodoro)
        self.update_menu()

if __name__ == "__main__":
    CatPomodoroApp().run()
