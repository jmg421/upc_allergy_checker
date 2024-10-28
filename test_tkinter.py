import tkinter as tk
from tkinter import messagebox

def on_click():
    messagebox.showinfo("Test", "tkinter is working!")

root = tk.Tk()
root.title("tkinter Test")

test_button = tk.Button(root, text="Click Me", command=on_click)
test_button.pack(pady=20)

root.mainloop()

