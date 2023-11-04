from utils import *

class Storage:

    def __init__(self):
        if os.path.exists("data.csv") and os.path.exists("user.csv"):
            self.FileList: pd.DataFrame = pd.read_csv("data.csv", index_col=0)
            self.UserList: pd.DataFrame = pd.read_csv("user.csv", index_col=0)
        else:
            self.FileList: pd.DataFrame = pd.DataFrame(columns=["filename", "IP", "time"])
            self.UserList: pd.DataFrame = pd.DataFrame(columns=["user", "password", "IP", "port"])
        return

    def addfile(self, filename: str, IP: str) -> bool:
        # self.FileList.update(filename, self.FileList.get(filename, list([IP])))
        return True

    def removefile(self, filename: str, IP: str) -> bool:
        return True
        pass

    def signup(self, data: dict[str, str], address: tuple) -> bool:
        usrname : str= data["username"]
        passwrd : str = data["password"]
        if self.UserList.get(usrname) is None:
            self.UserList.loc[len(self.UserList)]= {"user": usrname, "password": passwrd, "IP": address[0], "port" : address[1]} # type: ignore 
            self.write()
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
        self.write()
        return
    
    def write(self) -> None:
        t1 = threading.Thread(target=self.FileList.to_csv, args=(["data.csv"]), kwargs={})
        t2 = threading.Thread(target=self.UserList.to_csv, args=(["user.csv"]), kwargs={})
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        return
    
    def gethostnames(self, usrname) -> tuple[str, str]:
        user_row = self.UserList[self.UserList['user'] == usrname]
        if not user_row.empty:
            return str(user_row['IP'].iloc[0]), user_row['port'].iloc[0]
        return "", ""