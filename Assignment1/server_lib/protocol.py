class Protocol:
    # Fromat from PROTOCOL.txt
    authenticate  = {"type": "AUTH", "action" : "authenticate", "status": None}
    ping = {"type" : "PING", "action": "ping", "hostname" : None}
    connect = {"type": "CONNECT", "action": "connect", "hostname": None, "port": None, "key":  None}
    find = {"type" : "FIND", "action": "reply", "hostlist": None}

