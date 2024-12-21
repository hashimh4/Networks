# References:
# [1] Tu, W. (2021). Network Examples. Network Practicals - COMP2211, Durham University, delivered 4 October 2021
# [2] NeuralNine (2020). Simple TCP Chat Room. [online video] Available at: https://youtu.be/3UOyky9sEQY
# Both used as a basis for programming

import socket
import threading
import sys

# Define the required input arguments
client_username = sys.argv[1]
host = str(sys.argv[2])
port = int(sys.argv[3])

# Ensure that we receive the right number of arguments in the correct form
if len(sys.argv) != 4:
    print("Please enter three arguments in the form: python client.py [username] [hostname] [port]")
# Ensure a username has been set (code explicitly checks just in case)
elif host == "":
    print("Please enter a username")
else:
    # Create a socket and connect the client to their inputted host and port
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except socket.error:
        # Ensures we can connect to our server
        print("Please ensure the server is running or try again entering a valid hostname and port.")
        client.close()
        # Ends the current running script
        sys.exit(1)

    # Receives messages
    def receive():
        while True:
            try:
                # The client receives the messages
                message = client.recv(1024).decode("ascii")
                # Pass the username to the server
                if message == "user":
                    client.send(client_username.encode("ascii"))
                else:
                    # Print the messages we receive
                    print(message)
            except:
                # Returns a message if we disconnect from the server
                print("Server error")
                # Attempt to close the client connection in case of a crash
                client.close()
                break

    # Writes messages to the clients terminal
    def sender():
        while True:
            try:
                # Writes the messages to each user
                # Each line has the input prompt ">> "
                message = f"{client_username}: {input('>> ')}"
                client.send(message.encode("ascii"))
            except:
                # Attempt to close the client connection in case of a crash
                client.close()
                break

    # Define our threads to handle both these processes at the same time
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=sender)
    send_thread.start()

