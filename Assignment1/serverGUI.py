import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
FORMAT = "utf8"
BUTTON_WIDTH = 10
BUTTON_COLOR = "steelblue2"

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


app = ServerGUI()
app.mainloop()