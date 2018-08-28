import tkinter as tk
from tkinter import ttk
import datetime

from prices import *
import backend


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
        self.data.add_item('Hamak', szer + 'x' + dlug, self.size, self.value, None, datetime.date.today())


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
        self.data.add_item('Hamak', szer + 'x' + dlug, self.size, self.value, None, datetime.date.today())


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
        self.data.add_item('Hamak', szer + 'x' + dlug, self.size, self.value, None, datetime.date.today())


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
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.size, self.value, None, datetime.date.today())


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
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.size, self.value, None, datetime.date.today())


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
        self.data.add_item('Hamak', szer + 'x' + dlug + 'x' + wys, self.size, self.value, None, datetime.date.today())


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