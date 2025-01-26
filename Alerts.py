import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc

connection_string = "Driver={SQL Server};Server=DESKTOP-Q6P1DJ6;Database=DATABASE8;Trusted_Connection=yes;"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


def get_names_from_database():
    cursor.execute("SELECT PName FROM Patient")
    return [row[0] for row in cursor.fetchall()]


def get_floors_from_database():
    cursor.execute("SELECT RoomID FROM Room")
    return [int(row[0]) for row in cursor.fetchall()]


def on_dropdown_select(event, selected_value, combobox=None):
    if combobox is not None:
        selected_value.set(combobox.get())


def create_alert(selected_value1, selected_value2, selected_value3):
    selected_name = selected_value1.get()
    selected_floor = selected_value2.get()  # Cast to int
    selected_priority = selected_value3.get()

    names = get_names_from_database()
    floors = get_floors_from_database()
    priorities = ["Low", "Medium", "High"]

    if selected_name not in names:
        messagebox.showerror("Name Not Found", f"Name '{selected_name}' not found.")
    elif selected_floor not in floors:
        messagebox.showerror("Floor Not Found", f"Floor '{selected_floor}' not found.")
    elif selected_priority not in priorities:
        messagebox.showerror("Priority Not Found", f"Priority '{selected_priority}' not found.")
    else:
        # Replace this with the code to create an alert, e.g., save to the database or trigger an action.
        messagebox.showinfo("Alert Created", "Alert created successfully!")


def main():
    names = get_names_from_database()
    priorities = ["Low", "Medium", "High"]

    # Fetch floors as integers
    floors = get_floors_from_database()

    root = tk.Tk()
    root.title("Alert Creation")
    root.geometry("1080x800")

    combobox_frame = tk.Frame(root)
    combobox_frame.pack(padx=10, pady=10)

    background_frame = tk.Frame(combobox_frame, bg="gray")
    background_frame.pack(fill="both", expand=True, padx=1, pady=200)

    title_label = tk.Label(background_frame, text="Alert Creation", font=("Helvetica", 28))
    title_label.pack(side='top', padx=10, pady=10)

    selected_value1 = tk.StringVar()
    selected_value2 = tk.StringVar()
    selected_value3 = tk.StringVar()

    combobox1 = ttk.Combobox(background_frame, textvariable=selected_value1, values=names, width=90, height=5)
    combobox1.pack(side='top', padx=10, pady=10)
    combobox1.set("Name Selection")

    combobox2 = ttk.Combobox(background_frame, textvariable=selected_value2, values=floors, width=90, height=5)
    combobox2.pack(side='top', padx=10, pady=10)
    combobox2.set("Last known floor")

    combobox3 = ttk.Combobox(background_frame, textvariable=selected_value3, values=priorities, width=90, height=5)
    combobox3.pack(side='top', padx=10, pady=10)
    combobox3.set("Priority")

    combobox1.bind("<<ComboboxSelected>>", lambda event, sv=selected_value1: on_dropdown_select(event, sv))
    combobox2.bind("<<ComboboxSelected>>", lambda event, sv=selected_value2: on_dropdown_select(event, sv))
    combobox3.bind("<<ComboboxSelected>>", lambda event, sv=selected_value3: on_dropdown_select(event, sv))

    create_button = tk.Button(combobox_frame, text="Create Alert",
                             command=lambda: create_alert(selected_value1, selected_value2, selected_value3),
                             font=("Helvetica", 16))
    create_button.pack(side='bottom', pady=10)

    root.mainloop()



