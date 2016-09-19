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
        title = tk.Label(root, text='PonyUp Poker')
        title.config(bg='black', fg='yellow')
        title.config(font=labelfont)
        title.config(height=2, width=30)
        title.pack(side=tk.TOP)

        # Settings for the smaller text
        smconf = {
            'bg': 'black',
            'fg': 'yellow',
            'font': ('times', 12, 'bold'),
            'width': 30,
        }

        title2 = tk.Label(root, text='Card Room')
        title2.config(smconf)
        title2.pack(side=tk.TOP)

        credits = tk.Label(root, text='AoristTwilist Productions(2016)')
        credits.config(smconf)
        credits.pack(side=tk.TOP)

        author = tk.Label(root, text='Author: Erik Lunna')
        author.config(smconf)
        author.pack(side=tk.TOP)


if __name__ == "__main__":
    root = tk.Tk()
    SplashScreen(root).pack()
    QuitButton(root).pack()
    tk.Button(text='Poker', command=(lambda: mb.showerror('Pokerz', errmsg))).pack(fill=tk.X)

    buttons = tk.Frame()

    root.mainloop()
