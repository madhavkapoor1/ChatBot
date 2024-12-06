# Group#: G4
# Student Names: Chao-Wu Chu (Kevin Chu), Madhav Kapoor 


from tkinter import *
import socket
import threading

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    def __init__(self, window: Tk):
        self.window = window

        # GUI elements
        self.chat_area = Text(self.window, state="disabled", width=50, height=15, wrap="word")
        self.chat_area.pack(padx=10, pady=10)

        # Define text alignment tags
        self.chat_area.tag_configure("left", justify="left")
        self.chat_area.tag_configure("right", justify="right")

        self.message_entry = Entry(self.window, width=40)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Socket setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000)  # Connect to the server
        self.connect_to_server()

        # Start listening for messages
        self.listen_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.listen_thread.start()

    def connect_to_server(self):
        while True:
            try:
                self.client_socket.connect(self.server_address)
                self.client_name = self.client_socket.recv(1024).decode()  # Receive assigned name
                self.window.title(f"{self.client_name} @ port {self.client_socket.getsockname()[1]}")
                self.display_message(f"Connected to the server as {self.client_name}.", sender="Server")
                break  # Exit the loop if connection is successful
            except ConnectionRefusedError:
                self.display_message("Unable to connect to the server. Retrying...", sender="System")

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.client_socket.sendall(message.encode())
            self.display_message(f"You: {message}", sender="You")
            #Removes the text from the entry field, allowing the user to type a new message without manually clearing the previous one
            self.message_entry.delete(0, END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                # Display the message with right alignment for other clients
                self.display_message(message, sender="Other")
            except ConnectionError:
                self.display_message("Connection to server lost.", sender="System")
                break

    def display_message(self, message: str, sender: str):
        self.chat_area.config(state="normal")
        if sender == "You":
            # Left-aligned message
            self.chat_area.insert(END, message + "\n", "left")
        elif sender == "Other":
            # Right-aligned message
            self.chat_area.insert(END, message + "\n", "right")
        else:
            # Centered server message
            self.chat_area.insert(END, message + "\n", "left")

        self.chat_area.config(state="disabled")
        self.chat_area.see(END)


def main():
    window = Tk()
    ChatClient(window)
    window.mainloop()


if __name__ == '__main__':
    main()
