from serverGUI import *

server = ServerGUI()
server.mainloop()
input()
while True:
    val = int(input("[>]"))
    match val:
        case 1:
            server.shutdown()
            break
        case 2:
            server.discover("192.168.1.10")
        case 3:
            server.ping("tarim")
        