from storage import *
from protocol import Protocol


class Service(threading.Thread):
    def __init__(self, clientIP: str, sock: socket.socket, storage) -> None:
        super().__init__(target=self.chat)
        self.IP = clientIP
        self.socket = sock
        self.disconnect = False
        # self.chat()
        self.storage: Storage = storage
        self.start()

    def chat(self):
        pass

    def run(self):
        log = []
        while not self.disconnect:
        #     # TODO: hadling incoming request and send back the response
            msg = json.loads(self.socket.recv(1024).decode())
            if msg["type"] == "AUTH" and msg == "disconnect":
                self.stop()
                return
            match msg["type"]:
                case "PUBLISH":
                    fname = msg.get("fname")
                    lname = msg.get("lname")
                    IP = self.socket.getpeername()[0]
                    self.storage.addfile(fname, lname, IP)
                case "FETCH":
                    print(msg)
                    fname = msg.get("filename")
                    hostname = msg.get("hostname", "")
                    addr, lname = self.storage.get(fname,hostname=hostname)
                    key = "1234"
                    tosender = Protocol.getFile.copy()
                    tosender.update({"localname": lname, "key": key})
                    self.socket.sendto(json.dumps(tosender).encode(), addr) 
                    torecv = Protocol.connect.copy()
                    torecv.update({"key": key, "hostname" : str(addr)})
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
                    print(data)
                    if self.aunthenticate(data, address):
                        usr = data.get("username")
                        data = Protocol.authenticate.copy()
                        data["status"] = "success"
                        data = json.dumps(data)
                        connection.send(data.encode())
                        data = connection.recv(1024)
                        data = json.loads(data.decode())
                        ip, port = data.get("ip"), data.get("port")
                        self.storage.updateIP(usr, ip, port)
                        print(f"Connection open {type(connection)}")
                        new_worker = Service(ip, connection, self.storage)
                        self.thread.append(new_worker)
                    else:
                        data = json.dumps(
                            {"connection": "unauthorize", "type": "AUTH"})
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
        # print(type(data))
        _type = data.get("action")
        if _type == "signup":
            auth = self.storage.signup(data, address)
        else:
            auth = self.storage.signin(data, address)
        return auth

    def ping(self, hostname: str) -> dict:
        address = self.storage.gethostnames(hostname, "user")
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
        print(self.controller.ping(hostname))

    def discover(self, IP: str):
        pass

    def ban(self, IP: str):
        pass

    def remove(self, IP: str):
        pass

    def allow(self, IP: str):
        pass
    
    def shutdown(self):
        self.controller.stop()

class ServerInteract:
    def __init__(self) -> None:
        pass

    def ping(self, IP: str):
        pass

    def listHostname(self):
        pass

    # def
