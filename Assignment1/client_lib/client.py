from utils import *

class ClientUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("500x200")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(HomePage)
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("700x500")
        else:
            self.geometry("500x200")
        frame.tkraise()

        

class LoginPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN")
        label_user = tk.Label(self, text="username ")
        label_pswd = tk.Label(self, text="password ")
        label_notice = tk.Label(self, text="")
        self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')
        button_log = tk.Button(self,text="SIGN UP", command=self.signUp)
        button_log = tk.Button(self,text="LOG IN", command=self.logIn) 

        button_log.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        label_notice.pack()
        

        button_log.pack(pady=10)
    
    def logIn(self):
        pass

    def signUp(self):
        pass


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="HOME PAGE", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_title.pack(pady=10)


        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        #Publish frame
        self.publish_frame = ttk.Frame(notebook, width=70, height=15)
        notebook.add(self.publish_frame, text="publish")

        frame = tk.Frame(self.publish_frame)
        self.publish_lname_label = tk.Label(self.publish_frame, text="Chọn file:", bg="bisque2")
        self.publish_lname_entry = tk.Entry(frame)
        self.publish_lname_entry.configure(width=47)
        self.publish_choose_btn = tk.Button(frame, text="...", bg="white", command=self.publish_action)
        self.publish_fname_label = tk.Label(self.publish_frame, text="Tên file muốn lưu:", bg="bisque2")
        self.publish_fname_entry = tk.Entry(self.publish_frame)
        self.publish_fname_entry.configure(width=50)
        self.publish_submit_btn = tk.Button(self.publish_frame, text="Xác nhận", 
                                            bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                            command=self.publish)

        self.publish_lname_label.grid(row=0, column=0)
        self.publish_lname_entry.grid(row=0,column=0)
        self.publish_choose_btn.grid(row=0,column=1, sticky="w")
        frame.grid(row=0, column=1)
        self.publish_fname_label.grid(row=1,column=0)
        self.publish_fname_entry.grid(row=1,column=1,columnspan=2, sticky="w")
        self.publish_submit_btn.grid(row=2,column=1, sticky="e")



        #Fetch frame
        self.fetch_frame = ttk.Frame(notebook, width=70, height=15)
        notebook.add(self.fetch_frame, text="fetch",padding=[10,10])

        self.fetch_fname_label = tk.Label(self.fetch_frame, text="Tên file:", bg="bisque2")
        self.fetch_fname_entry = tk.Entry(self.fetch_frame)
        self.fetch_fname_entry.configure(width=50)
        self.fetch_hostname_label = tk.Label(self.fetch_frame, text="Hostname:", bg="bisque2")
        self.fetch_hostname_entry = tk.Entry(self.fetch_frame)
        self.fetch_hostname_entry.configure(width=50)
        self.fetch_submit_publish_btn = tk.Button(self.fetch_frame, text="Xác nhận", 
                                                  bg=BUTTON_COLOR, width=BUTTON_WIDTH, 
                                                  command=self.fetch)

        self.fetch_fname_label.grid(row=0,column=0)
        self.fetch_fname_entry.grid(row=0,column=1)
        self.fetch_hostname_label.grid(row=1,column=0)
        self.fetch_hostname_entry.grid(row=1,column=1)
        self.fetch_submit_publish_btn.grid(row=2,column=1, sticky="e")

        #Thao tác khác
        self.other_frame = ttk.Frame(notebook)
        notebook.add(self.other_frame, text="other", padding=[10,10])

        self.other_hostname_label = tk.Label(self.other_frame, text="Hostname:", bg="bisque2")
        self.other_hostname_entry = tk.Entry(self.other_frame)
        self.fetch_hostname_entry.configure(width=50)
        self.rename_btn = tk.Button(self.other_frame, text="Đổi tên", 
                                    bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                    command=self.rename)
        
        self.other_hostname_label.grid(row=0,column=0)
        self.other_hostname_entry.grid(row=0, column=1)
        self.rename_btn.grid(row=0,column=2)

        self.check_fname_label = tk.Label(self.other_frame, text="Tên file kiểm tra:")
        self.check_fname_entry = tk.Entry(self.other_frame)
        self.check_btn = tk.Button(self.other_frame, text="Kiểm tra", 
                                   bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                   command=self.check)
        
        self.check_fname_label.grid(row=1,column=0)
        self.check_fname_entry.grid(row=1, column=1)
        self.check_btn.grid(row=1,column=2)

        self.disconnect_btn = tk.Button(self.other_frame, text="Ngắt kết nối", 
                                        bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                        command=self.disconnect)
        self.disconnect_btn.grid(row=2,column=2, pady= 20)


    def publish_action(self):
        selected_file = filedialog.askopenfilename(title="File")
        if selected_file:
            local_path = selected_file
            print(local_path)
            self.publish_lname_entry.delete(0, tk.END)  # Xóa văn bản hiện có trong Entry
            self.publish_lname_entry.insert(0, local_path)


    # Xử lý publish lname fname
    def publish(self):
        local_path = self.publish_fname_entry.get()
        fname = self.publish_fname_label.get()
        pass
            
    def fetch(self):
        fname = self.fetch_fname_entry.get()
        hostname = self.fetch_hostname_entry.get()
        pass

    def rename(self):
        hostname = self.other_hostname_entry.get()
        pass

    def check(self):
        fname = self.check_fname_entry.get()
        pass

    def disconnect(self):
        pass


class ClientConnector:
    def __init__(self) :
        config = json.load(open("config.json", "r"))  
        self.Server = (config["ip"], config["port"])
        self.socket : socket.socket
        self.run()
        

    def connectToServer(self, username: str, password: str, auth: str = "signup") :#-> : # signup = True | signin = False
        # Load server connection port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Make a TCP connection request:
        self.socket.connect(self.Server)
        data = json.dumps({"auth" : auth, "username" : username, "password" : password})
        self.socket.sendto(data.encode(), self.Server)
        data = json.loads(self.socket.recv(1024).decode())
        if data["connection"] == "refuse": 
            return (False, data["type"])
        return (True, data["type"])

    def run(self):
        signup = inputMSG("Type 0 for login and 1 for signup : ")
        if signup == "1":
            auth = "signup"
        else: 
            auth = "signin"
        usr = inputMSG("Username : ")
        psswd =inputMSG("Password : ")
        printAlert(auth)
        connect, type = self.connectToServer(usr,psswd, auth=auth)
        printMSG(type)
        while True:
            msg : str= inputMSG("")
            data = json.dumps({"msg" : msg}).encode()
            self.socket.send(data)
            if msg == "disconnect":
                break

class ClientThreadHandler:
    pass
