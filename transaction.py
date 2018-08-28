import tkinter as tk
from tkinter import ttk

class TransactionFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.items = data
        self.tree = None
        self.create_table(["size", "value"])
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)