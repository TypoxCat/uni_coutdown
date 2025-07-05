# blackout.py
import tkinter as tk
import sys

duration = int(sys.argv[1]) if len(sys.argv) > 1 else 30  # seconds

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.after(duration * 1000, root.destroy)
root.mainloop()