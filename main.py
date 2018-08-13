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
        calculations = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
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
        hamak_v = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
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
        hamak_v = backend.ham_calc(int(szer.get()), int(dlug.get()), matpric, wat)
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
        calculations = backend.cube_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
        self.wynik.insert(0, calculations)


class CubeTriangle(tk.Frame):
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
        calculations = backend.cuba_tri_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
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
        calculations = backend.pig_calc(int(szer.get()), int(dlug.get()), int(wys.get()), matpric, wat)
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


def callback_creator(box_value, full_values, app):
    def select_callback(event):
        if box_value.get() == full_values[0]:
            app.switch_frame(Ham)
        elif box_value.get() == full_values[1]:
            app.switch_frame(HamTriangle)
        elif box_value.get() == full_values[2]:
            app.switch_frame(Cube)
        elif box_value.get() == full_values[3]:
            app.switch_frame(CubeTriangle)
        elif box_value.get() == full_values[4]:
            app.switch_frame(Pig)
        elif box_value.get() == full_values[5]:
            app.switch_frame(Ham2lvl)
    return select_callback


def add_frame():
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("300x300")
    frame1 = tk.Frame(root)
    frame1.pack()
    separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)
    frame2 = tk.Frame(root)
    frame2.pack()
    AP = Calculator(frame2)
    v = tk.IntVar()
    val = tk.StringVar()
    combo_values = ["Hamak", "Trójkątny hamak", "Domek kostka", "Domek narożnik", "Domek świnka",
                    "Paśnik/ham z dziurka/plaster 1 poziomowy"]
    combo = ttk.Combobox(frame1, textvariable=val, values=combo_values, state="readonly", width=100)
    combo.bind("<<ComboboxSelected>>", callback_creator(val, combo_values, AP))
    combo.pack(side=tk.TOP)
    root.mainloop()


def do_menu(frame):
    menu_bar = tk.Menu(frame)
    filemenu = tk.Menu(menu_bar, tearoff=0)
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=frame.quit)
    menu_bar.add_cascade(label="Menu", menu=filemenu)

    return menu_bar


class TabsView(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.nb = ttk.Notebook(self.root, width=800, height=600)
        self.tab1 = self.do_item_frame(self.nb)
        self.tab2 = tk.Frame(self.nb)
        self.tab3 = tk.Frame(self.nb)
        self.nb.add(self.tab1, text="Item")
        self.nb.add(self.tab2, text="Transaction")
        self.nb.add(self.tab3, text="Client")
        self.nb.pack()

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        ent = tk.Entry(frame).pack()
        return frame


    def do_item_frame(self, nb):
        frame = tk.Frame(nb)
        tree = ttk.Treeview(frame).grid(row=0, column=0)
        view = self.do_custom_item(frame).grid(row=0, column=1)
        return frame


if __name__ == '__main__':
    root = tk.Tk()
    root.pack_propagate(0)
    root.geometry("800x600")
    root.config(menu=do_menu(root))
    frame1 = tk.Frame(root).pack()
    tabs = TabsView(frame1).pack()

    root.mainloop()
