#!/usr/bin/env python3

#  from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb

errmsg = 'POKER HAS NOT YET BEEN IMPLEMENTED!\nBILL GATES PWNS U!!!!!!'


class QuitButton(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        widget = tk.Button(self, text='Quit', command=self.quit)
        widget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def quit(self):
        if mb.askyesno('verify', 'do you really want to quit?'):
            quit()
        else:
            mb.showinfo('No', 'Quit has been cancelled')


class SplashScreen(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        labelfont = ('times', 20, 'bold')
        title = tk.Label(root, text='Pycard$ by Erik Lunna')
        title.config(bg='black', fg='yellow')
        title.config(font=labelfont)
        title.config(height=3, width=30)
        title.pack(side=tk.TOP)


if __name__ == "__main__":
    root = tk.Tk()
    SplashScreen(root).pack()
    QuitButton(root).pack()
    tk.Button(text='Poker', command=(lambda: mb.showerror('Pokerz', errmsg))).pack(fill=tk.X)

    buttons = tk.Frame()

    root.mainloop()
