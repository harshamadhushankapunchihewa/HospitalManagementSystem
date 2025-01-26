import threading
import pyodbc
import socket
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Replace these with your actual database connection details
server = 'DESKTOP-Q6P1DJ6'  # Update with your SQL Server instance name
database = 'DATABASE8'  # Update with the name of your database

try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database)
    cursor = conn.cursor()
except pyodbc.Error as e:
    print("Error connecting to the database:", e)
    exit(1)

encryption_key = b'UnKwa0i3A0xzs_lhYd8dREinjTSuBzQ3OBiRs1yga2k='
cipher_suite = Fernet(encryption_key)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

def start_server():
    host = '192.168.1.2'
    port = 54752

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_ip = addr[0]

        while True:
            encrypted_data = client.recv(1024)
            if not encrypted_data:
                break

            # Decrypt the received data
            d_data = decrypt_data(encrypted_data)

            print(f"Received from {client_ip}: {d_data}")

            # Process the decrypted data here

            # Send a response back to the client
            response = "Data received and decrypted successfully"
            encrypted_response = encrypt_data(response)
            client.send(encrypted_response)

            # Return both client_ip and d_data
            return client_ip, d_data

def show_message(message):
    messagebox.showinfo("Access Status", message)

while True:
    client_ip, d_data = start_server()

    cursor.execute(
        "SELECT CurrentRoom FROM TimestampTbl WHERE RID = ? AND TIMESTAMP = (SELECT MAX(TIMESTAMP) FROM TimestampTbl WHERE RID = ?)",
        (d_data, d_data)
    )

    current_room = cursor.fetchone()[0]

    cursor.execute("SELECT TOP 1 RRF.NextRoom FROM RoomRFID AS RRF WHERE RRF.RoomID = ? AND RRF.RFIDS = ?", (current_room, client_ip))

    new_room = cursor.fetchone()[0]

    cursor.execute(
        "SELECT * FROM AllowedRoom WHERE RID = ? AND AllowedRooms = ?", (d_data, new_room, )
    )
    allowed_room = cursor.fetchall()

    if client_ip:
        def transfer_user():
            # Execute an INSERT INTO statement to insert the new row into the transaction table
            cursor.execute(
                "INSERT INTO Timestamptbl ( TimeIn, CurrentRoom, RID) VALUES (GETDATE(), ?, ?)",
                (new_room, d_data)
            )

            # Commit the changes to the database
            conn.commit()

        def allow_access():
            if d_data in [item[0] for item in allowed_room]:
                transfer_user()
                '''message = f"{d_data} allowed to move to {new_room}"
                show_message(message)'''
            else:
                message = f"{d_data} not allowed to move to {new_room}"
                show_message(message)

        allow_access()
