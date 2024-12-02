# Group#:
# Student Names: Madhav Kapoor, Kevin Chu

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    def __init__(self, window: Tk):
        self.window = window
        self.window.title("Server")

        # GUI elements
        self.chat_area = Text(self.window, state="disabled", width=50, height=15)
        self.chat_area.pack()

        # Socket setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000) #running on 127.0.0.1:5000
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)

        self.clients = []
        self.listen_thread = threading.Thread(target=self.accept_clients, daemon=True)
        self.listen_thread.start()

        self.display_message("Server started. Waiting for clients to connect...")

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            self.display_message(f"New connection from {client_address}.")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.display_message(message)
                self.broadcast_message(message, client_socket)
        except ConnectionError:
            self.display_message("A client disconnected.")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_message(self, message: str, sender_socket: socket.socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode())
                except ConnectionError:
                    self.clients.remove(client)

    def display_message(self, message: str):
        self.chat_area.config(state="normal")
        self.chat_area.insert(END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(END)


def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()