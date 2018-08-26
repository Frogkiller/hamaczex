import tkinter as tk
from tkinter import ttk
import datetime

from prices import *
import backend

import pdb


def combox(tkan, mats):
    if tkan == mats[0]:
        res = PRICE_pol
    elif tkan == mats[1]:
        res = PRICE_min
    elif tkan == mats[2]:
        res = PRICE_pik
    return res


def generator(tata, lista):
    enti = dict()
    for x in lista:
        row = tk.Frame(tata)
        lab = tk.Label(row, text=x)
        lab.pack(side=tk.LEFT)
        entr = tk.Entry(row)
        entr.pack(side=tk.RIGHT)
        row.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        enti[x] = entr
    return enti


class BaseCalc(tk.Frame):
    def __init__(self, master, fields, data, ref):
        tk.Frame.__init__(self, master)
        self.fields = fields
        self.data = data
        self.ref = ref
        self.function = None
        self.add_func = None
        self.wynik = None
        self.value = 0
        self.mats, self.itenz, self.watolina, self.val, self.wynik, self.add_b = self.ui_maker()

    def ui_maker(self):
        mats = ["Polar", "Minky", "Pikowanie"]
        itenz = generator(self, self.fields)
        watolina = tk.IntVar()
        radio = tk.Checkbutton(self, text="Watolina", variable=watolina)
        radio.pack(side=tk.TOP)
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        lab = tk.Label(frame, text="Wykończenie")
        lab.pack(side=tk.LEFT)
        val = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=val, values=mats, state="readonly")
        combo.pack(side=tk.RIGHT)
        b = tk.Button(self, text="Licz", command=lambda: self.calculate())
        b.pack(anchor=tk.S)
        wynik = tk.Entry(self)
        wynik.pack(anchor=tk.S)
        add_b = tk.Button(self, text="Add", command=lambda: self.wrapped_add())
        add_b.pack(anchor=tk.S)
        return mats, itenz, watolina, val, wynik, add_b

    def set_func(self, funct):
        self.function = funct

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations, size = self.function(self.itenz, matpric, wat)
        self.wynik.insert(0, calculations)
        self.value = calculations
        self.size = size

    def set_add(self, add):
        self.add_func = add

    def wrapped_add(self):
        self.calculate()
        self.add_func()
        self.ref.ref()
        self.master.master.destroy()


class Ham(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        ret = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
        return ret

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug, self.value, self.size, None, datetime.date.today())


class HamTriangle(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        hamak_v, size = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
        ret = backend.ceiling_half(hamak_v/2)
        return ret, size

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug, self.value, self.size, None, datetime.date.today())


class Ham2lvl(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        hamak_v, size = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
        ret = 2*hamak_v+2
        return ret, size

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug, self.value, self.size, None, datetime.date.today())


class Cube(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość", "Wysokość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        wys = itenz[self.fields[2]]
        ret = backend.cube_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        return ret

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        wys = self.itenz[self.fields[2]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.value, self.size, None, datetime.date.today())


class CubeTriangle(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość", "Wysokość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        wys = itenz[self.fields[2]]
        ret = backend.cuba_tri_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        return ret

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        wys = self.itenz[self.fields[2]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.value, self.size, None, datetime.date.today())


class Pig(BaseCalc):
    def __init__(self, master, *rest):
        BaseCalc.__init__(self, master, ["Szerokość", "Długość", "Wysokość"], *rest)
        self.set_func(self.calc)
        self.set_add(self.add_f)

    def calc(self, itenz, matpric, wat):
        szer = itenz[self.fields[0]]
        dlug = itenz[self.fields[1]]
        wys = itenz[self.fields[2]]
        ret = backend.pig_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        return ret

    def add_f(self):
        szer = self.itenz[self.fields[0]].get()
        dlug = self.itenz[self.fields[1]].get()
        wys = self.itenz[self.fields[2]].get()
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.value, self.size, None, datetime.date.today())


class Calculator:
    def __init__(self, rt, data, refresher):
        self.frame_ = None
        self.root = rt
        self.data = data
        self.ref = refresher

    def switch_frame(self, what):
        if self.frame_ is not None:
            self.frame_.destroy()
        self.frame_ = what(self.root, self.data, self.ref)
        self.frame_.pack()


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
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.calc = CalculatorWin(self.items, self)

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        for _, y in self.items.items.items.items():
            self.tree.insert('', 'end', text=y.comment)
        pass

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        self.add_button = tk.Button(frame, text="New", command=self.addoner).grid(row=0, column=0, columnspan=2)
        return frame

    def addoner(self):
        self.calc.show()


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
