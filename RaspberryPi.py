import socket
from cryptography.fernet import Fernet

# Receiver's UDP configuration
receiver_ip = '192.168.1.2'
receiver_port = 63829
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((receiver_ip, receiver_port))

# Encryption setup
key = Fernet.generate_key()
secret_key = key
cipher_suite = Fernet(secret_key)
print(secret_key)

# Server's TCP configuration
server_ip = '192.168.1.4'
server_port = 63889

while True:
    try:
        # Receive an unencrypted message via UDP
        data, sender_address = udp_socket.recvfrom(1024)
        message = data.decode()

        # Create a TCP socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))

        # Send the encrypted message to the server
        client_socket.send(encrypted_message)

        # Receive a response from the server (optional)
        encrypted_response = client_socket.recv(1024)
        response = cipher_suite.decrypt(encrypted_response).decode('utf-8')
        print(f"Received response from server: {response}")

    except Exception as e:
        print("Error")
