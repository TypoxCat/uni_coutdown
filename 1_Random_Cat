import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Initialize window
root = tk.Tk()
root.title("Your daily cat dose")
root.minsize(300, 300)
root.config(bg="#e0dfdc")

# Fonts & colors
FONT_HEADER = ("Helvetica Neue", 20, "bold")
FONT_TEXT = ("Helvetica Neue", 12)
FONT_BUTTON = ("Helvetica Neue", 12, "bold")
COLOR_BG = "#e0dfdc"
COLOR_ENTRY = "#2c2c2c"
COLOR_TEXT = "#f5f5f5"
BUTTON_TEXT = "#2c2c2c"
COLOR_ACCENT = "#888"
COLOR_HIGHLIGHT = "#b4b4b4"

# Title label
title = tk.Label(root, text="Car Says...", font=FONT_HEADER, bg=COLOR_BG, fg="#333")
title.pack(pady=(15, 5))

# Entry label
entry_label = tk.Label(root, text="What should your car say?", font=FONT_TEXT, bg=COLOR_BG, fg="#555")
entry_label.pack()

entry = tk.Entry(
    root,
    font=FONT_TEXT,
    width=30,
    bg=COLOR_ENTRY,
    fg=COLOR_TEXT,
    insertbackground=COLOR_TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=COLOR_HIGHLIGHT,
    highlightcolor=COLOR_HIGHLIGHT
)
entry.pack(pady=8, ipady=6)

image_frame = tk.Frame(root, width=400, height=250, bg="#ccc", relief="ridge", bd=1)
image_frame.pack(pady=10)
label = tk.Label(image_frame, bg="#ccc")
label.pack()

def catWithText():
    text = entry.get().strip()
    if not text:
        url = "https://cataas.com/cat"
    else:
        url = f"https://cataas.com/cat/says/{text}?position=center&font=Impact&fontSize=50&fontColor=%23fff&fontBackground=none"
    getCat(url)


# Get the image and print it in the window
def getCat(URL):
    try:
        # Make a GET request
        response = requests.get(url=URL, timeout=5)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Use RAM
            image_data = BytesIO(response.content)
            pil_image = Image.open(image_data)

            # Resize while keeping aspect ratio
            max_size = (400, 250)
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Convert to ImageTk format
            tk_image = ImageTk.PhotoImage(pil_image)

            # Display image in label
            label.config(image=tk_image)
            label.image = tk_image  # Keep a reference to avoid garbage collection
            
            # Resize window to fit image
            root.geometry("")
            root.update_idletasks()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: duh {e}")

# Buttons
fetch_button = tk.Button(
    root,
    text="Give me my car 🐾",
    font=FONT_BUTTON,
    width=25,
    bg="#333",
    fg=BUTTON_TEXT,
    activebackground="#444",
    activeforeground=COLOR_TEXT,
    relief="flat",
    command=catWithText
)
fetch_button.pack(pady=6)

close_button = tk.Button(
    root,
    text="Close",
    font=FONT_BUTTON,
    width=25,
    bg="#888",
    fg=BUTTON_TEXT,
    activebackground="#777",
    activeforeground=COLOR_TEXT,
    relief="flat",
    command=root.destroy
)
close_button.pack(pady=(4, 20))

root.mainloop()