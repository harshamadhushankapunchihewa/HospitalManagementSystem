import tkinter as tk
import pyodbc

def show_timestamp_log():
    connection_string = "Driver={SQL Server};Server=DESKTOP-Q6P1DJ6;Database=DATABASE8;Trusted_Connection=yes;"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Fetch the RFID log data from TimestampTbl
    cursor.execute("SELECT TOP 10 RID, TimeIN, CurrentRoom FROM TimestampTbl ORDER BY TimeIN DESC")
    timestamp_log = cursor.fetchall()

    log_text.delete(1.0, tk.END)  # Clear the text widget

    for entry in timestamp_log:
        log_text.insert(tk.END, f"RFID: {entry[0]}\n"
                               f"Time In: {entry[1]}\n"
                               f"Current Room: {entry[2]}\n\n")

    conn.close()

def page1():
    root = tk.Tk()
    root.title("Timestamp Log")
    root.geometry("400x400")

    global log_text
    log_text = tk.Text(root, width=50, height=10)
    log_text.pack(pady=10)

    show_button = tk.Button(root, text="Show Timestamp Log", command=show_timestamp_log)
    show_button.pack()

    root.mainloop()

# Call the page function to set up the UI
