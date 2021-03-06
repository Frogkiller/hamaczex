import datetime
import os
import shutil
import tkinter as tk
from tkinter import ttk
from items import ItemsFrame
from transaction import TransactionFrame
from client import ClientFrame

import backend


def do_menu(frame):
    menu_bar = tk.Menu(frame)
    filemenu = tk.Menu(menu_bar, tearoff=0)
    filemenu.add_command(label="Open", command=lambda: load_data(frame))
    filemenu.add_command(label="Save", command=lambda: save_data(frame))
    filemenu.add_command(label="Backup", command=lambda: backup())
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=frame.quit)
    menu_bar.add_cascade(label="Menu", menu=filemenu)

    return menu_bar


def backup():
    date = datetime.datetime.now()
    filename = "database.obj"
    dirname = "backup"
    try:
        os.mkdir(dirname)
    except OSError:
        pass
    shutil.copy2(filename, dirname + '/bk.' + date.strftime("%Y-%m-%dT%H-%M-%S") + '.obj')


def save_data(frame):
    frame.children['!tabsview'].data.dump()


def load_data(frame):
    frame.children['!tabsview'].data.load()
    frame.children['!tabsview'].ref()


class TabsView(tk.Frame):
    def __init__(self, master, datamodel):
        tk.Frame.__init__(self, master)
        self.root = master
        self.data = datamodel
        self.nb = ttk.Notebook(self.root, width=1024, height=768)
        self.tab1 = ItemsFrame(self.nb, self.data)
        self.tab2 = TransactionFrame(self.nb, self.data)
        self.tab3 = ClientFrame(self.nb, self.data)
        self.nb.add(self.tab1, text="Item")
        self.nb.add(self.tab2, text="Transaction")
        self.nb.add(self.tab3, text="Client")
        self.nb.pack()

    def ref(self):
        self.nb.destroy()
        self.nb = ttk.Notebook(self.root, width=1024, height=768)
        self.tab1 = ItemsFrame(self.nb, self.data)
        self.tab2 = TransactionFrame(self.nb, self.data)
        self.tab3 = ClientFrame(self.nb, self.data)
        self.nb.add(self.tab1, text="Item")
        self.nb.add(self.tab2, text="Transaction")
        self.nb.add(self.tab3, text="Client")
        self.nb.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("1024x768")
    root.config(menu=do_menu(root))
    data = backend.DataModel()
    frame1 = tk.Frame(root).pack()
    tabs = TabsView(frame1, data).pack()

    root.mainloop()
