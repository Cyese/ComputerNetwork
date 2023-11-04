from container import *
from protocol import Protocol


class Service(threading.Thread):
    def __init__(self, clientIP: str, sock: socket.socket) -> None:
        super().__init__(daemon=True, name=clientIP, target=self.chat)
        self.IP = clientIP
        self.socket = sock
        self.disconnect = False
        # self.chat()

    def chat(self):
        # To do: adding function based on the requirement </3 ### for now:
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
            # TODO: hadling incoming request and send back the response
            pass
        return


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
        self.server.bind((self.ip, self.port))
        self.server.listen()

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
                        data = connection.recv(1024)
                        data = json.loads(data.decode())
                        ip, port = data.get("ip"), data.get("port")
                        self.storage.updateIP(usr, ip, port)
                        new_worker = Service(ip, connection)
                        self.thread.append(new_worker)
                        new_worker.start()
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

    # def __del__(self):
    #     self.stop()

    def ping(self, hostname: str) -> dict:
        address = self.storage.gethostnames(hostname)
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
