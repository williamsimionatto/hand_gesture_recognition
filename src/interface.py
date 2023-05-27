import tkinter as tk
import cv2
from PIL import ImageTk, Image

def close_window(event):
    root.destroy()

def update_webcam():
    ret, frame = cap.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (webcam_width, webcam_height))

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        webcam_label.config(image=img_tk)
        webcam_label.image = img_tk
        webcam_label.config(text="")
    else:
        webcam_label.config(image="")
        webcam_label.config(text="Webcam Unavailable")
        webcam_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    webcam_label.after(1, update_webcam)

root = tk.Tk()
root.title("Hand Gesture Recognition")
root.state('zoomed')

root.bind("<Escape>", close_window)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

webcam_width = int(screen_width * 0.7)
webcam_height = screen_height

webcam_container = tk.Frame(root, width=webcam_width, height=webcam_height, borderwidth=1)
webcam_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

info_width = int(screen_width * 0.3)
info_height = screen_height

info_container = tk.Frame(root, width=info_width, height=info_height, borderwidth=1)
info_container.pack(side=tk.LEFT, fill=tk.BOTH)

webcam_label = tk.Label(webcam_container)
webcam_label.pack(pady=20)

cap = cv2.VideoCapture(0)

update_webcam()

root.mainloop()