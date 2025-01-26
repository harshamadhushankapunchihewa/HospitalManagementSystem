import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import constants, CENTER
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter import Scrollbar

# Create a Tkinter window
root = ttk.Window()
root.title("Patient Detail Screen ")

st = ttk.ScrolledText(root, )


# Center the window on the screen

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 800
window_height = 700
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry("1100x900")
# root.resizable(False, False)

# Define patient data (replace with your data)
patient_data = {
    "name": "John Doe",
    "age": 35,
    "condition": "Hypertension",
    "rfid_status": "Active",
    "location": "Room 101",
}

# Load patient image (replace 'patient_image.jpg' with the actual image file)
image_path = 'trevor.jpg'
image = Image.open(image_path)
image = image.resize((100, 100), Image.LANCZOS)  # Resize image to fit the GUI
photo = ImageTk.PhotoImage(image)
frame = ttk.Frame(root, bootstyle="secondary", padding=30)
frame.configure()

name_label = ttk.Label(root, bootstyle="", text="Patient Details", font=("Helvetica", 30, "bold"), )


name_label.pack(fill="x",padx=170, pady=20)

separator = ttk.Separator(root, orient='horizontal')

gridu = ttk.Frame(root )
#
# # Create labels and display patient data
image_label = ttk.Label(gridu, image=photo, anchor=ttk.CENTER)
image_label.grid(column=0, row=0)
# #




name_label = ttk.Label(gridu, text="Trevor Philips", anchor=ttk.CENTER, font=("Helvetica", 22), )
name_label.grid(column=1, row=0, ipadx=20)

gridu.pack(fill="x",padx=170, pady=5)

separator.pack(fill='x', pady=20, padx=50)

x = [1, 2, 2, 2, 2, 2, 2]
for y in range(4):
    container = ttk.Frame(frame)
    container.grid(row=0, column=y, pady=20, padx=20)

    image_label = ttk.Label(container, image=photo, bootstyle="inverse light", anchor=ttk.CENTER)
    image_label.grid(row=1, column=y, padx=10, pady=10, columnspan=2)

    name_label = ttk.Label(container, text="Patient Detailed", font=("Helvetica", 14, "bold"),

                           anchor=ttk.CENTER)
    name_label.grid(row=2, column=y, sticky="w", padx=10, pady=5, columnspan=2)
    name_value = ttk.Label(container, text=patient_data["name"], font=("Helvetica", 10,), bootstyle="inverse light", )
    name_value.grid(row=3, column=y, padx=10, pady=5, columnspan=2)

for y in range(4):
    container = ttk.Frame(frame)
    container.grid(row=4, column=y, pady=20, padx=20)

    image_label = ttk.Label(container, image=photo, bootstyle="inverse light", anchor=ttk.CENTER)
    image_label.grid(row=5, column=y, padx=10, pady=10, columnspan=2)

    name_label = ttk.Label(container, text="Patient Detailed", font=("Helvetica", 14, "bold"),
                           bootstyle="inverse light",
                           anchor=ttk.CENTER)
    name_label.grid(row=6, column=y, sticky="w", padx=10, pady=5, columnspan=2)
    name_value = ttk.Label(container, text=patient_data["name"], font=("Helvetica", 10,), bootstyle="inverse light", )
    name_value.grid(row=7, column=y, padx=10, pady=5, columnspan=2)
frame.pack()
root.configure(bg="#D9D9D9")

root.resizable(False, False)
# Run the Tkinter main loop
root.mainloop()
