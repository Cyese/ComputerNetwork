from utils import *

# class IP_User:
#     def __init__(self, ip, usern):
#         self.ip = ip
#         self.filename: dict[str, str] =dict() # filename: filepath
    
#     def add_file(self, filename, filepath) -> None:
#         self.filename[filename] = filepath  
    
#     def remove_file(self, filename) -> None:
#         del self.filename[filename]

# class User:
#     def __init__(self, usrname, password) -> None:
#         self.usrname = usrname
#         self.password= password 

class Storage:
    def __init__(self) :
        if os.path.exists("data.json") and os.path.exists("user.json"):
            self.FileList : dict[str, list[str]] = json.load(open("data.json", "r")) # filename: iplist 
            self.Username : dict[str, str] = json.load(open("user.json", "r")) # Username : Password
            # print(self.Username)
        else :
            self.FileList : dict[str, list[str]] = dict() # filename: IP list   
            self.Username : dict[str, str] = dict() # IP : Username
        return 

    def addfile(self, filename: str, IP: str) -> bool:
        # self.FileList.update(filename, self.FileList.get(filename, list([IP])))
        return True

    def removefile(self, filename: str, IP: str) -> bool:
        return True
        pass

    def signup(self, data: dict[str, str]) -> bool:
        usrname : str= data["username"]
        passwrd : str = data["password"]
        self.Username[usrname] = passwrd
        json.dump(self.Username, open("user.json", "w+"))
        return True

    def signin(self,data : dict) -> bool:
        usrname : str = data["username"]
        passwrd : str = data["password"]
        if self.Username.get(usrname, "") == passwrd:
            return True
        return False