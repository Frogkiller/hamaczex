import tkinter as tk
from tkinter import ttk
import math
from prices import *

def combox(tkan, mats):
    if tkan == mats[0]:
        res = PRICE_pol
    elif tkan == mats[1]:
        res = PRICE_min
    elif tkan == mats[2]:
        res = PRICE_pik
    return res


def ceiling_half(value):
    rv = round(value)
    if value - rv < 0:
        return rv
    else:
        return rv + 0.5


def mats_price(size, tkan, wata):
    price = size * PRICE_baw
    price += size * tkan
    if wata == 1:
        price += size * PRICE_wat
    price += size * value_waste
    return ceiling_half(price)


def kostka(szer, dl, wys, tkan, wata):
    size = (szer*dl + szer*wys + wys*dl)*2
    price = mats_price(size, tkan, wata)
    if size < 2600:
        price += size * value_kostka_small
    elif size <3700:
        price += size * value_kostka_med
    else:
        price += size * value_kostka_big
    price = ceiling_half(price)
    return price

def kostka_tr(szer, dl, wys, tkan, wata):
    size = szer*dl + szer*wys + wys*dl + math.sqrt(dl*dl+szer*szer)
    price = mats_price(size, tkan, wata)
    if size < 3700:
        price += size * value_kostka_tr_small
    else:
        price += size * value_kostka_tr_med
    price = ceiling_half(price)
    return price

def swinka(szer, dl, wys, tkan, wata):
    size = szer*dl + (szer*wys + wys*dl)*2
    price = mats_price(size, tkan, wata)
    if size < 3500:
        price += size * value_swinka_small
    else:
        price += size * value_swinka_big
    price = ceiling_half(price)
    return price


def hamak(szer, dl, tkan, wata):
    size = szer*dl
    price = mats_price(size, tkan, wata)
    if size < 1000:
        price += size * value_hamak_mini
    else:
        price += size * value_hamak
    price = ceiling_half(price)
    return price


def generator(tata, lista):
    enti = dict()
    for x in lista:
        row = tk.Frame(tata)
        lab = tk.Label(row, text=x)
        lab.pack(side=tk.LEFT)
        entr = tk.Entry(row)
        entr.pack(side=tk.RIGHT)
        row.pack(side=tk.TOP, expand = True, fill = tk.BOTH)
        enti[x] =  entr
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
    b = tk.Button(where, text="Licz", command=lambda: where.fun())
    b.pack(anchor=tk.S)
    where.wynik = tk.Entry(where)
    where.wynik.pack(anchor=tk.S)


class Ham(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def fun(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        calculations = hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        self.wynik.insert(0, calculations)

class Ham_tr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def fun(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        hamak_v = hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        calculations = ceiling_half(hamak_v/2)
        self.wynik.insert(0, calculations)

class Ham_2lvl(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ui_maker(self, ["Szerokość", "Długość"])

    def fun(self):
        self.wynik.delete(0, tk.END)
        wat = self.watolina.get()
        szer = self.itenz[self.entr[0]]
        dlug = self.itenz[self.entr[1]]
        val = self.val.get()
        matpric = combox(val, self.mats)
        hamak_v = hamak(int(szer.get()), int(dlug.get()), matpric, wat)
        calculations = 2*hamak_v+2
        self.wynik.insert(0, calculations)

class Kost(tk.Frame):
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
        calculations = kostka(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)

class Kost_tr(tk.Frame):
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
        calculations = kostka_tr(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)

class Swin(tk.Frame):
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
        calculations = swinka(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class app():
    def __init__(self, root):
        self.frame_ = None
        self.root = root

    def switchFrame(self, what):
        if self.frame_ is not None:
            self.frame_.destroy()
        self.frame_ = what(self.root)
        self.frame_.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("800x600")
    frame1 = tk.Frame(root)
    frame1.pack()
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)
    frame2 = tk.Frame(root)
    frame2.pack()
    AP = app(frame2)
    v = tk.IntVar()
    tk.Radiobutton(frame1, text="Hamak", variable=v, value=1, command=lambda: AP.switchFrame(Ham)).pack(side=tk.LEFT)
    tk.Radiobutton(frame1, text="Trójkątny hamak", variable=v, value=2, command=lambda: AP.switchFrame(Ham_tr)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek kostka", variable=v, value=3, command=lambda: AP.switchFrame(Kost)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek narożnik", variable=v, value=4, command=lambda: AP.switchFrame(Kost_tr)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Domek świnka", variable=v, value=5, command=lambda: AP.switchFrame(Swin)).pack(
        side=tk.LEFT)
    tk.Radiobutton(frame1, text="Paśnik/ham z dziurka/plaster 1 poziomowy", variable=v, value=6,
                   command = lambda: AP.switchFrame(Ham_2lvl)).pack(side=tk.LEFT)

    root.mainloop()