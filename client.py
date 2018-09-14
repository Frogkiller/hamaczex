import tkinter as tk
from tkinter import ttk
import backend


class ClientFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = self.create_table(["Nick", "Name", "Surname", "Source", "Phone No.", "Address", "Trans No.",
                                       "Comment"], self.selected)
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.trans_tree = self.create_table(["Date", "Comment", "State", "Items No.", "Value",
                                             "Shipping"], None)
        self.trans_tree.bind("<Double-1>", self.focus_item)
        self.trans_tree.grid(row=1, column=0)
        self.add_button = tk.Button(self, text="Add", command=self.add_trans)
        self.add_button.grid(row=1, column=1)
        self.ref()

    def focus_item(self, event):
        val = self.trans_tree.identify_row(event.y)
        if val is not '':
            self.master.children['!transactionframe'].tree.selection_set(val)
            self.master.children['!transactionframe'].simple_sel(val)
            self.master.select(1)

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        for _, y in self.model.clients.items.items():
            self.tree.insert('', 'end', iid=y.idx)
            self.tree.set(y.idx, column=0, value=y.nick)
            self.tree.set(y.idx, column=1, value=y.name)
            self.tree.set(y.idx, column=2, value=y.surname)
            self.tree.set(y.idx, column=3, value=y.source)
            self.tree.set(y.idx, column=4, value=y.phone)
            self.tree.set(y.idx, column=5, value=y.address)
            self.tree.set(y.idx, column=6, value=len(y.transactions))
            self.tree.set(y.idx, column=7, value=y.comment)
        self.ref_tr()

    def ref_tr(self):
        self.trans_tree.delete(*self.trans_tree.get_children())
        val = self.idval.get()
        if val is not '':
            for y in self.model.clients.get(val).transactions:
                element = self.model.trans.get(y)
                self.trans_tree.insert('', 'end', iid=element.idx)
                self.trans_tree.set(element.idx, column=0, value=str(element.date))
                self.trans_tree.set(element.idx, column=1, value=str(element.date_fin))
                self.trans_tree.set(element.idx, column=2, value=element.comment)
                self.trans_tree.set(element.idx, column=3, value=element.state)
                self.trans_tree.set(element.idx, column=4, value=len(element.items))
                self.trans_tree.set(element.idx, column=5, value=element.value)
                self.trans_tree.set(element.idx, column=6, value=element.shipping)

    def create_item(self):
        cli = self.model.add_client()
        cli.comment = self.comment_field.get('1.0', 'end')
        cli.phone = self.phone_field.get()
        cli.nick = self.nick_field.get()
        cli.name = self.name_field.get()
        cli.surname = self.surname_field.get()
        cli.address = self.address_field.get('1.0', 'end')
        cli.source = self.source.get()
        self.clear_view()
        self.ref_tr()
        self.ref()

    def add_trans(self):
        val = self.idval.get()
        if val is not '':
            item = self.master.children['!transactionframe'].tree.focus()
            if item is not '':
                self.model.conn_trans_cli(item, val)
                self.master.children['!transactionframe'].clear_item()
                self.ref_tr()
                self.ref()
                self.tree.selection_set(val)

    def modify_item(self):
        val = self.idval.get()
        if val is not '':
            cli = self.model.clients.get(val)
            cli.comment = self.comment_field.get('1.0', 'end')
            cli.phone = self.phone_field.get()
            cli.nick = self.nick_field.get()
            cli.name = self.name_field.get()
            cli.surname = self.surname_field.get()
            cli.address = self.address_field.get('1.0', 'end')
            cli.source = self.source.get()
            self.model.update_cli(cli)
            self.ref()

    def delete_item(self):
        val = self.idval.get()
        if val is not '':
            self.model.delete_cli(val)
            self.clear_view()
            self.ref()

    def clear_item(self):
        self.clear_view()
        self.ref_tr()
        self.ref()

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)

        labe0l = tk.Label(frame, text="Nick")
        labe0l.grid(row=0, column=0)
        self.nick_field = tk.Entry(frame)
        self.nick_field.grid(row=0, column=1)

        labe02 = tk.Label(frame, text="Name")
        labe02.grid(row=1, column=0)
        self.name_field = tk.Entry(frame)
        self.name_field.grid(row=1, column=1)

        labe03 = tk.Label(frame, text="Surname")
        labe03.grid(row=2, column=0)
        self.surname_field = tk.Entry(frame)
        self.surname_field.grid(row=2, column=1)

        self.source = tk.StringVar()
        label04 = tk.Label(frame, text="Source")
        label04.grid(row=3, column=0)
        self.combo_source = ttk.Combobox(frame, textvariable=self.source, values=list(backend.sources.keys()),
                                       state="readonly")
        self.combo_source.grid(row=3, column=1)
        self.combo_source.current(0)

        labe05 = tk.Label(frame, text="Phone")
        labe05.grid(row=4, column=0)
        self.phone_field = tk.Entry(frame)
        self.phone_field.grid(row=4, column=1)

        label06 = tk.Label(frame, text="Address")
        label06.grid(row=5, column=0)
        self.address_field = tk.Text(frame, height=3, width=30)
        self.address_field.grid(row=5, column=1)

        label = tk.Label(frame, text="Comment")
        label.grid(row=6, column=0)
        self.comment_field = tk.Text(frame, height=4, width=30)
        self.comment_field.grid(row=6, column=1)

        label2 = tk.Label(frame, text="Date")
        label2.grid(row=7, column=0)
        self.date = tk.Entry(frame, state="readonly")
        self.date.grid(row=7, column=1)
        label4 = tk.Label(frame, text="ID")
        label4.grid(row=8, column=0)
        self.idval = tk.Entry(frame, state="readonly")
        self.idval.grid(row=8, column=1)
        self.create_button = tk.Button(frame, text="Create", command=self.create_item)
        self.create_button.grid(row=9, column=0)
        self.modify_button = tk.Button(frame, text="Modify", command=self.modify_item)
        self.modify_button.grid(row=9, column=1)
        self.delete_button = tk.Button(frame, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=10, column=0)
        self.clear_button = tk.Button(frame, text="Clear", command=self.clear_item)
        self.clear_button.grid(row=10, column=1)
        return frame

    def selected(self, event):
        val = self.tree.identify_row(event.y)
        if val is not '':
            self.simple_sel(val)
        self.ref_tr()

    def simple_sel(self, idx):
        sel = self.model.clients.get(idx)
        self.update_view(sel)
        self.ref_tr()

    def clear_view(self):
        sel = type('', (), {})
        sel.comment = ''
        sel.idx = ''
        sel.date = ''
        sel.phone = ''
        sel.nick = ''
        sel.name = ''
        sel.surname = ''
        sel.address = ''
        sel.source = list(backend.sources.keys())[0]
        self.update_view(sel)

    def update_view(self, sel):
        self.comment_field.delete("1.0", tk.END)
        self.comment_field.insert("1.0", sel.comment)
        self.address_field.delete("1.0", tk.END)
        self.address_field.insert("1.0", sel.address)
        self.combo_source.current(backend.sources[sel.source])

        self.nick_field.delete(0, tk.END)
        self.nick_field.insert(0, sel.nick)
        self.name_field.delete(0, tk.END)
        self.name_field.insert(0, sel.name)
        self.surname_field.delete(0, tk.END)
        self.surname_field.insert(0, sel.surname)
        self.phone_field.delete(0, tk.END)
        self.phone_field.insert(0, sel.phone)
        self.idval.config(state="normal")
        self.idval.delete(0, tk.END)
        self.idval.insert(0, str(sel.idx))
        self.idval.config(state="readonly")
        self.date.config(state="normal")
        self.date.delete(0, tk.END)
        self.date.insert(0, str(sel.date))
        self.date.config(state="readonly")

    def create_table(self, list_columns, binder):
        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        tree["columns"] = list_columns
        for column in list_columns:
            tree.column(column, minwidth=0, width=80)
            tree.heading(column, text=column.capitalize())
        tree.bind("<Button-1>", binder)
        return tree
