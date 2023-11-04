from utils import *
from protocol import Protocol

# class Error(Exception):
#     UnkwownFilePath = "UnkwownFilePath"

class ClientThreadHandler(threading.Thread):
    def __init__(self, soc : socket.socket, usrname) -> None:
        super().__init__(daemon=True, target=self.run)
        self.socket = soc
        self.user = usrname
        self.terminate = False
        self.child : list[Transimition] = list()
        self.socket.listen() 
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
        self.running =True
        self.run()

    def run(self):
        # try:
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
            printAlert("Connection established")
            printAlert(auth + f" {'success' if logged_in else 'failed'}")

        while self.running:
            msg : str= inputMSG("")
            command = msg.split()
            try:
                match command[0]:
                    case "PUBLISH":
                        fname = command[1] if len(command) <=  2 else ""
                        lname = command[2] if len(command) <=  3 else ""
                        data = Client.publish(filename=fname, localname=lname)
                        self.socket.send(json.dumps(data).encode())
                    case "CHECK":
                        fname = command[1] if len(command) <=  2 else ""
                        count = command[2] if len(command) <=  3 else ""
                        data = Client.check(filename=fname, count=count)
                        self.socket.send(json.dumps(data).encode())
                        data = json.loads(self.socket.recv(1024).decode())
                        # TODO: move this data up to UI
                    case "DISCONNECT":
                        self.socket.send(json.dumps(Client.disconnect()).encode())
                        self.socket.close()
                        self.listener.stop()
                        self.running = False
                    case "FETCH":
                        pass
                    case "REMOVE":
                        pass
                    case "HOSTNAME":
                        pass
                    case "HELP":
                        pass
                    case "PASSWORD":
                        pass
                    case _:
                        printFailed("Invalid command. Use HELP for more information")
            except ValueError as e:
                printAlert(str(e))
            except FileNotFoundError as e:
                printAlert(str(e))
            except FileExistsError as e:
                printAlert(str(e))

    @staticmethod
    def publish(**kwargs):
        lname = kwargs.get("localname", "")
        fname = kwargs.get("filename", "")
        if fname == "" or lname == "":
            raise ValueError("filename and localname are required")
        elif not os.path.exists(lname):  
            raise FileNotFoundError(f"{lname} is not available")
        elif not os.path.isfile(lname):  
            raise FileExistsError(f"{lname} is not a file")
        data = Protocol.publish.copy()
        data.update({"filename" : fname, "localname" : lname})
        return data
    
    @staticmethod
    def check(**kwargs):
        fname = kwargs.get("filename", "")
        count = kwargs.get("count", "")
        if not count.isdecimal():
            raise ValueError("count must be an integer")
        if fname == "":
            raise ValueError("filename is required")
        data = Protocol.find.copy()
        data.update({"filename" : fname, "count" : count})
        return data

    @staticmethod
    def disconnect():
        data = Protocol.disconnect.copy()
        return data

    @staticmethod
    def fetch(**kwargs):
        # This gonna painfully long
        pass

    @staticmethod
    def remove(**kwargs):
        pass

    @staticmethod
    def modify(**kwargs):
        pass

    @staticmethod
    def help():
        # Print all available commands
        
        pass

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
        self.listener = ClientThreadHandler(soc, usrname)
        # self.listener.daemon = True
        self.listener.start()
        return address
