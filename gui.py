#!/usr/bin/env python3

#  from tkinter import *
import tkinter as tk
import sys


def quit():
    print("Hey I gotta get going.")
    sys.exit()


def greeting():
    print('Hello stdout world!...')

root = tk.Tk()
labelfont = ('times', 20, 'bold')

title = tk.Label(root, text='Pycard$ by Erik Lunna')
title.config(bg='black', fg='yellow')
title.config(font=labelfont)
title.config(height=3, width=30)
title.pack(side=tk.TOP)

root.mainloop()
