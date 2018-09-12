import tkinter as tk
from tkinter import ttk


class ClientFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = self.create_table(["date", "client", "comment"], self.selected)
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.trans_tree = self.create_table(["size", "value", "comment"], None)
        self.trans_tree.grid(row=1, column=0)
        self.add_button = tk.Button(self, text="Add", command=self.add_trans)
        self.add_button.grid(row=1, column=1)
        self.ref()

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        for _, y in self.model.clients.items.items():
            self.tree.insert('', 'end', iid=y.idx)
            self.tree.set(y.idx, column=0, value=y.comment)
            self.tree.set(y.idx, column=1, value=str(y.date))
        self.ref_tr()

    def ref_tr(self):
        self.trans_tree.delete(*self.trans_tree.get_children())
        val = self.idval.get()
        if val is not '':
            for y in self.model.clients.get(val).transactions:
                element = self.model.trans.get(y)
                self.trans_tree.insert('', 'end', iid=element.idx)
                self.trans_tree.set(element.idx, column=0, value=element.comment)
                self.trans_tree.set(element.idx, column=1, value=str(element.date))

    def create_item(self):
        trans = self.model.add_client()
        trans.comment = self.comment_field.get()
        self.ref()

    def add_trans(self):
        val = self.idval.get()
        if val is not '':
            item = self.master.children['!transactionframe'].tree.focus()
            self.model.conn_trans_cli(item, val)
        self.ref_tr()

    def modify_item(self):
        val = self.idval.get()
        if val is not '':
            trans = self.model.trans.get(val)
            trans.comment = self.comment_field.get()
            self.model.update_trans(trans)
            self.ref()

    def delete_item(self):
        val = self.idval.get()
        if val is not '':
            self.model.delete_trans(val)
            self.ref()
            self.clear_view()

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
        self.create_button = tk.Button(frame, text="Create", command=self.create_item)
        self.create_button.grid(row=4, column=0)
        self.modify_button = tk.Button(frame, text="Modify", command=self.modify_item)
        self.modify_button.grid(row=4, column=1)
        self.delete_button = tk.Button(frame, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=5, column=0)
        return frame

    def selected(self, event):
        val = self.tree.identify_row(event.y)
        if val is not '':
            sel = self.model.clients.get(val)
            self.update_view(sel)
        self.ref_tr()

    def clear_view(self):
        sel = type('', (), {})
        sel.comment = ''
        sel.idx = ''
        sel.date = ''
        self.update_view(sel)

    def update_view(self, sel):
        self.comment_field.delete(0, tk.END)
        self.comment_field.insert(0, sel.comment)
        self.idval.config(state="normal")
        self.idval.delete(0, tk.END)
        self.idval.insert(0, str(sel.idx))
        self.idval.config(state="readonly")
        self.date.config(state="normal")
        self.date.delete(0, tk.END)
        self.date.insert(0, str(sel.date))
        self.date.config(state="readonly")
        # self.client.delete(0, tk.END)
        # self.client.insert(0, selected.client)

    def create_table(self, list_columns, binder):
        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        tree["columns"] = list_columns
        for column in list_columns:
            tree.column(column)
            tree.heading(column, text=column.capitalize())
        tree.bind("<Button-1>", binder)
        return tree
