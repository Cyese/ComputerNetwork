import socket

import socket

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to a server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# send data
data = b'Hello, server!'
client_socket.send()

# close the socket
client_socket.close()
