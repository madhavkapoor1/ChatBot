# Group#: G4
# Student Names: Chao-Wu Chu (Kevin Chu), Madhav Kapoor 


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
    """
    def __init__(self, window: Tk):
        self.window = window
        self.window.title("Server")

        # GUI elements
        self.chat_area = Text(self.window, state="disabled", width=50, height=15)
        self.chat_area.pack()

        self.server_ready = False  # Flag to indicate server readiness
        self.display_message("Server initializing...")

        # Socket setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000)  # Only the server binds to this address/port
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(10) #Server to handle up to 10 pending connection requests before refusing additional ones

        self.clients = {}  # Dictionary to store client sockets and assigned names
        self.client_count = 0  # Counter for assigning unique names

        self.listen_thread = threading.Thread(target=self.accept_clients, daemon=True)

        self.server_ready = True  # Mark the server as ready

        self.listen_thread.start()

        self.display_message("Server started. Waiting for clients to connect...")

    def accept_clients(self):
        while True:
            if not self.server_ready:
                continue
            client_socket, client_address = self.server_socket.accept()
            # Increase client count when a new client connects
            self.client_count += 1
            client_name = f"Client {self.client_count}"
            self.clients[client_socket] = client_name

            client_socket.sendall(client_name.encode())

            self.display_message(f"{client_name} joined the chat from {client_address}.")

            # Each client gets a new thread
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        client_name = self.clients[client_socket]
        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                formatted_message = f"{client_name}: {message}"
                self.display_message(formatted_message)
                #Send the message to the clients
                self.broadcast_message(formatted_message, sender_socket=client_socket)
        except ConnectionError:
            self.display_message(f"{client_name} disconnected.")
        finally:
            self.clients.pop(client_socket, None)
            client_socket.close()

    def broadcast_message(self, message: str, sender_socket: socket.socket):
        #For messages shown in client window
        for client in list(self.clients.keys()):
            if client != sender_socket:
                try:
                    client.sendall(message.encode())
                except ConnectionError:
                    self.clients.pop(client, None)

    def display_message(self, message: str):
        #For messages shown in server window
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
