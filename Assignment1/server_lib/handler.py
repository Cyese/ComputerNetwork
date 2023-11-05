from container import *
from utils import *

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
    
class ServerGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("500x200")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame_input = tk.Frame(container)
        frame_input.pack(padx=10,pady=10)
        frame_btn = tk.Frame(container)
        frame_btn.pack(padx=10,pady=10)
        self.frame_list = tk.Frame(container)
        self.frame_list.pack(padx=10,pady=10)


        self.hostname_label = tk.Label(frame_input, text="Host name:")
        self.hostname_entry = tk.Entry(frame_input)
        self.ping_btn = tk.Button(frame_btn, text="Ping", 
                                   bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                   command=self.ping)
        self.discover_btn = tk.Button(frame_btn, text="Discover", 
                                   bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                   command=self.discover)
        
        self.hostname_label.pack(side="left")
        self.hostname_entry.pack(side="left")
        self.ping_btn.pack(side="right")
        self.discover_btn.pack(side="right")


        self.discovered_files = ttk.Treeview(self.frame_list)
        self.discovered_files["column"] = ("STT", "Filename")

        self.discovered_files.column("#0",width=0,stretch=0)
        self.discovered_files.column("STT",width=30)
        self.discovered_files.column("Filename",width=200) 

        self.discovered_files.heading("STT", text="STT")
        self.discovered_files.heading("Filename", text="Tên File")


    def ping(self):
        hostname = self.hostname_entry.get()

        # self.show_message_box()
        pass

    def discover(self):
        hostname = self.hostname_entry.get()

        self.discovered_files.pack()
        self.frame_list.pack()
        # try:
        #     self.discovered_files.pack_forget()
            
        #     x = self.discovered_files.get_children()
        #     for item in x:
        #         self.discovered_files.delete(item)

        #     self.discovered_files.insert(index="end", iid=1, 
        #             values=(1, "Alice.txt"))
            

        #     self.frame_list.pack(pady=10)
        # except:
        #     print("ERROR")
            
        pass

    def show_message_box(self):
        messagebox.showinfo("Thông báo", "Hostname vẫn đang kết nối")



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
