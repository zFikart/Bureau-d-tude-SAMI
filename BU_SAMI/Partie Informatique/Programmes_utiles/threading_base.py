# Import Module
import tkinter as tk
import threading
from time import sleep
import random

# Create Object
root = tk.Tk()
root.geometry("400x400")
# global thread_word
# thread_word = None
a = "0"

# use threading
def threading_work():
    # global thread_word
    # if thread_work:
        # Call work function
        thread_word = threading.Thread(target = work)
        thread_word.start()
        # etat += 1

def update():
    label["text"] = a
    print(a)
    root.after(1000,update)

# work function
def work():
    global a
    # print("etat :", etat)
    while True:
        # if (etat%2 == 1):
        #     raise("STOPPPPPPP")
        x = random.randint(0,10)
        y = random.randint(0,10)
        theta = random.randint(0,180)
        a = f"{x} {y} {theta}"
        # print(a)
        # root.update_idletasks()
        # root.update()
        # print(x,y,theta)
        # root.after_idle(update)
        # root.after(1000, work)
        sleep(1)


def stop_thread():
    print("STOP")
    etat = 1

def exit_window():
    print("Exit")
    stop_thread()
    root.destroy()

# Create Button
label = tk.Label(root,text = a)
label.pack()
tk.Button(root, text = "Click Me", command = threading_work).pack()
tk.Button(root, text = "Stop thread (NE FONCTIONNE PAS)", command = stop_thread).pack()
tk.Button(root, text = "Exit window", command = exit_window).pack()

# Execute Tkinter
update()
root.mainloop()