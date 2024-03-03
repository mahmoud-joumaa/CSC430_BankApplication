import socket
import threading

# Database to store user details (simplified for demonstration)
users = dict()
# Set to keep track of connected clients
clients = set()

def read_users(file, users): # Read users from database
    # Open file to read users & passwords
    users_db = open(file, "r")
    # Read all lines in the file
    user_lines = users_db.readlines()
    # Add every entry to the dictionary
    for line in user_lines:
        user = line.split(" ")
        username = user[0]
        password = user[1]
        balance = user[2]
        users[username] = {"password": password, "balance": float(balance)}
    # Close file
    users_db.close()

def add_user(users, username, password, amount): # Add a user to the current working users list
    # Add the user to the current dictionary
    users[username] = {"password": password, "balance": amount}

# Update the users db with the new data (i.e. permenantly store any updates that occurred)
def update_users_db(file, users):
    # Open file with write permissions
    users_db = open(file, "w")
    # Clear file
    users_db.write("")
    # Close file
    users_db.close()
    # Reopen file with append permissions
    users_db = open(file, "a")
    # Add every entry to the dictionary
    count = 0
    for username in users.keys():
        password = users[username]["password"]
        balance = users[username]["balance"]
        users_db.write(f"{username} {password} {balance}")
        count += 1
        if count != len(users):
            users_db.write("\n")
    # Close file
    users_db.close()

# Send a message to all connected clients
def broadcast(message, clients):
    for client in clients:
        try:
            client.send((message +"\n").encode())
        except:
            print(f"Failed to broadcast message: {message} to {client}")

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode().split()
            if not data:
                break

            # Sign Up
            if data[0] == "signup":
                # Handling client data received
                username = data[1]
                password = data[2]
                if username not in users:
                    client_socket.send("Signup successful!".encode())
                    # Add user to dictionary
                    add_user(users, username, password, 0)
                    # Broadcast to other clients
                    msg = f"{username} has created an account in our bank!"
                    broadcast(msg, clients)
                else:
                    client_socket.send("Username already exists!".encode())

            # Log in
            elif data[0] == "login":
                # Handling client data received
                username = data[1]
                password = data[2]
                if username in users and users[username]['password'] == password:
                    client_socket.send("Login successful!".encode())
                else:
                    client_socket.send("Invalid credentials!".encode())

            # Deposit
            elif data[0] == "deposit":
                # Handling client data received
                username = data[1]
                amount = float(data[2])
                if username in users:
                    users[username]['balance'] += amount
                    client_socket.send(f"Deposited {amount} successfully!".encode())
                else:
                    client_socket.send("User not found!".encode())

            # Withdraw
            elif data[0] == "withdraw":
                # Handling client data received
                username = data[1]
                amount = float(data[2])
                if username in users and users[username]['balance'] >= amount:
                    users[username]['balance'] -= amount
                    client_socket.send(f"Withdrawn {amount} successfully!".encode())
                else:
                    client_socket.send("Insufficient balance or user not found!".encode())
            
            elif data[0] == "broadcast":
                if len(data) >= 3:
                    username = data[1]
                    message = " ".join(data[2:])
                    if username in users:
                        msg = f"{username} says: {message}"
                        broadcast(msg, clients)
                    else:
                        client_socket.send("User not found!".encode())
                else:
                    client_socket.send("Invalid broadcast format!".encode())

            # Update the text file (database) if no exceptions occured
            update_users_db("users.txt", users)

        except Exception as e:
            print(f"Error: {e}")
            break

# Server configuration
HOST = '127.0.0.1'
PORT = 12348

# Initialize server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10) # listen to 10 clients simultaneously
print(f"Server listening on {HOST}:{PORT}")

# Initialize bank database
read_users("users.txt", users)

# Keep server on & accept incoming clients' requests
while True:
    client, address = server_socket.accept()
    clients.add(client)
    print(f"Accepted connection from {address}")
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
