from container import *

class Service: 
    def __init__(self, clientIP: str, sock: socket.socket) -> None:
        # threading.Thread.__init__()
        self.IP = clientIP
        self.socket = sock
        self.run()

    def run(self):
        ### To do: adding function based on the requirement </3 ### for now:
        log = ""
        while True: 
            msg = json.loads(self.socket.recv(1024).decode())["msg"]
            if msg == "disconnect":
                with open(f"{threading.current_thread().name}.txt", "w") as file:
                    file.write(log)
                break
            log += msg + '\n'
        

class Handler:
    def __init__(self) -> None:
        config: dict = json.load(open("config.json", "r"))
        self.maximiumClient : int = int(config["client"])
        self.port : int = int(config["port"])
        self.thread : list[threading.Thread] = list()
        self.ip : str = config["ip"]
        self.online = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        self.run()

    def run(self):
        while self.online: 
            while len(self.thread) <= self.maximiumClient:
                # Aunthenticate upcoming request, assign a worker to that port
                connection, address = self.server.accept()
                data = json.loads(connection.recv(1024).decode())
                if self.aunthenticate(data, address):
                    data = json.dumps({"connection" : "allow" , "type" : "authorize"})
                    connection.send(data.encode())
                    new_worker = threading.Thread(target=Service, args=(address, connection))
                    new_worker.daemon = False
                    self.thread.append(new_worker)
                    new_worker.start()
                else:
                    data = json.dumps({"connection" : "refuse" , "type" : "unauthorize"})
                    connection.send(data.encode())
                    connection.close()
                for thread in self.thread:
                    if not thread.is_alive():
                        self.thread.remove(thread)
        return

    def aunthenticate(self, data : dict) -> bool:
        auth : bool
        meh = data["auth"]
        print(meh)
        if meh == "signup":
            auth = self.storage.signup(data)
        else:
            auth = self.storage.signin(data)
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
        self.handler : threading.Thread = threading.Thread(target=Handler)
        
              
    def __del__(self): 
        for thread in self.thread:
            thread.join()
        del self.storage
        del self.handler
        pass

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
    

    # def 
