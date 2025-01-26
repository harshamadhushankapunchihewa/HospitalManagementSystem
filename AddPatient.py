import tkinter as tk
from tkinter import messagebox
import pyodbc

def add_patient_page():
    add_patient_window = tk.Tk()
    add_patient_window.title("Add Patient")
    add_patient_window.geometry("400x400")

    def submit_patient():
        ID = full_name_entry.get()
        condition = condition_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        rfid = rfid_entry.get()

        if not ID or not age.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid Full Name and Age.")
        else:
            # Connect to the database
            connection_string = "Driver={SQL Server};Server=DESKTOP-Q6P1DJ6;Database=DATABASE8;Trusted_Connection=yes;"
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Insert RFID into RFIDTag table
            insert_rfid_query = "INSERT INTO RFIDTag (RID) VALUES (?)"
            rfid_values = (rfid,)
            cursor.execute(insert_rfid_query, rfid_values)

            # Insert the patient details into the database
            insert_patient_query = """
                INSERT INTO Patient (PID, Condition, gender, age, RoomID, RID)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            patient_values = (ID, condition, gender, int(age), 102, rfid)  # Adjust RoomID accordingly
            cursor.execute(insert_patient_query, patient_values)

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Patient added successfully.")
            add_patient_window.destroy()

    title_label = tk.Label(add_patient_window, text="Add a Patient", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Full Name
    full_name_label = tk.Label(add_patient_window, text="ID :")
    full_name_entry = tk.Entry(add_patient_window, width=40)

    # Condition
    condition_label = tk.Label(add_patient_window, text="Condition:")
    condition_entry = tk.Entry(add_patient_window, width=40)

    # Gender
    gender_label = tk.Label(add_patient_window, text="Gender:")
    gender_entry = tk.Entry(add_patient_window, width=40)

    # Age
    age_label = tk.Label(add_patient_window, text="Age:")
    age_entry = tk.Entry(add_patient_window, width=40)

    # RFID
    rfid_label = tk.Label(add_patient_window, text="RFID:")
    rfid_entry = tk.Entry(add_patient_window, width=40)

    submit_button = tk.Button(add_patient_window, text="Submit", command=submit_patient)

    full_name_label.pack()
    full_name_entry.pack()
    condition_label.pack()
    condition_entry.pack()
    gender_label.pack()
    gender_entry.pack()
    age_label.pack()
    age_entry.pack()
    rfid_label.pack()
    rfid_entry.pack()
    submit_button.pack()

    add_patient_window.mainloop()

add_patient_page()
