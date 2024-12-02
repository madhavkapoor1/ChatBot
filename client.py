# Group#:
# Student Names: Madhav Kapoor, Kevin Chu

#Rather than indent, can we make it such that it shows client 1, client2, etc to understand clearly if we have multiple clients

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    # To implement
    def __init__(self, window: Tk):
        self.window = window
        self.window.title(f"Chat Client - {current_process().name}")

        # GUI elements
        self.chat_area = Text(self.window, state="disabled", width=50, height=15)
        self.chat_area.pack()

        self.message_entry = Entry(self.window, width=40)
        self.message_entry.pack()
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        # Socket setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000)
        self.connect_to_server()

        # Start listening for messages
        self.listen_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.listen_thread.start()

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server_address)
            self.display_message("Connected to the server.")
        except ConnectionRefusedError:
            self.display_message("Unable to connect to the server. Please try again later.")

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.client_socket.sendall(message.encode())
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.display_message(message)
            except ConnectionError:
                self.display_message("Connection to server lost.")
                break

    def display_message(self, message: str):
        self.chat_area.config(state="normal")
        self.chat_area.insert(END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(END)

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()