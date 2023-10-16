import socket

# Create a port for listening 
port = 4000

# Create a socket object
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
listener.bind(('localhost', port))

# Listen for incoming connections
