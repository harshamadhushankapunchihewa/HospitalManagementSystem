import tkinter as tk
from PIL import Image, ImageTk
from tkinter import constants, CENTER
import Dashboard
from tkinter import messagebox


username_entry_box_text = ""
password_entry_box_text = ""
LOGIN_FRAME_COLOR_BG = "#E4E4E4"

root = ''

def main():
    global root
    root = tk.Tk()

    #db.Connect_To_Database()

    root.title("Patients Software")
    root.geometry("800x700")
    root.configure(background='#D9D9D9')

    # Create Login Frame
    login_frame = tk.Frame(root)

    login_label = tk.Label(login_frame, text="Login", font=("Roboto", 22, "bold"), background=LOGIN_FRAME_COLOR_BG)
    username_label = tk.Label(login_frame, text="Username:", background=LOGIN_FRAME_COLOR_BG, font=("Helvetica", 12))
    username_input_box = tk.Entry(login_frame, width=75)

    password_label = tk.Label(login_frame, text="Password:", background=LOGIN_FRAME_COLOR_BG, font=("Helvetica", 12))
    password_input_box = tk.Entry(login_frame, width=75)

    login_button = tk.Button(login_frame, text="Login", takefocus=False, width=15,
                             command=lambda: check_credentials(username_input_box.get(), password_input_box.get()),
                            )


    container = tk.Frame(login_frame)
    server_connection_label = tk.Label(container, text="Server Connection:", background=LOGIN_FRAME_COLOR_BG,
                                       font=("Helvetica", 12))
    database_symbol_label = tk.Label(container, text="S:", background=LOGIN_FRAME_COLOR_BG, font=("Helvetica", 12))
    server_connection_label.grid(row=0, column=0)
    database_symbol_label.grid(row=0, column=1)

    image = Image.open("patient.png")  # Replace with your image file
    new_size = (100, 100)  # Set the desired size (width, height)
    resized_image = image.resize(new_size)

    # Convert the resized image to a PhotoImage object
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(login_frame, image=photo, background=LOGIN_FRAME_COLOR_BG)
    login_frame.place(anchor=CENTER, relx=.5, rely=.5)
    image_label.pack(padx=10, pady=30)
    login_label.pack(anchor='w', padx=30, pady=5)
    username_label.pack(anchor='w', padx=30, pady=5)
    username_input_box.pack(anchor="w", padx=30, pady=10)
    password_label.pack(anchor='w', padx=30, pady=5)
    password_input_box.pack(anchor='w', padx=30, pady=10)
    login_button.pack(anchor='center', padx=10, pady=30)
    container.pack(pady=20)
    root.resizable(False, False)
    root.mainloop()

def check_credentials(username, password):
    global root

    # Replace 'your_username' and 'your_password' with the actual valid username and password
    valid_username = "colombo"
    valid_password = "ecu"

    if username == valid_username and password == valid_password:
        messagebox.showinfo("Authentication Successful", "Welcome User to Patients Software!")
        root.destroy()
        Dashboard.show_dashboard(username)
    else:
        messagebox.showerror("Authentication Failed", "Either Username or Password is invalid!")

if __name__ == '__main__':
    main()

