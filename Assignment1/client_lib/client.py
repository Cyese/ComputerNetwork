from utils import *
from protocol import Protocol


class ClientThreadHandler(threading.Thread):
    def __init__(self, usrname, ip) -> None:
        super().__init__(daemon=True, target=self.run)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket .bind((ip, 60000))
        except:
            self.socket .bind((ip, 60001))
        self.port = self.socket.getsockname()[1]
        self.user = usrname
        self.terminate = False
        self.child : list[Transimition] = list()
        self.socket.listen() 
    
    def run(self):
        while not self.terminate:
            try:
                soc, _ = self.socket.accept()
                data = json.loads(soc.recv(1024).decode())
                match data["type"]:
                    case "CONNECT": 
                        transmitter = Transimition(soc, "send")
                        transmitter.addfile(data["lname"])
                        self.child.append(transmitter)
                        transmitter.start()
                                
                    case "PING":
                        reply = json.dumps(self.ping()).encode()
                        soc.send(reply)
                        soc.close()
                    
                    case _:
                        soc.close()
                        printAlert("Invalid request")
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
        
    def makeConnection(self, address: tuple, key):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(address)
        data = Protocol.connect_req.copy()
        data.update({"lname" : key})
        soc.send(json.dumps(data).encode())
        transmitter = Transimition(soc, "recv")
        self.child.append(transmitter)
        transmitter.start()
        return None

class Transimition(threading.Thread):
    def __init__(self, soc : socket.socket, role : str):
        super().__init__(daemon=True, target=self.run)
        self.lname : os.PathLike
        # os.path.join(os.getcwd(), "test.py")
        self.socket = soc
        self.terminate = False
        self.role = role


    def run(self):
        try:
            match self.role:
                case "send":
                    self.send()
                case "recv":
                    self.recv() 
        except Exception as e:
            printAlert({str(e)})
            printFailed("Aborted")
        finally:
            self.socket.close()


    def recv(self):
        data = json.loads(self.socket.recv(1024).decode())
        self.fname = data["file"]
        length = data["length"]
        if data["status"] == "Error":
            raise ConnectionAbortedError("File is not available")
        with open(os.path.join(os.getcwd(),self.fname), "wb") as file:
            recved = self.socket.recv(1024)
            file.write(recved)
        return True


    def send(self):
        filename = self.lname
        if not os.path.exists(filename) or not os.path.isfile(filename):
            reply = Protocol.post_rep.copy()
            reply.update({"status" : "Error"})
            self.socket.send(json.dumps(reply).encode())
            raise FileNotFoundError(f"{filename} is not available")
        fname = os.path.split(filename)[-1]    
        length = os.path.getsize(filename)  
        reply = Protocol.post_rep.copy()
        reply.update({"status" : "OK", "length" : length, "file" : fname})
        self.socket.send(json.dumps(reply).encode())
        with open(filename, "rb") as file:
            offset = 0
            while offset < length:
                data = file.read(1024)
                offset += len(data)
                self.socket.send(data)
        return True

    def addfile(self, filename):
        self.lname = filename

