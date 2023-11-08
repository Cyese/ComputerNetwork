from utils import *

class Storage:
    def __init__(self):
        self.lock = threading.Lock()
        if  os.path.exists("user.csv"):
            self.UserList: pd.DataFrame = pd.read_csv("user.csv", index_col=0)
        else:
            self.UserList: pd.DataFrame = pd.DataFrame(columns=["user", "password", "IP", "port"])
        if os.path.exists("data.csv"):
            self.FileList: pd.DataFrame = pd.read_csv("data.csv")
        else:
            self.FileList: pd.DataFrame = pd.DataFrame(columns=["fname", "lname", "IP"])
        return

    def addfile(self, filename: str, localname: str, IP : str) -> bool:
        self.FileList.loc[len(self.FileList)] = {"fname" : filename, "lname": localname, "IP" :IP} # type: ignore
        self.write(1)
        return True


    def find(self, fname: str):
        result = self.FileList[self.FileList["fname"] == fname]
        result = result.drop(columns=["lname"]).to_dict(orient="records") # type: ignore
        pack = []
        for data in result:
            pack.append({"fname": data["fname"], "IP": data["IP"]})
        return pack

    def signup(self, data: dict[str, str], address: tuple) -> bool:
        usrname : str= data["username"]
        passwrd : str = data["password"]
        if self.UserList.get(usrname) is None:
            self.UserList.loc[len(self.UserList)]= {"user": usrname, "password": passwrd, "IP": address[0], "port" : address[1]} # type: ignore 
            self.write(0)
            printMSG("Signup success from " + str(address))
            return True
        return False

    def signin(self,data : dict, address) -> bool:
        usrname : str = data["username"]
        passwrd : str = data["password"]
        user_row = self.UserList[self.UserList['user'] == usrname]
        # print(user_row)
        if not user_row.empty:
            stored_password = str(user_row['password'].iloc[0] ) # Get the password from the DataFrame
            if stored_password == passwrd:
                printMSG("Login success from " + str(address))
                return True
        return False
        
    def updateIP(self, usr: str, ip, port) -> None:
        self.UserList.loc[self.UserList['user'] == usr, ['IP', 'port']] = [ip, port]
        self.write(0)
        return
    
    def write(self, switch: int ) -> None:
        with self.lock:
            if switch == 0:
                self.UserList.to_csv("user.csv")
            elif switch == 1: 
                self.FileList.to_csv("data.csv")
        return

    def gethostnames(self, info,  filter) -> tuple[str, str]:
        row = self.UserList[self.UserList[info] == filter].to_dict(orient="records")[0]
 
        return row.get('IP', ""), row.get('port', )
 
    def get(self, fname, **kwarg):
        host = kwarg.get("", None)
        lname : str
        addr : tuple
        if host is None:
            data = self.FileList.loc[self.FileList["fname"] == fname].to_dict(orient="records")[0]

            print(data)
            lname, IP = data["lname"], data["IP"]
            addr = self.gethostnames("IP", IP)
        else:
            data = self.FileList[self.FileList["fname"] == fname and self.FileList["IP"] == host].to_dict(orient="records")[0]
            lname, IP = data["lname"], data["IP"]
            addr = self.gethostnames("IP", IP)
        return (addr, lname)

    def getFileList(self, IP: str):
        filelist = self.FileList[self.FileList["IP"] == IP]["fname"].to_list()
        return filelist