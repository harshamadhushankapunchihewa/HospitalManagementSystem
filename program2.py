import cv2
import pyodbc
import tkinter as tk
from tkinter import messagebox
import threading

# Initialize a tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Replace these with your actual database connection details
server = 'DESKTOP-Q6P1DJ6'  # Update with your SQL Server instance name
database = 'DATABASE8'  # Update with the name of your database

try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database)
    cursor = conn.cursor()
except pyodbc.Error as e:
    messagebox.showerror("Database Error", "Error connecting to the database: " + str(e))
    exit(1)

# Function to create a named window and set its position
def create_window(window_name, x, y):
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, x, y)

# Function to detect face shape
def detect_face_shape(frame):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Loop over the detected faces
    for (x, y, w, h) in faces:
        # Draw a bounding box around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add text label for the detected face
        cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame, len(faces)

# Function to display alerts in a tkinter message box
def show_alert(message):
    messagebox.showwarning("Alert", message)

# Function to display count in a corner of the window
def display_count(frame, count, corner='top-left'):
    text = f'Humans: {count}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (0, 255, 0)
    margin = 10

    if corner == 'top-left':
        position = (margin, margin + 20)
    elif corner == 'top-right':
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        position = (frame.shape[1] - text_size[0] - margin, margin + 20)
    elif corner == 'bottom-left':
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        position = (margin, frame.shape[0] - margin)
    else:
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        position = (frame.shape[1] - text_size[0] - margin, frame.shape[0] - margin)

    cv2.putText(frame, text, position, font, font_scale, text_color, font_thickness)

# Input the camera IP address (enter only if there is a mobile or external cam, otherwise just press enter)
camera_ip = input("Enter the IP address of the camera (e.g., http://192.168.1.3:8080/video): ")

# Create connections to the webcam (usually 0 for the default webcam)
cap_webcam = cv2.VideoCapture(0)

# Check if an IP address for the mobile camera is provided
if camera_ip:
    # Create connections to the phone's camera feed
    cap_mobile = cv2.VideoCapture(camera_ip)  # Camera feed

    # Create windows for displaying the video feeds
    create_window('Webcam Feed', 0, 0)
    create_window('Mobile Camera Feed', 700, 0)

    # Flags to control counting and printing
    webcam_counting_started = False
    mobile_cam_counting_started = False
else:
    cap_mobile = None  # No IP address provided

    # Create windows for displaying the video feeds (only webcam)
    create_window('Webcam Feed', 0, 0)

    # Flags to control counting and printing (only webcam)
    webcam_counting_started = False

last_known_state = None

while True:
    try:

        # Read a frame from the phone's camera (if available)
        if cap_mobile is not None:
            ret_mobile, frame_mobile = cap_mobile.read()
            # Detect face shape in the mobile camera frame and count humans
            frame_mobile, num_faces_mobile = detect_face_shape(frame_mobile)

            display_count(frame_mobile, num_faces_mobile, corner='top-left')

            # Display the mobile camera frame in one window (if available)
            cv2.imshow('Mobile Camera Feed', frame_mobile)

        # Read a frame from the webcam
        ret_webcam, frame_webcam = cap_webcam.read()
        # Detect face shape in the webcam frame and count humans
        frame_webcam, num_faces_webcam = detect_face_shape(frame_webcam)

        display_count(frame_webcam, num_faces_webcam, corner='top-left')

        # Display the webcam frame in another window
        cv2.imshow('Webcam Feed', frame_webcam)

        # Display the count in the top-left corner of each window (if available)
        if cap_mobile is not None:
            display_count(frame_mobile, num_faces_mobile, corner='top-left')
        display_count(frame_webcam, num_faces_webcam, corner='top-left')
        cursor.execute("SELECT COUNT(*) FROM TimestampTbl")
        current_state = cursor.fetchone()[0]
        if last_known_state is None or current_state != last_known_state:
            cursor.execute("SELECT COUNT(DISTINCT RID) AS TotalPeopleInRoom1 FROM TimestampTbl AS tt WHERE CurrentRoom = 101 AND TIMESTAMP = (SELECT MAX(TIMESTAMP) FROM TimestampTbl WHERE RID = tt.RID) GROUP BY CurrentRoom")
            func1 = cursor.fetchone()

            cursor.execute(
                "SELECT COUNT(DISTINCT RID) AS TotalPeopleInRoom2 FROM TimestampTbl AS tt WHERE CurrentRoom = 102 AND TIMESTAMP = (SELECT MAX(TIMESTAMP) FROM TimestampTbl WHERE RID = tt.RID) GROUP BY CurrentRoom")
            func2 = cursor.fetchone()

            total_people_in_room1 = int(func1.TotalPeopleInRoom1)

            # Start playing sounds based on human face count (only if webcam)
            if not webcam_counting_started:
                if num_faces_webcam > total_people_in_room1:
                    show_alert("Alert from web cam")
        key = cv2.waitKey(1)
        # Input 'q' key to stop the program
        if key & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")
        continue

# Release the camera connections and close the windows
if cap_mobile is not None:
    cap_mobile.release()
cap_webcam.release()

# Close the tkinter window
root.destroy()
