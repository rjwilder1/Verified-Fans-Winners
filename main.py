from bs4 import BeautifulSoup
import requests
from datetime import date
import datetime
import time
import configparser
import threading
import ctypes
import os
import shutil

def Print(text): return print("[" + str(datetime.datetime.now().time().strftime("%H:%M:%S")) + "] " + str(text))
today = date.today().strftime("%Y-%m-%d")
UsedCodes = []
AmountWon = 0
Validated = False

def GetEmail(phonenum):
    with open('TMAccounts.txt', "r") as file:
        for line in file:
            values = line.strip().split(",")
            phone_number = values[4]
            if phone_number in phonenum:
                return values[1]#EMAIL
            
def GetPassword(phonenum):
    with open('TMAccounts.txt', "r") as file:
        for line in file:
            values = line.strip().split(",")
            phone_number = values[4]
            if phone_number in phonenum:
                return values[2]
            
def title(title):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleTitleW(title)

def thread_function():
    while True:
        time.sleep(1)
        title(f"Waiting for winning accounts " + str(datetime.datetime.now().strftime("%H:%M:%S")))

thread = threading.Thread(target=thread_function)
thread.start()

config= configparser.ConfigParser()
config.read(r'config.ini')
URL = config['CONFIG']['smsurl'].split(", ")
KEY = config['CONFIG']['key']

def ValidateKeys(key):
    global Validated
    content = requests.get("https://raw.githubusercontent.com/rjwilder1/TMV-Keys/main/README.md").text
    keys = content.splitlines()
    for line in keys:
        if line == key:
            Validated = True
            break
    if Validated:
        Print("Key is valid")
        Print('Waiting for page')
    else:
        input("Key in invalid, press enter to exit")
        quit()

ValidateKeys(KEY)

folder_name = "Winners"
try:
    shutil.rmtree(folder_name)
except Exception as i:
    time.sleep(0)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def GetCode():
    global URL
    global today
    global UsedCodes
    global AmountWon
    global CardsList
    for SMSURL in URL:
        response = requests.get(SMSURL)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find('table')
        if table:
            msgs = table.find_all('tr')
            if len(msgs) >= 1:
                for msg in msgs:
                    td_elements = msg.find_all('td')
                    if len(td_elements) >= 3:
                        PhoneNumber = td_elements[0].get_text()
                        txtmsg = td_elements[2].get_text()
                        if today in td_elements[3].get_text():
                            if r"****" in txtmsg:
                                code = txtmsg[-7:]
                                if code not in UsedCodes:
                                    UsedCodes.append(code)
                                    AmountWon += 1
                                    email = GetEmail(PhoneNumber)
                                    password = GetPassword(PhoneNumber)
                                    with open('Winners\\DYC.txt', "a") as file:
                                        file.write(f"{str(AmountWon)}cs,{email},{password}\n")
                                    with open('Winners\\TAC.txt', "a") as file:
                                        file.write(f"{email},{password}\n")
                                    with open('Winners\\Default.txt', "a") as file:
                                        file.write(f"[{str(AmountWon)}] Email: {email} | Code: {code}\n")
                                    Print(f"[{str(AmountWon)}] Email: {email} | Code: {code}")

Print("Waiting for winners")

while True:
    if Validated:
        GetCode()
        time.sleep(10)