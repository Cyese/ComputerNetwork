import json
import os
import socket
import threading
import tkinter as tk 
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk 

LARGE_FONT = ("verdana", 13,"bold")
FORMAT = "utf8"
BUTTON_WIDTH = 12
BUTTON_COLOR = "steelblue2"

def printMSG(msg: str) -> None: 
    print("[+] " + msg)
    return

def printFailed(msg:str) -> None:
    print("[-]" + msg)
    return

def printAlert(msg: str) -> None:
    print("[*] " + msg)
    return

def inputMSG(msg: str) -> str:
    return input(f"[+] {msg}")