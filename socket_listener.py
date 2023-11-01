import socket

def run():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to a public host and a port
    server_socket.bind(('localhost', 8000))
    while True:
        # receive data from the client
        data, address = server_socket.recvfrom(1024)
        print(f'Received data: {data.decode()}')
        print(f'From address: {address}')
        # send data to the client
        server_socket.sendto(data, address)
        if data.decode() == 'exit':
            break

# close the socket
# server_socket.close()

if __name__ == "__main__":
    run()