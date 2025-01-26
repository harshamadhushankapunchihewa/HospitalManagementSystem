import threading
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class CameraAccess:
    def __init__(self):
        self.camera_access_window = None
        self.cap = None
        self.photo = None
        self.running = True
        self.camera_thread_handler = None

    def detect_face_shape(self, frame):
        # Your face detection code here
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

        return frame

    def open_camera_access(self):
        def camera_thread():
            nonlocal canvas  # Declare canvas as nonlocal to access it in this function
            # Open the camera using OpenCV
            self.cap = cv2.VideoCapture(0)

            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    frame = self.detect_face_shape(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame), master=self.camera_access_window)
                    canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Release the camera
            self.cap.release()

        def update_camera_feed():
            if self.running:
                nonlocal canvas  # Declare canvas as nonlocal to access it
                camera_thread_handler = threading.Thread(target=camera_thread)
                camera_thread_handler.daemon = True
                camera_thread_handler.start()

        self.camera_access_window = tk.Toplevel()  # Use Toplevel instead of Tk()
        self.camera_access_window.title("Camera Access Page")

        def close_camera_access():
            self.running = False  # Stop the camera thread

            if self.cap is not None:
                self.cap.release()  # Release the camera

            if self.camera_thread_handler is not None:
                self.camera_thread_handler.join()  # Wait for the camera thread to complete

            self.camera_access_window.destroy()  # Close the camera access window

        close_button = ttk.Button(self.camera_access_window, text="Close", command=close_camera_access)
        close_button.pack(padx=20, pady=20)

        canvas = tk.Canvas(self.camera_access_window, width=640, height=480)
        canvas.pack()

        update_camera_feed()
        self.camera_access_window.protocol("WM_DELETE_WINDOW", close_camera_access)  # Handle window close event

        self.camera_access_window.mainloop()


if __name__ == '__main__':
    camera_access = CameraAccess()
    camera_access.open_camera_access()

    # The main program will continue to run after the camera access window is closed
