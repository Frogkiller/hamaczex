import datetime
import tkinter as tk
from tkinter import ttk
import backend


class TransactionFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = self.create_table(["Date", "End Date", "Client", "Comment", "State", "Items No.", "Value", "Shipping"],
                                      self.selected)
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.hamm_tree = self.create_table(["Type", "Value", "Size", "Comment"], None)
        self.hamm_tree.grid(row=1, column=0)
        self.hamm_tree.bind("<Double-1>", self.focus_item)
        self.add_button = tk.Button(self, text="Add", command=self.add_item)
        self.add_button.grid(row=1, column=1)
        self.clear_item()

    def btn_jump(self):
        val = self.idval.get()
        if val is not '':
            it = self.model.trans.get(val)
            self.jump_to_cli(it.client)

    def jump_to_cli(self, idx):
        self.master.children['!clientframe'].tree.selection_set(idx)
        self.master.children['!clientframe'].simple_sel(idx)
        self.master.select(2)

    def focus_item(self, event):
        val = self.hamm_tree.identify_row(event.y)
        if val is not '':
            self.master.children['!itemsframe'].tree.selection_set(val)
            self.master.children['!itemsframe'].simple_sel(val)
            self.master.select(0)

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        for _, y in self.model.trans.items.items():
            self.tree.insert('', 'end', iid=y.idx)
            self.tree.set(y.idx, column=0, value=str(y.date))
            self.tree.set(y.idx, column=1, value=str(y.date_fin))
            self.tree.set(y.idx, column=2, value=self.model.print_cli(y.client))
            self.tree.set(y.idx, column=3, value=y.comment)
            self.tree.set(y.idx, column=4, value=y.state)
            self.tree.set(y.idx, column=5, value=len(y.items))
            self.tree.set(y.idx, column=6, value=y.value)
            self.tree.set(y.idx, column=7, value=y.shipping)
        self.ref_it()

    def ref_it(self):
        self.hamm_tree.delete(*self.hamm_tree.get_children())
        val = self.idval.get()
        if val is not '':
            for y in self.model.trans.get(val).items:
                element = self.model.items.get(y)
                self.hamm_tree.insert('', 'end', iid=element.idx)
                self.hamm_tree.set(element.idx, column=0, value=element.parttype)
                self.hamm_tree.set(element.idx, column=1, value=element.value)
                self.hamm_tree.set(element.idx, column=2, value=element.size)
                self.hamm_tree.set(element.idx, column=3, value=element.comment)

    def create_item(self):
        trans = self.model.add_trans()
        trans.comment = self.comment_field.get('1.0', 'end')
        trans.state = self.state.get()
        trans.shipping = self.shipping.get()
        trans.value = self.value.get()
        trans.date = self.date.get()
        trans.date_fin = self.enddate.get()
        self.clear_view()
        self.ref_it()
        self.ref()

    def add_item(self):
        val = self.idval.get()
        if val is not '':
            item = self.master.children['!itemsframe'].tree.focus()
            if item is not '':
                self.model.conn_item_trans(item, val)
                self.master.children['!itemsframe'].clear_item()
                self.ref_it()
                self.ref()
                self.tree.selection_set(val)
                self.master.children['!itemsframe'].ref()
                self.master.children['!itemsframe'].clear_view()

    def modify_item(self):
        val = self.idval.get()
        if val is not '':
            trans = self.model.trans.get(val)
            trans.comment = self.comment_field.get('1.0', 'end')
            trans.state = self.state.get()
            trans.shipping = self.shipping.get()
            trans.value = self.value.get()
            trans.date = self.date.get()
            trans.date_fin = self.enddate.get()
            self.model.update_trans(trans)
            self.master.children['!clientframe'].ref_tr()
            self.ref()

    def delete_item(self):
        val = self.idval.get()
        if val is not '':
            self.model.delete_trans(val)
            self.clear_view()
            self.ref()
            self.master.children['!clientframe'].ref_tr()
            self.master.children['!clientframe'].ref()
            self.master.children['!itemsframe'].ref()
            self.master.children['!itemsframe'].clear_view()

    def clear_item(self):
        self.clear_view()
        self.ref_it()
        self.ref()

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        self.state = tk.StringVar()
        label0 = tk.Label(frame, text="State")
        label0.grid(row=0, column=0)
        self.combo_state = ttk.Combobox(frame, textvariable=self.state, values=list(backend.states.keys()), state="readonly")
        self.combo_state.grid(row=0, column=1)
        self.combo_state.current(0)

        label = tk.Label(frame, text="Comment")
        label.grid(row=1, column=0)
        self.comment_field = tk.Text(frame, height=4, width=30)
        self.comment_field.grid(row=1, column=1)

        label = tk.Label(frame, text="Value")
        label.grid(row=2, column=0)
        self.val = tk.StringVar()
        self.value = tk.Entry(frame, textvariable=self.val)
        self.val.set("0")
        self.value.grid(row=2, column=1)

        self.shipping = tk.StringVar()
        label0 = tk.Label(frame, text="Shipping")
        label0.grid(row=3, column=0)
        self.combo_ship = ttk.Combobox(frame, textvariable=self.shipping, values=list(backend.shippings.keys()),
                                        state="readonly")
        self.combo_ship.grid(row=3, column=1)
        self.combo_ship.current(0)

        label2 = tk.Label(frame, text="Date")
        label2.grid(row=4, column=0)
        self.date = tk.Entry(frame)
        self.date.grid(row=4, column=1)

        label2 = tk.Label(frame, text="End date")
        label2.grid(row=5, column=0)
        self.enddate = tk.Entry(frame)
        self.enddate.grid(row=5, column=1)

        label3 = tk.Label(frame, text="Client Name")
        label3.grid(row=6, column=0)
        self.client = tk.Entry(frame, state="readonly")
        self.client.grid(row=6, column=1)

        label4 = tk.Label(frame, text="ID")
        label4.grid(row=7, column=0)
        self.idval = tk.Entry(frame, state="readonly")
        self.idval.grid(row=7, column=1)

        self.create_button = tk.Button(frame, text="Create", command=self.create_item)
        self.create_button.grid(row=8, column=0)
        self.modify_button = tk.Button(frame, text="Modify", command=self.modify_item)
        self.modify_button.grid(row=8, column=1)
        self.delete_button = tk.Button(frame, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=9, column=0)
        self.clear_button = tk.Button(frame, text="Clear", command=self.clear_item)
        self.clear_button.grid(row=9, column=1)
        self.jump_button = tk.Button(frame, text="Jump", command=self.btn_jump)
        self.jump_button.grid(row=10, column=0)
        return frame

    def selected(self, event):
        val = self.tree.identify_row(event.y)
        if val is not '':
            self.simple_sel(val)
        self.ref_it()

    def simple_sel(self, idx):
        sel = self.model.trans.get(idx)
        self.update_view(sel)
        self.ref_it()

    def clear_view(self):
        sel = type('', (), {})
        sel.comment = ''
        sel.state = list(backend.states.keys())[0]
        sel.shipping = list(backend.shippings.keys())[0]
        sel.value = '0'
        sel.idx = ''
        sel.date = str(datetime.date.today())
        sel.date_fin = ''
        sel.client = None
        self.update_view(sel)

    def update_view(self, sel):
        self.combo_state.current(backend.states[sel.state])
        self.combo_ship.current(backend.shippings[sel.shipping])
        self.comment_field.delete("1.0", tk.END)
        self.comment_field.insert("1.0", sel.comment)
        self.value.delete(0, tk.END)
        self.value.insert(0, sel.value)
        self.idval.config(state="normal")
        self.idval.delete(0, tk.END)
        self.idval.insert(0, str(sel.idx))
        self.idval.config(state="readonly")
        self.date.delete(0, tk.END)
        self.date.insert(0, str(sel.date))
        self.enddate.delete(0, tk.END)
        self.enddate.insert(0, str(sel.date_fin))
        self.client.delete(0, tk.END)
        self.client.insert(0, self.model.print_cli(sel.client))
        self.client.config(state="readonly")

    def create_table(self, list_columns, binder):
        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        tree["columns"] = list_columns
        for column in list_columns:
            tree.column(column, minwidth=0, width=90)
            tree.heading(column, text=column.capitalize())
        tree.bind("<Button-1>", binder)
        return tree
