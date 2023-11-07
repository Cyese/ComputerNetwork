class Protocol:
    # Fromat from PROTOCOL.txt
    authenticate  = {"type": "AUTH", "action" : "authenticate", "status": None}
    ping = {"type" : "PING", "action": "ping"}
    connect = {"type": "CONNECT", "action": "connect", "hostname": None, "key":  None}
    find = {"type" : "FIND", "action": "reply", "hostlist": None}
    getFile = {"type" : "CONNECT", "action" : "send", "localname": None, "key": None}

