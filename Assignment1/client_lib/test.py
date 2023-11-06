from utils import os, socket, json, printAlert, printFailed
from protocol import Protocol


class Transimition():
    def __init__(self, role: int, fname: os.PathLike):
        # super().__init__(daemon=True, target=self.run, args=(role,))
        self.fname: os.PathLike = fname
        self.lname = os.path.join(os.getcwd(), fname)
        StrRole = ["send", "recv"]
        if role == 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(("localhost", 60000))
            self.fname = fname
            self.socket.listen()
        elif role == 1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("localhost", 60000))
        # self.terminate = False
        self.run(StrRole[role])

    def run(self, role: str):
        done = False
        # while not done:
        try:
            match role:
                case "send":
                    # print(f"Waiting for connection at {self}")
                    self.socket, addr = self.socket.accept()
                    # print(f"Connected to {addr}")
                    done = self.send()
                case "recv":
                    done = self.recv()
        except Exception as e:
            print(e)
            printFailed("Aborted")
            # if role == "send":
        finally: 
            self.socket.close()
            
            # pass
        # except Exception as e:
        #     printAlert(f"{str(e)}")
            # finally:
            #     self.socket.close()
            #     break

    def recv(self):
        data = json.loads(self.socket.recv(1024).decode())
        self.fname = data["filename"]
        length = data["length"]
        # if data.get("status", "OK") == "Error":
        #     raise ConnectionAbortedError("File is not available")
        recv_length = 0
        with open(os.path.join(os.getcwd(), self.fname), "wb") as file:
            # data = json.loads(self.socket.recv(1024).decode())
            # recved = data["data"]
            # recved_length = data["offset"] - recv_length
            # recv_length += recved_length
            # file.write(recved)
            # self.socket.send(json.dumps({"status": "OK"}).encode())
            self.socket.recv_into(file)
            # print(msg)
            # file.write(msg)
        if length != recv_length:
            return True
        return True

    def send(self):
        socc = self.socket
        filename = self.lname
        if not os.path.exists(filename) or not os.path.isfile(filename):
            reply = Protocol.post_rep.copy()
            reply.update({"status": "Error"})
            self.socket.send(json.dumps(reply).encode())
            raise FileNotFoundError(f"{filename} is not available")
        fname = os.path.split(filename)[-1]
        length = os.path.getsize(filename)
        reply = Protocol.post_rep.copy()
        reply.update({"status": "OK", "length": length, "file": fname})
        socc.send(json.dumps(reply).encode())
        with open(filename, "rb") as file:
            # offset = 0
            # while offset < length:
            #     response = json.loads(socc.recv(1024).decode())
            #     if response["status"] == "Error":
            #         raise ConnectionAbortedError("File is not available")
            #     data = file.read(1024)
            #     offset += len(data)
            #     reply = Protocol.post_transmit.copy()
            #     reply.update({"offset": offset, "data": data})
            #     socc.send(json.dumps(reply).encode())
            socc.sendfile(file)
        return True


role = int(input("[>] "))
meh = Transimition(role,"PROTOCOL.txt")
