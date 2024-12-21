# References:
# [1] Tu, W. (2021). Network Examples. Network Practicals - COMP2211, Durham University, delivered 4 October 2021
# [2] NeuralNine (2020). Simple TCP Chat Room. [online video] Available at: https://youtu.be/3UOyky9sEQY
# Both used as a basis for programming

import socket
import threading
import sys
import logging

# Initialise our logging file and format
logging.basicConfig(filename="server.log", level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# Define the required input arguments
port = int(sys.argv[1])
host = ""

# Ensure that we receive the right number of arguments in the correct form
if len(sys.argv) != 2:
    print("Please enter one argument in the form: python server.py [port]")
# Ensure our argument contain a valid port number
elif (int(sys.argv[1])) < 0 or (int(sys.argv[1]) > 65535):
    print("Please try again entering a valid port")
else:
    # Use SOCK_STREAM as our instant messenger uses TCP
    # Define our socket to connect our client to
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
    except socket.error:
        # Notifies us of our server error
        print("Server error - please try again entering a valid port.")
        # Logs this server error
        logging.warning("Server crashed")
        # Ends the current running script
        sys.exit(1)

    # Display the port on our log file
    logging.info("Server run on port:" + str(port))
    # Print a message on the server side, once the server is set up
    print("This server is ready to receive messages")

    # Looks out for a connection to our socket
    server_socket.listen()

    # Stores a new client and their username once entered
    clients = []
    clients_usernames = []

    # Sends a message to all the clients
    def message_to_all(message):
        for client in clients:
            client.send(message)

    # Processes inputs from the clients and outputs them
    def messages(client):
        while True:
            try:
                # When we receive a message from a client, send this to all users
                message = client.recv(1024)
                message_to_all(message)
                # Add this message, including who its from, to our log file
                logging.info(message.decode("ascii"))
            except:
                # For errors when receiving a message or sending a message to all:
                # Remove this client from the current list of clients using the server
                index = clients.index(client)
                clients.remove(client)
                # End the connection to this client
                client.close()
                # Find the username of our client
                clients_username = clients_usernames[index]
                # Notify all users that this user has left, even when there is a connection loss
                message_to_all(f"{clients_username} has left".encode("ascii"))
                # Add this to our log file
                logging.info(f"{clients_username} left")
                # Remove this user from our current list of users
                clients_usernames.remove(clients_username)
                break

    # Deals with all the clients we currently have
    def receive():
        while True:
            # When the server is running, return the client and their address
            client, address = server_socket.accept()
            # Prints where the connection has come from on the server side
            print(f"{str(address)} has connected to the server")

            # Allows us to receive a username (links to client file)
            client.send("user".encode("ascii"))
            # Adds the client's username to our list
            clients_username = client.recv(1024).decode("ascii")
            clients_usernames.append(clients_username)
            # Add the client to our client list
            clients.append(client)

            # Display a welcome message to the client
            client.send("Welcome to the server. Send a message".encode("ascii"))
            # Notify all users that this user has joined
            message_to_all(f"{clients_username} has joined".encode("ascii"))
            # Add this to our log file
            logging.info(f"{clients_username} joined")

            # Use threading to help us handle messages sent at the same time
            thread = threading.Thread(target=messages, args=(client,))
            thread.start()


    receive()

