import multiprocessing
import client
import server

def start_server(ready_event):
    server.main(ready_event)  # Pass an event to signal readiness that server is ready to be connected to

if __name__ == "__main__":
    # Create an event for synchronization
    server_ready = multiprocessing.Event()

    # Start the server process with the event
    server_process = multiprocessing.Process(target=start_server, args=(server_ready,))
    server_process.start()

    # Wait for the server to signal readiness
    print("Waiting for the server to start...")
    server_ready.wait()
    print("Server is ready. Starting clients...")

    # Start the client processes
    number_of_clients = 3  # Change this value for a different number of clients
    for count in range(1, number_of_clients + 1):
        client_process = multiprocessing.Process(target=client.main, name=f"Client{count}")
        client_process.start()
