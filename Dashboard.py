import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import json

# Opening JSON file
with open('data_dashboard.json') as f:
    data = json.load(f)

image_list = []

def on_container_button_click(counter):
    def handler(event):
        left_click(data['items'][counter]['Name'])
    return handler

def left_click(name):
    if name == "General Overview":
        import GeneralOverview
        GeneralOverview.page1()
    if name == "Camera Access":
        import CameraAccess as camera
        try:
            cam = camera.CameraAccess()
            cam.open_camera_access()
        except:
            print("something went wrong")
    if name == "View Patients":
        import PatientDetails
        PatientDetails.page()
    if name == "Add Patient":
        import AddPatient
        AddPatient.add_patient_page()
    if name == "Alerts":
        import Alerts
        Alerts.main()
    if name == "Logout":
        dashboard_window.destroy()
        import main
        main.main()

def show_dashboard(username):
    global dashboard_window
    dashboard_window = tk.Tk()
    dashboard_window.title("Patients Software")
    dashboard_window.geometry("1200x800")
    dashboard_window.configure(background='#D9D9D9')

    # Create Login Frame
    dashboard_container = tk.Frame(dashboard_window)
    dashboard_container.configure(background="#E4E4E4")  # this one!!!

    dashboard_container.grid(row=1, column=0, sticky="nsew", padx=50, pady=50, ipady=40)  # Make it expand vertically
    dashboard_title = tk.Label(master=dashboard_container, text="Dashboard", font=("Helvetica", 22, "bold"),
                                background="#E4E4E4")

    dashboard_title.grid(row=0, column=0, sticky="w", pady=20, padx=40)

    dashboard_user_welcome = tk.Label(master=dashboard_container, text=f"Welcome, {username}!", font=("Helvetica", 13),
                                       background="#E4E4E4")
    dashboard_user_welcome.grid(row=1, column=0, sticky="w", pady=2, padx=40)
    seperator = ttk.Separator(dashboard_container, orient='horizontal')
    seperator.grid(row=2, column=0, sticky="we", columnspan=9, padx=50, pady=30)

    # Load and resize images in advance
    image_list = [Load_And_Resize_Image(counter) for counter in range(len(data['items']))]

    counter = 0
    for i in range(2):
        for j in range(3):
            if counter < len(data['items']):
                container_button = tk.Frame(dashboard_container, background=data['items'][counter]['Color'])
                image_label = ttk.Label(master=container_button, image=image_list[counter],
                                        background=data['items'][counter]['Color'])
                login_label = ttk.Label(container_button, text=data['items'][counter]['Name'], font=("Roboto", 16))

                image_label.pack(pady=20)
                login_label.pack(pady=6, padx=10)
                login_label.configure(background=data['items'][counter]['Color'], foreground="white")
                container_button.bind("<Button-1>", on_container_button_click(counter))
                container_button.grid(row=i + 3, column=j, padx=50, pady=20, ipadx=30, sticky="nsew")

                counter += 1

    dashboard_window.resizable(False, False)
    dashboard_window.mainloop()

def Load_And_Resize_Image(counter):
    img_path = data['items'][counter]['Image_Path']
    image = Image.open(img_path)
    new_size = (70, 70)
    resized_image = image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    return photo

if __name__ == '__main__':
    show_dashboard("Username")
