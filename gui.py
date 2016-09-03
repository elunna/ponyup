#!/usr/bin/env python3

#  from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import sys

errmsg = 'POKER HAS NOT YET BEEN IMPLEMENTED!\nBILL GATES PWNS U!!!!!!'


def quit():
    print("Hey I gotta get going.")
    sys.exit()


def callback():
    if mb.askyesno('verify', 'do you really want to quit?'):
        quit()
        #  mb.showwarning('Yes', 'Quit not yet implemented')
    else:
        mb.showinfo('No', 'Quit has been cancelled')

root = tk.Tk()
labelfont = ('times', 20, 'bold')

title = tk.Label(root, text='Pycard$ by Erik Lunna')
title.config(bg='black', fg='yellow')
title.config(font=labelfont)
title.config(height=3, width=30)
title.pack(side=tk.TOP)

tk.Button(text='Quit', command=callback).pack(fill=tk.X)
tk.Button(text='Poker', command=(lambda: mb.showerror('Pokerz', errmsg))).pack(fill=tk.X)

buttons = tk.Frame()

root.mainloop()
