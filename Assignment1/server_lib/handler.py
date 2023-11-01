from container import *

class Service: 
    def __init__(self, clientIP: str, clientPort: int, clientName : str) -> None:
        threading.Thread.__init__()
        self.IP = clientIP
        self.port = clientPort
        self.name = clientName

    
    def run():
        ### To do: adding function based on the requirement </3 ### for now:
        pass


class Controller:
    def __init__(self, config: dict = json.load(open("config.json", "r"))) -> None:
        self.maximiumClient : int = int(config["maxiumClient"])
        self.port : int = int(config["port"])
        self.protocol = config["Protocol"]
        self.ip : str = config["ip"]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ip, self.port)
        self.server.listen()
    
    def terminated(self): 
        data : dict = json.loads(open("config.json", "r"))
        data.update("maximiumClient", self.maximiumClient)
        data.update("port", self.port)
        data.update("ip", self.ip)
        json.dump(data, open("config.json", "w+"))

class ServerInteract:
    pass

class Server: 
    def __init__(self):
        printMSG("Initializing Server")
        self.storage : Storage = Storage()
        printMSG("Loaded data")
        self.controllerThread = threading.Thread(target=Controller, name="ServerController")
        # printMSG("")
        self.interactThread = threading.Thread(target=ServerInteract, name="ServerInteration")

