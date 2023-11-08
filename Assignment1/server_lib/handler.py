from storage import *
from protocol import Protocol


class Service(threading.Thread):
    def __init__(self, clientIP: str, sock: socket.socket, storage) -> None:
        super().__init__(daemon=True, name="Service", target=self.run)
        self.IP = clientIP
        self.socket = sock
        self.disconnect = False
        # self.chat()
        self.storage: Storage = storage
        self.start()


    def run(self):
        log = []
        while not self.disconnect:
        #     # TODO: hadling incoming request and send back the response
            msg = json.loads(self.socket.recv(1024).decode())
            if msg["type"] == "AUTH" and msg["action"] == "disconnect":

                self.stop()
                return
            match msg["type"]:
                case "PUBLISH":
                    fname = msg.get("fname")
                    lname = msg.get("lname")
                    IP = self.socket.getpeername()[0]
                    print(self.storage.checkLname(fname, lname, IP))
                    match self.storage.checkLname(fname, lname, IP):

                        case "Fname existed":
                            rep_msg = "Fname existed"
                            self.socket.send(json.dumps(rep_msg).encode())
                        case "Lname existed":
                            rep_msg = "Lname existed"
                            self.socket.send(json.dumps(rep_msg).encode())
                        case "Pass":
                            rep_msg = "Pass"
                            self.storage.addfile(fname, lname, IP)
                            self.socket.send(json.dumps(rep_msg).encode())

                case "FETCH":
                    fname = msg.get("filename")
                    hostname = msg.get("hostname", "")
                    addr, lname = self.storage.get(fname,hostname=hostname)
                    torecv = Protocol.connect.copy()
                    torecv.update({"hostname" : str(addr),"localname": lname})
                    self.socket.send(json.dumps(torecv).encode())    
                case "FIND":
                    fname = msg.get("fname")
                    data = self.storage.find(fname)
                    rep = Protocol.find.copy()
                    rep.update({"hostlist" : data})
                    self.socket.send(json.dumps(rep).encode())
                
                case _:
                    pass  

    def stop(self):
        self.disconnect = True
        self.socket.close()

    def publish(self, msg: str):
        self.socket.send(msg.encode())

class Controller(threading.Thread):
    def __init__(self, storage: Storage) -> None:
        super().__init__(daemon=True, name="Controller", target=self.run)
        config: dict = json.load(open("config.json", "r"))
        self.maximiumClient: int = int(config["client"])
        self.port: int = int(config["port"])
        self.thread: list[Service] = list()
        self.ip: str = config["ip"]
        self.storage = storage
        self.online = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.ip, self.port))
        except:
            self.server.bind((self.ip, self.port+2))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.listen()
        

    def run(self):
        try:
            while self.online:
                while len(self.thread) <= self.maximiumClient:
                    # Aunthenticate upcoming request, assign a worker to that port
                    connection, address = self.server.accept()
                    recv = connection.recv(1024).decode()
                    data = json.loads(recv)
                    if self.aunthenticate(data, address):
                        usr = data.get("username")
                        data = Protocol.authenticate.copy()
                        data["status"] = "success"
                        ip = connection.getpeername()[0] 
                        data["IP"] = ip
                        data = json.dumps(data)
                        connection.send(data.encode())
                        data = connection.recv(1024)
                        data = json.loads(data.decode())
                        port =data.get("port")
                        self.storage.updateIP(usr, ip, port)
                        print(f"Connection open {type(connection)}")
                        new_worker = Service(ip, connection, self.storage)
                        self.thread.append(new_worker)
                    else:
                        data = Protocol.authenticate.copy()
                        data["status"] = "failed"
                        data = json.dumps(data)
                        connection.send(data.encode())
                        connection.close()
                    for thread in self.thread:
                        if not thread.is_alive():
                            self.thread.remove(thread)
        except KeyboardInterrupt:
            self.server.close()
        return

    def aunthenticate(self, data: dict, address: tuple) -> bool:
        auth: bool
        _type = data.get("action")
        if _type == "signup":
            auth = self.storage.signup(data, address)
        else:
            auth = self.storage.signin(data, address)
        return auth

    def ping(self, hostname: str) -> dict:
        address = self.storage.gethostnames("user", hostname)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = Protocol.ping.copy()
        data = json.dumps(data).encode()
        try:
            soc.connect(address)
            soc.send(data)
            data = json.loads(soc.recv(1024).decode())
            soc.close()
        except ConnectionRefusedError:
            data = {"status": "offline"}
        return data

    def stop(self):
        self.online = False
        self.server.close()
        for thread in self.thread:
            thread.join()

class Server:
    def __init__(self) -> None:
        # Init Database
        self.storage: Storage = Storage()
        # Init background
        self.controller = Controller(self.storage)
        self.controller.start()


    def ping(self, hostname: str):
        data = self.controller.ping(hostname)
        print(data)
        return data

    def discover(self, hostname: str):
        data = self.storage.getFileList(hostname)
        print(data)
        return data

    def ban(self, IP: str):
        pass

    def remove(self, IP: str):
        pass

    def allow(self, IP: str):
        pass
    
    def shutdown(self):
        self.controller.stop()
