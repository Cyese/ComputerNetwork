import json
import os
import socket
import threading

def printMSG(msg: str) -> None: 
    print("[+] " + msg)
    return

def printFailed(msg:str) -> None:
    print("[-]" + msg)
    return

def printAlert(msg: str) -> None:
    print("[*] " + msg)
    return