from utils import *

class IP_User:
    def __init__(self, ip):
        self.ip = ip
        self.filename: dict[str, str] =dict() # filename: filepath
    
    def add_file(self, filename, filepath) -> None:
        self.filename[filename] = filepath  
    
    def remove_file(self, filename) -> None:
        del self.filename[filename]


class Storage:
    def __init__(self) :
        if os.path.exists("data.json") and os.path.exists("userMask.json"):
            self.FileList : dict[str, list[str]] = json.load(open("data.json", "rw")) # filename: iplist 
            self.Username :  dict[str, str] = json.load(open("userMask,json"), "rw") # IP : Username
        else :
            self.FileList : dict[str, list[str]] = dict() # filename: IP list   
            self.Username : dict[str, str] = dict() # IP : Username
        return 

    def addfile(self, filename: str, IP: str) -> bool:
        self.FileList.update(filename, self.FileList.get(filename, list([IP])))
    
    def removefile(self, filename: str, IP: str) -> bool:
        pass