import tkinter as tk
from tkinter import ttk

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


def ui_maker(where, what):
    where.entr = what
    where.mats = ["Polar", "Minky", "Pikowanie"]
    where.itenz = generator(where, where.entr)
    where.watolina = tk.IntVar()
    radio = tk.Checkbutton(where, text="Watolina", variable=where.watolina)
    radio.pack(side=tk.TOP)
    frame = tk.Frame(where)
    frame.pack(side=tk.TOP)
    lab = tk.Label(frame, text="Wykończenie")
    lab.pack(side=tk.LEFT)
    where.val = tk.StringVar()
    combo = ttk.Combobox(frame, textvariable=where.val, values=where.mats, state="readonly")
    combo.pack(side=tk.RIGHT)
    b = tk.Button(where, text="Licz", command=lambda: where.calculate())
    b.pack(anchor=tk.S)
    where.wynik = tk.Entry(where)
    where.wynik.pack(anchor=tk.S)


class Ham(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations = backend.hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class HamTriangle(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        hamak_v = backend.hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        calculations = backend.ceiling_half(hamak_v/2)
        self.wynik.insert(0, calculations)


class Ham2lvl(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        hamak_v = backend.hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        calculations = 2*hamak_v+2
        self.wynik.insert(0, calculations)


class Cube(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość", "Wysokość"])

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        wys = self.itenz[self.entr[2]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations = backend.kostka(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class CubeTriangle(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość", "Wysokość"])

    def fun(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        wys = self.itenz[self.entr[2]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations = backend.kostka_tr(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class Pig(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość", "Wysokość"])

    def calculate(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        wys = self.itenz[self.entr[2]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations = backend.swinka(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class Calculator:
    def __init__(self, rt):
        self.frame_ = None
        self.root = rt

    def switch_frame(self, what):
        if self.frame_ is not None:
            self.frame_.destroy()
        self.frame_ = what(self.root)
        self.frame_.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("800x300")
    frame1 = tk.Frame(root)
    frame1.pack()
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)
    frame2 = tk.Frame(root)
    frame2.pack()
    AP = Calculator(frame2)
    v = tk.IntVar()
    tk.Radiobutton(frame1, text="Hamak", variable=v, value=1, command=lambda: AP.switch_frame(Ham)).pack(side=tk.LEFT)
    tk.Radiobutton(frame1, text="Trójkątny hamak", variable=v, value=2,
                   command=lambda: AP.switch_frame(HamTriangle)).pack(side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek kostka", variable=v, value=3, command=lambda: AP.switch_frame(Cube)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek narożnik", variable=v, value=4,
                   command=lambda: AP.switch_frame(CubeTriangle)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek świnka", variable=v, value=5, command=lambda: AP.switch_frame(Pig)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Paśnik/ham z dziurka/plaster 1 poziomowy", variable=v, value=6,
                   command=lambda: AP.switch_frame(Ham2lvl)).pack(side=tk.LEFT)

    root.mainloop()
