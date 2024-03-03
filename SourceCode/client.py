import socket
import tkinter as tk

# Define the username variable to store the logged-in username
current_username = ""

def send_message(message):
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    display_response(response)

def display_response(response):
    response_text.config(state=tk.NORMAL)
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, response)
    response_text.config(state=tk.DISABLED)

def signup():
    username = username_entry.get()
    password = password_entry.get()
    send_message(f"signup {username} {password}")

def login():
    global current_username
    username = username_entry.get()
    password = password_entry.get()
    send_message(f"login {username} {password}")
    if "Successfully logged in" in response_text.get("1.0", tk.END):
        current_username = username

def deposit():
    amount = amount_entry.get()
    send_message(f"deposit {current_username} {amount}")

def withdraw():
    amount = amount_entry.get()
    send_message(f"withdraw {current_username} {amount}")

def broadcast(message):
    send_message(f"broadcast {current_username} {message}")

# Client configuration
HOST = '127.0.0.1'
PORT = 12348

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Create a Tkinter window
root = tk.Tk()
root.title("Banking Application")

# Labels and entries for username and password
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Buttons for signup and login
signup_button = tk.Button(root, text="Signup", width=12, command=signup)
signup_button.grid(row=2, column=0, padx=10, pady=5)

login_button = tk.Button(root, text="Login", width=12, command=login)
login_button.grid(row=2, column=1, padx=10, pady=5)

# Labels and entries for deposit and withdraw
amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=3, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, padx=10, pady=5)

deposit_button = tk.Button(root, text="Deposit", width=12, command=deposit)
deposit_button.grid(row=4, column=0, padx=10, pady=5)

withdraw_button = tk.Button(root, text="Withdraw", width=12, command=withdraw)
withdraw_button.grid(row=4, column=1, padx=10, pady=5)

# Text widget to display server responses
response_text = tk.Text(root, height=5, width=40)
response_text.grid(row=5, columnspan=2, padx=10, pady=5)
response_text.config(state=tk.DISABLED)

broadcast_entry = tk.Entry(root)
broadcast_entry.grid(row=6, column=0, padx=10, pady=5)

broadcast_button = tk.Button(root, text="Broadcast", width=12, command=lambda: broadcast(broadcast_entry.get()))
broadcast_button.grid(row=6, column=1, padx=10, pady=5)
# Start the Tkinter main loop
root.mainloop()