class Client:
    def __init__(self) :
        config = json.load(open("config.json", "r"))  
        self.Server = (config["ip"], config["port"])
        self.socket : socket.socket
        self.listener : ClientThreadHandler
        self.running =True
        # self.run()

    def run(self, data: dict):
        # try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.Server)
        except:
            self.socket.connect((self.Server[0], self.Server[1]+2))
        signup = data.get("signup", "")

        usr = data.get("usr", "")
        psswd = data.get("psswd", "")
        if signup == "1":
            auth = "signup"
            logged_in = self.signup(usr, psswd)
        else: 
            auth = "login"
            logged_in = self.login(usr, psswd)
        printAlert("Connection established")
        printAlert(auth + f" {'success' if logged_in else 'failed'}")
        return logged_in

    # def operate(self, COMMAND: str, **kwargs):
    #     try:    
    #         match COMMAND:
    #             # case "PUBLISH":
    #             #     fname = ...
    #             #     lname = ...
    #             #     data = Client.publish(fname=fname, lname=lname)
    #             #     self.socket.send(json.dumps(data).encode())
    #             # case "CHECK":
    #             #     fname = command[1] if len(command) >=  2 else ""
    #             #     count = command[2] if len(command) ==  3 else 3
    #             #     data = Client.check(fname=fname, count=count)
    #             #     self.socket.send(json.dumps(data).encode())
    #             #     data = json.loads(self.socket.recv(1024).decode())
    #             #     # TODO: move this data up to UI
    #             #     hostlist : list[dict] = data["hostlist"]
    #             #     for value in hostlist:
    #             #         fname = value.get("fname", "")
    #             #         ip = value.get("IP", "")
    #             #         printAlert(f"file: {fname} : {ip}")
    #             # case "DISCONNECT":
    #             #     self.socket.send(json.dumps(Client.disconnect()).encode())
    #             #     self.socket.close()
    #             #     self.listener.stop()
    #             #     self.running = False
    #             # case "FETCH":
    #             #     fname = command[1] if len(command) >=  2 else ""
    #             #     hostname = command[2] if len(command) ==  3 else ""
    #             #     data = Client.fetch(filename=fname, hostname=hostname)
    #             #     self.socket.send(json.dumps(data).encode())
    #             #     reply = json.loads(self.socket.recv(1024).decode())
    #             #     address = reply["hostname"][1:-1].split(", ")
    #             #     address = (address[0][1:-1], int(address[1]))
    #             #     localname = reply["localname"]
    #             #     self.listener.makeConnection(address, localname)
    #             # case "REMOVE":
    #             #     fname = command[1] if len(command) >=  2 else ""
    #             #     data = Client.remove(filename=fname)
    #             #     self.socket.send(json.dumps(data).encode())
    #             # case "HOSTNAME":
    #             #     usr = command[1] if len(command) ==  2 else ""
    #             #     self.socket.send(json.dumps(Client.modify(username=usr)).encode())
    #             # case "PASSWORD":
    #             #     psswd = command[1] if len(command) ==  2 else ""
    #             #     self.socket.send(json.dumps(Client.modify(password=psswd)).encode())
    #             # case "HELP":
    #             #     Client.help()
    #             case _:
    #                 printFailed("Invalid command. Use HELP for more information")
    #     except ValueError as e:
    #         printAlert(str(e))
    #     except FileNotFoundError as e:
    #         printAlert(str(e))
    #     except FileExistsError as e:
    #         printAlert(str(e))
    #     return

    def publish(self, **kwargs):
        lname = kwargs.get("lname", "")
        fname = kwargs.get("fname", "")
        if fname == "" or lname == "":
            raise ValueError("filename and localname are required")
        elif not os.path.exists(lname):  
            raise FileNotFoundError(f"{lname} is not available")
        elif not os.path.isfile(lname):  
            raise FileExistsError(f"{lname} is not a file")
        data = Protocol.publish.copy()
        lname = os.path.abspath(lname)
        data.update({"fname" : fname, "lname" : lname})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        print(data)
        return data
    
    def check(self,**kwargs):
        fname = kwargs.get("fname", "")
        count = kwargs.get("count")
        if fname == "":
            raise ValueError("filename is required")
        data = Protocol.find.copy()
        data.update({"fname" : fname, "count" : count})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        # TODO: move this data up to UI
        hostlist : list[dict] = data["hostlist"]
        return hostlist

    def disconnect(self):
        data = Protocol.disconnect.copy()
        self.socket.send(json.dumps(data).encode())
        self.socket.close()
        self.listener.stop()
        self.running = False
        return

    def fetch(self,**kwargs):
        fname = kwargs.get("filename", "")
        hostname = kwargs.get("hostname", "")
        if fname == "":
            raise ValueError("filename is required")
        data = Protocol.fetch.copy()
        data.update({"filename" : fname, "hostname" : hostname})
        self.socket.send(json.dumps(data).encode())
        reply = json.loads(self.socket.recv(1024).decode())
        address = reply["hostname"][1:-1].split(", ")
        address = (address[0][1:-1], int(address[1]))
        localname = reply["localname"]
        self.listener.makeConnection(address, localname)
        return True
    
    def remove(self, **kwargs):
        fname = kwargs.get("filename", "")
        if fname == "":
            raise ValueError("filename is required")
        data = Protocol.remove.copy()
        data.update({"filename" : fname})
        self.socket.send(json.dumps(data).encode())
        return

    def modify(self, switch: int,**kwargs):
        match switch:
            case 0:
                data = Protocol.modify.copy()
                usrname = kwargs.get("username", "")
                data.update({"username" : usrname})
            case 1:
                data = Protocol.modify.copy()
                psswd = kwargs.get("password", "")
                data.update({"password" : psswd})
        self.socket.send(json.dumps(data).encode())
        return data

    @staticmethod
    def help():
        data = {"PULISH" : ["PUBLISH <filename> <localname>", "Publish a file to the server"],
                "FETCH" : ["FETCH <filename> <hostname>", "Fetch a file from the hostname, newest if <hostname> is omitted"],
                "REMOVE" : ["REMOVE <filename>", "Remove a file from the server"],
                "CHECK" : ["CHECK <filename> <count>", "Check if a file is available on the server"],
                "DISCONNECT" : ["DISCONNECT", "Disconnect from the server"],
                "HOSTNAME" : ["HOSTNAME <hostname>", "Change your username"],
                "PASSWORD" : ["PASSWORD <password>", "Change your password"],
                "HELP" : ["HELP", "Print this help message"]
                }
        return data
        

    def signup(self, usrname, psswd): 
        data = Protocol.signup.copy()
        data.update({"username" : usrname, "password" : psswd})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        if data["status"] == "success":
            port = self.start_listerner(usrname, data["IP"])
            data = Protocol.identify.copy()
            data.update({"port" : port})
            self.socket.send(json.dumps(data).encode())
            return "success"
        elif data["status"] == "failed":
            return "failed"
        return False

    def login(self, usrname, psswd):
        data = Protocol.login.copy()
        data.update({"username" : usrname, "password" : psswd})
        self.socket.send(json.dumps(data).encode())
        data = json.loads(self.socket.recv(1024).decode())
        if data["status"] == "success":
            port = self.start_listerner(usrname, data["IP"])
            data = Protocol.identify.copy()
            data.update({"port" : port})
            self.socket.send(json.dumps(data).encode())
            return True
        return False

    def start_listerner(self, usrname, IP):

        self.listener = ClientThreadHandler(usrname, IP)
        port = self.listener.port
        self.listener.start()
        return port
