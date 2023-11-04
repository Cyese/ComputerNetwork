from container import *
from protocol import Protocol
class Service: 
    def __init__(self, clientIP: str, sock: socket.socket) -> None:
        # threading.Thread.__init__()
        self.IP = clientIP
        self.socket = sock
        self.disconnect = False
        self.chat()

    def chat(self):
        ### To do: adding function based on the requirement </3 ### for now:
        log = ""
        while True: 
            msg = json.loads(self.socket.recv(1024).decode())["msg"]
            if msg == "disconnect":
                with open(f"{threading.current_thread().name}.txt", "w") as file:
                    file.write(log)
                break
            log += msg + '\n'
        
    def run(self):
        while not self.disconnect:
            ## TODO: hadling incoming request and send back the response
            pass
        return


class Controller:
    def __init__(self, storage : Storage) -> None:
        config: dict = json.load(open("config.json", "r"))
        self.maximiumClient : int = int(config["client"])
        
        self.port : int = int(config["port"])
        self.thread : list[threading.Thread] = list()
        self.ip : str = config["ip"]
        self.online = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        self.storage = storage
        self.run()

    def run(self):
        try:
            while self.online: 
                while len(self.thread) <= self.maximiumClient:
                    # Aunthenticate upcoming request, assign a worker to that port
                    connection, address = self.server.accept()
                    recv = connection.recv(1024).decode()
                    # print(recv)
                    data = json.loads(recv)
                    print(data)
                    if self.aunthenticate(data, address):
                        usr = data.get("username")
                        data = Protocol.authenticate.copy()
                        data["status"] = "success"
                        data = json.dumps(data)
                        connection.send(data.encode())
                        data, _RetAddress = connection.recvfrom(1024)
                        data = json.loads(data.decode())
                        print(data)
                        ip, port = data.get("ip"), data.get("port")
                        self.storage.updateIP(usr, ip, port)
                        new_worker = threading.Thread(target=Service, args=(address, connection))
                        new_worker.daemon = False
                        self.thread.append(new_worker)
                        new_worker.start()
                    else:
                        data = json.dumps({"connection" : "unauthorize" , "type" : "AUTH"})
                        connection.send(data.encode())
                        connection.close()
                    for thread in self.thread:
                        if not thread.is_alive():
                            self.thread.remove(thread)
        except KeyboardInterrupt:
            self.server.close()
        return

    def aunthenticate(self, data : dict, address: tuple ) -> bool:
        auth : bool
        # print(type(data))
        _type = data.get("action")
        if _type == "signup":
            auth = self.storage.signup(data, address)
        else:
            auth = self.storage.signin(data, address)
        return auth

    def __del__(self): 
        for thread in self.thread:
            thread.join()
            
    def dsth(self):
        pass
    
class Server:
    def __init__(self) -> None:
        # Init Database
        self.storage : Storage = Storage()
        # Init background 
        # self.handler : threading.Thread = threading.Thread(target=Controller)
        self.handler = Controller(self.storage)
              
    # def __del__(self): 
    #     # for thread in self.thread:
    #     #     thread.join()
    #     del self.storage
    #     del self.handler
    #     pass

    def ping(self, IP: str):
        pass

    def discover(self, IP: str):
        pass

    def ban(self, IP: str):
        pass

    def remove(self, IP: str):
        pass

    def allow(self, IP: str):
        pass
   


class ServerInteract:
    def __init__(self) -> None:
        pass
    

    def ping(self, IP: str):
        pass

    def listHostname(self):
        pass

    # def 
