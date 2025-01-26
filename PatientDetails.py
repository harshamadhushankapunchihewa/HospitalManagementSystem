import tkinter as tk
import pyodbc

def search_patient():
    query = search_entry.get()
    if not query:
        result_label.config(text="Please enter a patient ID.")
        return

    connection_string = "Driver={SQL Server};Server=DESKTOP-Q6P1DJ6;Database=DATABASE8;Trusted_Connection=yes;"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patient WHERE PID = ?", (query,))
    patient = cursor.fetchone()

    if patient:
        result_label.config(text=f"Patient ID: {patient[0]}\n"
                                 f"Name: {patient[1]}\n"
                                 f"Condition: {patient[2]}\n"
                                 f"Gender: {patient[3]}\n"
                                 f"Age: {patient[4]}\n"
                                 f"Room ID: {patient[5]}\n")
    else:
        result_label.config(text=f"Patient with ID {query} not found.")

    conn.close()

def reset_search():
    search_entry.delete(0, tk.END)
    result_label.config(text="")

def page():
    root = tk.Tk()
    root.title("Patient Search")
    root.geometry("400x400")

    search_label = tk.Label(root, text="Enter Patient ID:")
    search_label.pack(pady=10)

    global search_entry  # Make search_entry global so it can be accessed in other functions
    search_entry = tk.Entry(root)
    search_entry.pack(pady=10)

    search_button = tk.Button(root, text="Search", command=search_patient)
    search_button.pack()

    reset_button = tk.Button(root, text="Reset", command=reset_search)
    reset_button.pack()

    global result_label  # Make result_label global so it can be accessed in other functions
    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    root.mainloop()

# Call the page() function to create the GUI

