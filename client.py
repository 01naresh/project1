# # client.py
# import socket
# import threading
# from crypto_utils import encrypt_message, decrypt_message

# HOST = '127.0.0.1'
# PORT = 65432

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))

# def receive():
#     while True:
#         try:
#             enc_msg = client.recv(1024).decode()
#             print(f"\nFriend: {decrypt_message(enc_msg)}")
#         except:
#             print("Connection closed.")
#             break

# def send():
#     while True:
#         msg = input("You: ")
#         enc_msg = encrypt_message(msg)
#         client.send(enc_msg.encode())

# threading.Thread(target=receive).start()
# threading.Thread(target=send).start()
# client.py (with Tkinter GUI)
# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from crypto_utils import encrypt_message, decrypt_message

# ---------- Network Setup ----------
HOST = '127.0.0.1'
PORT = 65432
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Connection Error: {e}")
    exit(1)

# ---------- GUI Setup ----------
class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Secure Chat App")

        # Ask for username first
        self.username = simpledialog.askstring("Username", "Enter your name:", parent=master)
        if not self.username:
            self.username = "User"

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_field = tk.Entry(master, font=("Arial", 12))
        self.entry_field.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=(0, 10))

        # Start background receiving thread
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message.strip() == "":
            return
        full_msg = f"{self.username}: {message}"
        try:
            enc_msg = encrypt_message(full_msg)
            client.send(enc_msg.encode())
            self.entry_field.delete(0, tk.END)
        except Exception as e:
            print(f"[Send Error] {e}")
            messagebox.showerror("Error", "Failed to send message.")

    def receive_messages(self):
        while self.running:
            try:
                enc_msg = client.recv(1024).decode()
                if enc_msg:
                    msg = decrypt_message(enc_msg)
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, msg + "\n")
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
            except Exception as e:
                print(f"[Receive Error] {e}")
                break

    def on_closing(self):
        self.running = False
        client.close()
        self.master.destroy()

# ---------- Launch GUI ----------
root = tk.Tk()
app = ChatApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
