from utils import *
from protocol import Protocol

class ClientThreadHandler(threading.Thread):
    def __init__(self, soc : socket.socket, usrname) -> None:
        super().__init__(daemon=True, target=self.run)
        self.socket = soc
        self.user = usrname
        self.terminate = False
        self.child : list[Transimition] = list()
        self.socket.listen()
        self.run() 
        self.keyList = []
    
    def run(self):
        while not self.terminate:
            try:
                # Listening form server: 
                if len(self.child) <= 5:
                    soc, _ =self.socket.accept()
                    data = json.loads(soc.recv(1024).decode())
                    match data["type"]:
                        case "CONNECT": 
                            res= self.connect(data)
                            if len(res) == 2:
                                reply = json.dumps(res[1]).encode()
                                soc.send(reply)
                                if not res[0]:
                                    soc.close()
                                else: 
                                    trasmitter = Transimition(soc)
                                    self.child.append(trasmitter)
                                    trasmitter.start()
                        case "PING":
                            reply = json.dumps(self.ping()).encode()
                            soc.send(reply)
                            soc.close()
                        case _:
                            
                            soc.close()
                else:
                    pass
            except:
                printAlert("Connection lost")     

    def stop(self):
        self.terminate = True
        for thread in self.child:
            thread.join()
        pass

    def ping(self):
        reply = Protocol.ping.copy()
        reply.update({"status" : f"{'avalable' if len(self.child) < 5 else 'busy'}"})
        return reply

    def connect(self, data: dict) -> tuple:
        match data["action"]:
            case "establish":
                self.keyList.append(data["key"])
                return ()
            case "request":
                if data["key"] in self.keyList:
                    self.keyList.remove(data["key"])
                    data = Protocol.connect_res.copy()
                    data.update({"connection" : "allowed"})
                    return (True, data)
                else:               
                    data = Protocol.connect_res.copy()
                    data.update({"connection" : "refused"})
                    return (False, data)
        return ()
        

class Transimition(threading.Thread):
    def __init__(self, soc : socket.socket):
        super().__init__(daemon=True, target=self.run)
        self.socket = soc
        self.terminate = False


    def run(self):
        pass


class Client:
    def __init__(self) :
        config = json.load(open("config.json", "r"))  
        self.Server = (config["ip"], config["port"])
        self.socket : socket.socket
        self.listener : ClientThreadHandler
        self.run()
        
    # def connectToServer(self, username: str, password: str, auth: str = "signup") :
    #     # Depricated
    #     # Load server connection port
        
    #     # Make a TCP connection request:

    #     data = json.dumps({"auth" : auth, "username" : username, "password" : password})
    #     self.socket.sendto(data.encode(), self.Server)
    #     data = json.loads(self.socket.recv(1024).decode())
    #     if data["connection"] == "refuse": 
    #         return (False, data["type"])
    #     return (True, data["type"])

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.Server)
            logged_in : bool = False
            while not logged_in:
                signup = inputMSG("Type 0 for login and 1 for signup : ")
                usr = inputMSG("Username : ")
                psswd =inputMSG("Password : ")
                if signup == "1":
                    auth = "signup"
                    logged_in = self.signup(usr, psswd)
                else: 
                    auth = "login"
                    logged_in = self.login(usr, psswd)
                printAlert(auth + f" {'success' if logged_in else 'failed'}")

            while True:
                msg : str= inputMSG("")
                data = json.dumps({"msg" : msg}).encode()
                self.socket.send(data)
                if msg == "disconnect":
                    break
        except:
            self.socket.close()

    def signup(self, usrname, psswd): 
        data = Protocol.signup.copy()
        data.update({"username" : usrname, "password" : psswd})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        if data["status"] == "success":
            ip, port = self.start_listerner(usrname)
            data = Protocol.identify.copy()
            data.update({"port" : port, "ip": ip})
            self.socket.send(json.dumps(data).encode())
            return True
        return False

    def login(self, usrname, psswd):
        data = Protocol.login.copy()
        data.update({"username" : usrname, "password" : psswd})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        if data["status"] == "success":
            ip, port = self.start_listerner(usrname)
            data = Protocol.identify.copy()
            data.update({"port" : port, "ip": ip})
            self.socket.send(json.dumps(data).encode())
            return True
        return False


    def start_listerner(self, usrname):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.bind(("localhost", 60000))
        except:
            soc.bind(("localhost", 60001))
        address = soc.getsockname()
        # self.listener = threading.Thread(target=ClientThreadHandler, args=(soc, usrname))
        # self.listener.daemon = True
        self.listener.start()
        return address
