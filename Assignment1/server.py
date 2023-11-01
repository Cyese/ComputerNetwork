import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Perform TCP handshake
        self.request.sendall(b"Welcome to the server!\n")

        # Handle incoming data
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            else:
                print(data)
            # Process data here

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# Create a port for listening 
port = 4000

# Create a socket object
listener = ThreadedTCPServer(('localhost', port), ThreadedTCPRequestHandler)

# Start the server
listener.serve_forever()

