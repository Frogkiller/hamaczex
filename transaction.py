import tkinter as tk
from tkinter import ttk


class TransactionFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = None
        self.create_table(["date", "client", "comment"])
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        rowid = 0
        for _, y in self.model.trans.items.items():
            self.tree.insert('', 'end', iid=rowid)
            self.tree.set(rowid, column=0, value=y.comment)
            self.tree.set(rowid, column=1, value=str(y.date))
            rowid += 1

    def create(self):
        trans = self.model.add_trans()
        trans.comment = self.comment_field.get()
        self.ref()

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        label = tk.Label(frame, text="Comment")
        label.grid(row=0, column=0)
        self.comment_field = tk.Entry(frame)
        self.comment_field.grid(row=0, column=1)
        label2 = tk.Label(frame, text="Date")
        label2.grid(row=1, column=0)
        self.date = tk.Entry(frame, state="readonly")
        self.date.grid(row=1, column=1)
        label3 = tk.Label(frame, text="Client Name")
        label3.grid(row=2, column=0)
        self.client = tk.Entry(frame, state="readonly")
        self.client.grid(row=2, column=1)
        label4 = tk.Label(frame, text="ID")
        label4.grid(row=3, column=0)
        self.idval = tk.Entry(frame, state="readonly")
        self.idval.grid(row=3, column=1)
        self.create_button = tk.Button(frame, text="Create", command=self.create)
        self.create_button.grid(row=3, column=0)
        return frame

    def selected(self, event):
        self.update_view(int(self.tree.identify_row(event.y)))

    def update_view(self, idx):
        selected = self.model.trans.get(idx)
        self.comment_field.delete(0, tk.END)
        self.comment_field.insert(0, selected.comment)
        self.idval.config(state="normal")
        self.idval.delete(0, tk.END)
        self.idval.insert(0, str(selected.iid))
        self.idval.config(state="readonly")
        self.date.config(state="normal")
        self.date.delete(0, tk.END)
        self.date.insert(0, str(selected.date))
        self.date.config(state="readonly")
        # self.client.delete(0, tk.END)
        # self.client.insert(0, selected.client)


    def create_table(self, list_columns):
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"] = list_columns
        for column in list_columns:
            self.tree.column(column)
            self.tree.heading(column, text=column.capitalize())
        self.tree.bind("<Double-1>", self.selected)
