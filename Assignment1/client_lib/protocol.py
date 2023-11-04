class Protocol:
    login = {"type" : "AUTH", "action": "login", "username" : None, "password": None}
    signup = {"type" : "AUTH", "action": "signup", "username" : None, "password": None}
    disconnect = {"type" : "AUTH", "action": "disconnect"}
    publish = {"type" : "PUBLISH", "action": "publish", "localname" : None, "filename": None}
    fetch = {"type" : "FETCH", "action": "login", "username" : None, "password": None}
    connect_req = {"type" : "CONNECT", "action": "request", "key" : None}
    connect_res = {"type" : "CONNECT", "action": "response", "connection" : None}
    get = {"type" : "GET", "action" : "get", "filename" : None}
    post_rep = {"type" : "POST", "action" : "reply" , "file": "filename", "format" : None , "length" : None, "status" : None}
    post_transmit = {"type" : "POST", "action" : "transmit" , "offset": None, "data" : None }
    ping = {"type" : "PING", "action" : "reply" , "status" : None}
    find = {"type" : "FIND", "action" : "find" , "filename" : None, "count" : 3}
    identify = {"type" : "IDENTIFY", "action" : "identify" , "port" : None, "ip" : None}
    unknown = {"type" : "UNKNOWN", "action" : "disconnect" , "message" : None} 

