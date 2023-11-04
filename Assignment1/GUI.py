import socket
import tkinter as tk 
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk 
import threading
from datetime import datetime
FORMAT = "utf8"
DISCONNECT = "x"

LARGE_FONT = ("verdana", 13,"bold")

class ClientGUI(tk.Tk):
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
        #self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')
        button_log = tk.Button(self,text="LOG IN", command=lambda: appController.showPage(HomePage)) 

        button_log.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        label_notice.pack()
        

        button_log.pack(pady=10)
    


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="HOME PAGE", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_title.pack(pady=10)


        publish_btn = tk.Button(self, text="publish", bg="steelblue1")
        fetch_btn = tk.Button(self, text="fetch", bg="steelblue1")
        publish_btn.configure(width=10)
        fetch_btn.configure(width=10)
        publish_btn.pack()
        fetch_btn.pack()


        #Publish frame
        self.publish_frame = tk.Frame(self, bg="bisque2")
        self.publish_lname_label = tk.Label(self.publish_frame, text="Chọn file:", bg="bisque2")
        self.publish_lname_entry = tk.Entry(self.publish_frame)
        self.publish_choose_btn = tk.Button(self.publish_frame, text="...", bg="white", command=self.publish_action)
        self.publish_fname_label = tk.Label(self.publish_frame, text="Tên file muốn lưu:", bg="bisque2")
        self.publish_fname_entry = tk.Entry(self.publish_frame)
        self.publish_submit_btn = tk.Button(self.publish_frame, text="submit", bg="steelblue2")

        self.publish_lname_label.grid(row=0, column=0)
        self.publish_lname_entry.grid(row=0,column=1)
        self.publish_choose_btn.grid(row=0,column=2, sticky="w")
        self.publish_fname_label.grid(row=1,column=0)
        self.publish_fname_entry.grid(row=1,column=1,columnspan=2, sticky="w")
        self.publish_submit_btn.grid(row=2,column=2)

        self.publish_frame.pack(padx=10, pady=10)


        #Fetch frame
        self.fetch_frame = tk.Frame(self, bg="bisque2")
        self.fetch_fname_label = tk.Label(self.publish_frame, text="Tên file:", bg="bisque2")
        self.fetch_fname_entry = tk.Entry(self.publish_frame)
        self.fetch_submit_publish_btn = tk.Button(self.publish_frame, text="submit", bg="steelblue2")

        self.fetch_fname_label.grid(row=0,column=0)
        self.fetch_fname_entry.grid(row=0,column=1)
        self.fetch_submit_publish_btn.grid(row=0,column=2)

        self.fetch_frame.pack(padx=10, pady=10)


        # self.entry_search = tk.Entry(self)
        # button_back = tk.Button(self, text="Go back",bg="#20639b",fg='#f5ea54')
        # button_list = tk.Button(self, text="List all", bg="#20639b",fg='#f5ea54', command=self.listAll)
        # self.label_notice = tk.Label(self, text="", bg="bisque2" )
        # button_search = tk.Button(self, text="Search for ID",bg="#20639b",fg='#f5ea54')

        # button_search.configure(width=10)
        # button_list.configure(width=10)
        # button_back.configure(width=10)
        # self.entry_search.pack()
        # self.label_notice.pack(pady=4)

        # button_search.pack(pady=2)
        # button_list.pack(pady=2) 
        # button_back.pack(pady=2)

        # self.frame_detail = tk.Frame(self, bg="steelblue1")
        
        # self.label_score = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)
        # self.label_time = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)
        # self.label_status = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)

        # self.tree_detail = ttk.Treeview(self.frame_detail)
        # self.tree_detail["column"] = ("Time", "Player", "Team", "Event")
        
        # self.tree_detail.column("#0", width=0, stretch=tk.NO)
        # self.tree_detail.column("Time", anchor='c', width=50)
        # self.tree_detail.column("Player", anchor='c', width=200)
        # self.tree_detail.column("Team", anchor='c', width=200)
        # self.tree_detail.column("Event", anchor='c', width=180)

        # self.tree_detail.heading("0", text="", anchor='c')
        # self.tree_detail.heading("Time", text="Time", anchor='c')
        # self.tree_detail.heading("Player", text="Player", anchor='c')
        # self.tree_detail.heading("Team", text="Team", anchor='c')
        # self.tree_detail.heading("Event", text="Event", anchor='c')

        # self.label_score.pack(pady=5)
        # self.label_time.pack(pady=5)
        # self.label_status.pack(pady=5)
        # self.tree_detail.pack()
        
        

        # self.frame_list = tk.Frame(self, bg="tomato")
        
        # self.tree = ttk.Treeview(self.frame_list)

        
        # self.tree["column"] = ("ID", "TeamA", "Score", "TeamB", "Status")
        
        
        # self.tree.column("#0", width=0, stretch=tk.NO)
        # self.tree.column("ID", anchor='c', width=30)
        # self.tree.column("TeamA", anchor='e', width=140)
        # self.tree.column("Score", anchor='c', width=40)
        # self.tree.column("TeamB", anchor='w', width=140)
        # self.tree.column("Status", anchor='c', width=80)

        # self.tree.heading("0", text="", anchor='c')
        # self.tree.heading("ID", text="ID", anchor='c')
        # self.tree.heading("TeamA", text="TeamA", anchor='e')
        # self.tree.heading("Score", text="Score", anchor='c')
        # self.tree.heading("TeamB", text="TeamB", anchor='w')
        # self.tree.heading("Status", text="Status", anchor='c')
        

        # self.tree.pack(pady=20)

    def publish_action(self):
        selected_file = filedialog.askopenfilename(title="File")
        if selected_file:
            local_path = selected_file
            print(local_path)
            self.publish_lname_entry.delete(0, tk.END)  # Xóa văn bản hiện có trong Entry
            self.publish_lname_entry.insert(0, local_path)


    # Xử lý publish lname fname
    def publish(self):
        pass
            

    def listAll(self):
        print(self.frame_detail)
        try:
            self.frame_detail.pack_forget()
            
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)

            self.tree.insert(parent="", index="end", iid= 1, 
                    values=("Helllo","Hi","Fuckyou"))
                

            self.frame_list.pack(pady=10)
        except:
            print('Error')
           # self.label_notice["text"] = "Error"

app = ClientGUI()
app.mainloop()