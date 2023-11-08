import json
import os
import socket
import threading
import pandas as pd

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
FORMAT = "utf8"
BUTTON_WIDTH = 10
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