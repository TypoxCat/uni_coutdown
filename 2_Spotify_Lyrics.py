import asyncio
import tkinter as tk
import subprocess
import threading
import time
import re
from syncedlyrics_aio import search as fetch_lrc

# --- Spotify detection (macOS) ---
def get_current_track():
    script = '''
    tell application "Spotify"
      if it is running and player state is playing then
        set t to name of current track
        set a to artist of current track
        return t & " - " & a
      else
        return ""
      end if
    end tell'''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return res.stdout.strip()

def get_spotify_position():
    script = 'tell application "Spotify" to player position'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    try:
        return float(result.stdout.strip()) + 0.2
    except:
        return 0.0

# --- LRC parser ---
def parse_lrc(lrc_text):
    pattern = re.compile(r'\[(\d+):(\d+\.\d+)\](.*)')
    data = []
    for line in lrc_text.strip().splitlines():
        m = pattern.match(line)
        if m:
            t = int(m[1]) * 60 + float(m[2])
            text = m[3].strip()
            data.append((t, text))
    return data

# --- Async-safe wrapper for asyncio
def fetch_lyrics_sync(track_title):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(fetch_lrc(track_title, plain_only=False, synced_only=True))
    finally:
        loop.close()

# --- GUI Setup ---
root = tk.Tk()
root.title("Floating Lyrics")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.5)
root.config(bg="black")

text_box = tk.Text(
    root,
    fg="white",
    bg="black",
    font=("Helvetica", 17),
    wrap="word",
    relief="flat",
    height=2,
    padx=10,
    pady=10
)
text_box.pack(fill="both", expand=True)
text_box.configure(state="disabled")

def update_text(content):
    text_box.configure(state="normal")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", content)
    text_box.configure(state="disabled")


root.update_idletasks()
root.minsize(600, 80)
root.geometry("600x20+10+10")

# --- Global state ---
current_track_title = ""
lyrics = []

# --- Lyrics fetch thread
def load_lyrics_for(track_title):
    def task():
        root.after(0, lambda: update_text(f"Loading lyrics for:\n{track_title}"))
        try:
            lrc = fetch_lyrics_sync(track_title)
            parsed = parse_lrc(lrc) if lrc else [(0, f"No synced lyrics found for:\n{track_title}")]
        except Exception as e:
            parsed = [(0, f"Error loading lyrics:\n{e}")]

        lyrics.clear()
        lyrics.extend(parsed)
    threading.Thread(target=task, daemon=True).start()

# --- Sync thread
def start_sync():
    def loop():
        global current_track_title, lyrics
        last_line = ""
        while True:
            new_title = get_current_track()
            if new_title and new_title != current_track_title:
                current_track_title = new_title
                load_lyrics_for(current_track_title)

            current_time = get_spotify_position()
            line = ""
            for i, (t, txt) in enumerate(lyrics):
                if t > current_time:
                    break
                line = txt

            if line != last_line:
                last_line = line
                root.after(0, lambda l=line: update_text(l))

            time.sleep(0.1)
    threading.Thread(target=loop, daemon=True).start()

# --- Start ---
start_sync()
root.mainloop()




# Detect sporify track MacOS, also detect when changing song, if ads then dont show anything
# Detect current song position
# GUI 
# GUI allow overlap app and keep on top
# Make it copyable