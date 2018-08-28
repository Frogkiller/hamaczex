from calculators import *


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