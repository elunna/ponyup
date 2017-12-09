#!/usr/bin/env python3
"""
  " Module for running the poker game in a tkinter GUI
  " Might have to do: sudo apt-get install tk-dev python-tk"
  """

# import Tkinter
# from Tkinter import *
import Tkinter as tk
import tk.messagebox as mb

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
        title = tk.Label(self, text='PonyUp Poker')
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

        title2 = tk.Label(self, text='Card Room')
        title2.config(smconf)
        title2.pack(side=tk.TOP)

        company = tk.Label(self, text='AoristTwilist Productions(2016)')
        company.config(smconf)
        company.pack(side=tk.TOP)

        author = tk.Label(self, text='Author: Erik Lunna')
        author.config(smconf)
        author.pack(side=tk.TOP)


class MainMenu(tk.Frame):
    """ Main menu screen and lobby """
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        menu = tk.Menu()
        parent.config(menu=menu)

        gameMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=gameMenu)
        gameMenu.add_command(label="New Player", command=self.dont)
        gameMenu.add_command(label="Open Player", command=self.dont)
        gameMenu.add_command(label="Save Player", command=self.dont)
        gameMenu.add_command(label="Delete Player", command=self.dont)
        gameMenu.add_separator()
        gameMenu.add_command(label="Exit", command=self.dont)

        helpMenu = tk.Menu(menu)

        menu.add_cascade(label="Edit", menu=helpMenu)
        helpMenu.add_command(label="Help", command=self.dont)
        helpMenu.add_command(label="Credits", command=self.dont)
        gameMenu.add_separator()
        helpMenu.add_command(label="About", command=self.dont)

    def dont(self):
        print('Octavia cellos')


class Lobby(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()


def main():
    """ Main entry point """
    root = tk.Tk()
    SplashScreen(root).pack()
    QuitButton(root).pack()
    MainMenu(root).pack()

    tk.Button(text='Poker', command=(lambda: mb.showerror('Pokerz', errmsg))).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
