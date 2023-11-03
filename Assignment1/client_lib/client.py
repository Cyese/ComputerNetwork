from utils import *

class ClientUI:
    pass

class ClientConnector:
    def __init__(self) :
        config = json.load(open("config.json", "r"))  
        self.Server = (config["ip"], config["port"])
        self.socket : socket.socket
        self.run()
        

    def connectToServer(self, username: str, password: str, auth: str = "signup") :#-> : # signup = True | signin = False
        # Load server connection port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Make a TCP connection request:
        self.socket.connect(self.Server)
        data = json.dumps({"auth" : auth, "username" : username, "password" : password})
        self.socket.sendto(data.encode(), self.Server)
        data = json.loads(self.socket.recv(1024).decode())
        if data["connection"] == "refuse": 
            return (False, data["type"])
        return (True, data["type"])

    def run(self):
        signup = inputMSG("Type 0 for login and 1 for signup : ")
        if signup == "1":
            auth = "signup"
        else: 
            auth = "signin"
        usr = inputMSG("Username : ")
        psswd =inputMSG("Password : ")
        printAlert(auth)
        connect, type = self.connectToServer(usr,psswd, auth=auth)
        printMSG(type)
        while True:
            msg : str= inputMSG("")
            data = json.dumps({"msg" : msg}).encode()
            self.socket.send(data)
            if msg == "disconnect":
                break

class ClientThreadHandler:
    pass
