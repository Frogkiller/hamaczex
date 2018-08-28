import tkinter as tk
from tkinter import ttk


class TransactionFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = None
        self.create_table(["size", "value"])
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
    #
    # def ref(self):
    #     self.tree.delete(*self.tree.get_children())
    #     rowid = 1
    #     for _, y in self.items.items.items.items():
    #         self.tree.insert('', 'end', iid=rowid)
    #         self.tree.set(rowid, column=0, value=y.comment)
    #         self.tree.set(rowid, column=1, value=str(y.value))
    #         rowid += 1

    def create(self):
        print(self.comment_field.get())
        # self.model.add_trans()

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        label = tk.Label(frame, text="Comment")
        label.grid(row=0, column=0)
        self.comment_field = tk.Entry(frame)
        self.comment_field.grid(row=0, column=1)
        label2 = tk.Label(frame, text="Date")
        label2.grid(row=1, column=0)
        self.date = tk.Entry(frame, state="disabled")
        self.date.grid(row=1, column=1)
        label3 = tk.Label(frame, text="Client Name")
        label3.grid(row=2, column=0)
        self.client = tk.Entry(frame, state="disabled")
        self.client.grid(row=2, column=1)
        self.create_button = tk.Button(frame, text="Create", command=self.create)
        self.create_button.grid(row=3, column=0)
        return frame

    def create_table(self, list_columns):
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"] = list_columns
        for column in list_columns:
            self.tree.column(column)
            self.tree.heading(column, text=column.capitalize())