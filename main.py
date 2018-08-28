import tkinter as tk
from tkinter import ttk
from calculators import *

from prices import *
import backend

import pdb


def do_menu(frame):
    menu_bar = tk.Menu(frame)
    filemenu = tk.Menu(menu_bar, tearoff=0)
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=frame.quit)
    menu_bar.add_cascade(label="Menu", menu=filemenu)

    return menu_bar


class CalculatorWin:
    def __init__(self, model, refresh):
        self.combo_values = ["Hamak", "Trójkątny hamak", "Domek kostka", "Domek narożnik", "Domek świnka",
                        "Paśnik/ham z dziurka/plaster 1 poziomowy"]
        self.data = model
        self.refresh = refresh

    def show(self):
        root = tk.Toplevel()
        root.pack_propagate(0)
        root.geometry("300x300")
        frame1 = tk.Frame(root)
        frame1.pack()
        separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        frame2 = tk.Frame(root)
        frame2.pack()
        AP = Calculator(frame2, self.data, self.refresh)
        val = tk.StringVar()
        combo = ttk.Combobox(frame1, textvariable=val, values=self.combo_values, state="readonly", width=100)
        combo.bind("<<ComboboxSelected>>", self.callback_creator(val, AP))
        combo.pack(side=tk.TOP)

    def callback_creator(self, box_value, app):
        def select_callback(event):
            if box_value.get() == self.combo_values[0]:
                app.switch_frame(Ham)
            elif box_value.get() == self.combo_values[1]:
                app.switch_frame(HamTriangle)
            elif box_value.get() == self.combo_values[2]:
                app.switch_frame(Cube)
            elif box_value.get() == self.combo_values[3]:
                app.switch_frame(CubeTriangle)
            elif box_value.get() == self.combo_values[4]:
                app.switch_frame(Pig)
            elif box_value.get() == self.combo_values[5]:
                app.switch_frame(Ham2lvl)

        return select_callback


class ItemsFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.items = data
        self.tree = None
        self.create_table(["size", "value"])
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.calc = CalculatorWin(self.items, self)

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        rowid = 1
        for _, y in self.items.items.items.items():
            self.tree.insert('', 'end', iid=rowid)
            self.tree.set(rowid, column=0, value=y.comment)
            self.tree.set(rowid, column=1, value=str(y.value))
            rowid += 1

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        self.add_button = tk.Button(frame, text="New", command=self.addoner).grid(row=0, column=0, columnspan=2)
        return frame

    def addoner(self):
        self.calc.show()

    def create_table(self, list_columns):
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"] = list_columns
        for column in list_columns:
            self.tree.column(column)
            self.tree.heading(column, text=column.capitalize())


class TabsView(tk.Frame):
    def __init__(self, master, datamodel):
        tk.Frame.__init__(self, master)
        self.root = master
        self.data = datamodel
        self.nb = ttk.Notebook(self.root, width=800, height=600)
        self.tab1 = ItemsFrame(self.nb, self.data)
        self.tab2 = tk.Frame(self.nb)
        self.tab3 = tk.Frame(self.nb)
        self.nb.add(self.tab1, text="Item")
        self.nb.add(self.tab2, text="Transaction")
        self.nb.add(self.tab3, text="Client")
        self.nb.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("800x600")
    root.config(menu=do_menu(root))
    data = backend.DataModel()
    frame1 = tk.Frame(root).pack()
    tabs = TabsView(frame1, data).pack()

    root.mainloop()
