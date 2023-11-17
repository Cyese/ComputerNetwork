from utils import *
from client import *

class ClientGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("P2P-client")
        self.geometry("500x200")
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

        self.showFrame(LoginPage)
        self.client = Client()
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("500x300")
        else:
            self.geometry("500x200")
        frame.tkraise()

        

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="LOG IN", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_user = tk.Label(self, text="username ",fg='#20639b',bg="bisque2",font='verdana 10 ')
        label_pswd = tk.Label(self, text="password ",fg='#20639b',bg="bisque2",font='verdana 10 ')

        self.label_notice = tk.Label(self,text="",bg="bisque2",fg="red")
        self.entry_user = tk.Entry(self,width=20)
        self.entry_pswd = tk.Entry(self,width=20)

        button_log = tk.Button(self,text="LOG IN", bg="steelblue1",command=lambda: self.logIn(controller)) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="SIGN UP",bg="steelblue1", command=lambda: self.signUp(controller)) 
        button_sign.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()

        button_log.pack()
        button_sign.pack()

    def logIn(self, controller):
        username = self.entry_user.get()
        password = self.entry_pswd.get()
        if username == "" or password == "":
            self.label_notice.config(text="Trường nhập đang trống")
            return
        else:
            self.label_notice.config(text="")

        logged_in = controller.client.run({
            "signup": "0",
            "usr": username,
            "psswd": password
        })
        if logged_in:
            controller.showFrame(HomePage)
        else: 
            self.label_notice.config(text="Đăng nhập thất bại")

    def signUp(self, controller):
        username = self.entry_user.get()
        password = self.entry_pswd.get()
        if username == "" or password == "":
            self.label_notice.config(text="Trường nhập đang trống")
            return
        else:
            self.label_notice.config(text="")

        success = controller.client.run({
            "signup": "1",
            "usr": username,
            "psswd": password
        })
        if success == "success":
            controller.showFrame(HomePage)
        elif success == "failed":
            self.label_notice.config(text="Tài khoản đã tồn tại")
        else:
            self.label_notice.config(text="Đăng ký thất bại")



class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        self.header_frame = tk.Frame(self, bg="bisque2", width=600)
        self.label_title = tk.Label(self.header_frame, text="HOME PAGE", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        self.label_title.pack(side=tk.LEFT, pady=10, padx=(60,160))
        self.disconnect_btn = tk.Button(self.header_frame, text="Ngắt kết nối", 
                                        bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                        command=lambda: self.disconnect(controller))
        
        self.disconnect_btn.pack(side=tk.RIGHT, pady=10, padx=10)
        self.header_frame.pack()

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        #Publish frame
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="publish", padding=[10,10]) #type: ignore
        self.publish_frame = ttk.Frame(tab1)

        frame = tk.Frame(self.publish_frame)
        self.publish_lname_label = tk.Label(self.publish_frame, text="Chọn file:")
        self.publish_lname_entry = tk.Entry(frame)
        self.publish_lname_entry.configure(width=47)
        self.publish_choose_btn = tk.Button(frame, text="...", bg="white", command=self.publish_action)
        self.publish_fname_label = tk.Label(self.publish_frame, text="Tên file muốn lưu:")
        self.publish_fname_entry = tk.Entry(self.publish_frame)
        self.publish_fname_entry.configure(width=50)
        self.publish_label_notice = tk.Label(self.publish_frame, text="",fg="red")
        self.publish_submit_btn = tk.Button(self.publish_frame, text="Xác nhận", 
                                            bg=BUTTON_COLOR, width=BUTTON_WIDTH,
                                            command=lambda: self.publish(controller))

        self.publish_lname_label.grid(row=0, column=0)
        self.publish_lname_entry.grid(row=0,column=0)
        self.publish_choose_btn.grid(row=0,column=1, sticky="w")
        frame.grid(row=0, column=1)
        self.publish_fname_label.grid(row=1,column=0)
        self.publish_fname_entry.grid(row=1,column=1,columnspan=2, sticky="w")
        self.publish_label_notice.grid(row=2,column=1)
        self.publish_submit_btn.grid(row=3,column=1, sticky="e")

        self.publish_frame.pack(pady=20)

        #Fetch frame
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="fetch",padding=[10,10]) # type: ignore
        self.fetch_frame = ttk.Frame(tab2, width=70, height=15)

        self.fetch_fname_label = tk.Label(self.fetch_frame, text="Tên file:")
        self.fetch_fname_entry = tk.Entry(self.fetch_frame)
        self.fetch_fname_entry.configure(width=50)
        self.fetch_hostname_label = tk.Label(self.fetch_frame, text="Hostname:")
        self.fetch_hostname_entry = tk.Entry(self.fetch_frame)
        self.fetch_hostname_entry.configure(width=50)
        self.fetch_label_notice = tk.Label(self.fetch_frame, text="",fg="red")
        self.fetch_btn = tk.Button(self.fetch_frame, text="Xác nhận", 
                                                  bg=BUTTON_COLOR, width=BUTTON_WIDTH, 
                                                  command=lambda: self.fetch(controller))

        self.fetch_fname_label.grid(row=0,column=0)
        self.fetch_fname_entry.grid(row=0,column=1)
        self.fetch_hostname_label.grid(row=1,column=0)
        self.fetch_hostname_entry.grid(row=1,column=1)
        self.fetch_label_notice.grid(row=2,column=1)
        self.fetch_btn.grid(row=3,column=1, sticky="e")

        self.fetch_frame.pack(anchor="center", pady = 20)


    def publish_action(self):
        selected_file = filedialog.askopenfilename(title="File")
        if selected_file:
            local_path = selected_file
            self.publish_lname_entry.delete(0, tk.END)  # Xóa văn bản hiện có trong Entry
            self.publish_lname_entry.insert(0, local_path)


    # Xử lý publish lname fname
    def publish(self, controller):
        local_path = self.publish_lname_entry.get()
        fname = self.publish_fname_entry.get()
        if local_path == "" or fname == "":
            self.publish_label_notice.config(text="Trường nhập đang trống")
            return
        else:
            self.publish_label_notice.config(text="")

        data = controller.client.publish(lname=local_path,fname=fname)
        if data == "Fname existed":
            show_message_box("Tên file bạn muốn lưu đã tồn tại")
        elif data == "Lname existed":
            show_message_box("Bạn đã publish file này")
        else:
            show_message_box("Publish thành công")



        #########################
        # XỬ LÝ BACKEND
        #########################
            
    def fetch(self, controller):
        fname = self.fetch_fname_entry.get()
        hostname = self.fetch_hostname_entry.get()
        if fname == "":
            self.fetch_label_notice.config(text="Trường nhập đang trống")
            return
        elif hostname == "":
            self.fetch_label_notice.config(text="")
            controller.client.fetch(fname=fname)
        else:
            self.fetch_label_notice.config(text="")
            controller.client.fetch(fname=fname, hostname=hostname)

    def disconnect(self, controller):
        controller.client.disconnect()

def show_message_box(msg):
    messagebox.showinfo("Thông báo", msg)

# app = ClientGUI()
# app.mainloop()