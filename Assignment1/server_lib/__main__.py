from handler import *

server = Server()
input()
while True:
    val = int(input("[>]"))
    match val:
        case 1:
            server.shutdown()
            break
        case 2:
            server.ping("cyese")
        case 3:
            server.ping("tarim")
        