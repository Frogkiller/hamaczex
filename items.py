from calculators import *


class ItemsFrame(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(self, master)
        self.model = data
        self.tree = self.create_table(["Type", "Size", "Value", "Comment", "Transaction", "Date"], self.selected)
        self.tree.grid(row=0, column=0)
        self.view = self.do_custom_item(self)
        self.view.grid(row=0, column=1)
        self.calc = CalculatorWin(self.model, self)
        self.ref()

    def btn_jump(self):
        val = self.idval.get()
        if val is not '':
            it = self.model.items.get(val)
            self.jump_to_trans(it.trans)

    def jump_to_trans(self, idx):
        self.master.children['!transactionframe'].tree.selection_set(idx)
        self.master.children['!transactionframe'].simple_sel(idx)
        self.master.select(1)

    def print_trans(self, trans):
        if trans is not None:
            return 'YES'
        else:
            return 'NO'

    def ref(self):
        self.tree.delete(*self.tree.get_children())
        for _, y in self.model.items.items.items():
            self.tree.insert('', 'end', iid=y.idx)
            self.tree.set(y.idx, column=0, value=y.parttype)
            self.tree.set(y.idx, column=1, value=y.size)
            self.tree.set(y.idx, column=2, value=y.value)
            self.tree.set(y.idx, column=3, value=y.comment)
            self.tree.set(y.idx, column=4, value=self.print_trans(y.trans))
            self.tree.set(y.idx, column=5, value=y.date)

    def do_custom_item(self, parent):
        frame = tk.Frame(parent)
        self.add_button = tk.Button(frame, text="New", command=self.addoner).grid(row=0, column=0, columnspan=2)
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

        label = tk.Label(frame, text="Size")
        label.grid(row=3, column=0)
        self.siz = tk.StringVar()
        self.size = tk.Entry(frame, textvariable=self.siz)
        self.size.grid(row=3, column=1)

        label2 = tk.Label(frame, text="Date")
        label2.grid(row=4, column=0)
        self.date = tk.Entry(frame, state="readonly")
        self.date.grid(row=4, column=1)

        label2 = tk.Label(frame, text="Type")
        label2.grid(row=5, column=0)
        self.type = tk.Entry(frame, state="readonly")
        self.type.grid(row=5, column=1)

        label4 = tk.Label(frame, text="ID")
        label4.grid(row=6, column=0)
        self.idval = tk.Entry(frame, state="readonly")
        self.idval.grid(row=6, column=1)

        label4 = tk.Label(frame, text="Transaction")
        label4.grid(row=7, column=0)
        self.trans = tk.Entry(frame, state="readonly")
        self.trans.grid(row=7, column=1)

        self.modify_button = tk.Button(frame, text="Modify", command=self.modify_item)
        self.modify_button.grid(row=8, column=1)
        self.delete_button = tk.Button(frame, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=8, column=0)
        self.jump_button = tk.Button(frame, text="Jump", command=self.btn_jump)
        self.jump_button.grid(row=9, column=0)
        return frame

    def modify_item(self):
        val = self.idval.get()
        if val is not '':
            it = self.model.items.get(val)
            it.comment = self.comment_field.get('1.0', 'end')
            it.size = self.siz.get()
            it.value = self.val.get()
            self.model.update_item(it)
            self.ref()

    def delete_item(self):
        val = self.idval.get()
        if val is not '':
            self.model.delete_item(val)
            self.clear_view()
            self.ref()
        self.master.children['!transactionframe'].ref_it()
        self.master.children['!transactionframe'].ref()

    def clear_item(self):
        self.clear_view()
        self.ref()

    def addoner(self):
        self.calc.show()

    def create_table(self, list_columns, binder):
        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        tree["columns"] = list_columns
        for column in list_columns:
            tree.column(column, minwidth=0, width=100)
            tree.heading(column, text=column.capitalize())
        tree.bind("<Button-1>", binder)
        return tree

    def selected(self, event):
        val = self.tree.identify_row(event.y)
        if val is not '':
            self.simple_sel(val)

    def simple_sel(self, idx):
        sel = self.model.items.get(idx)
        self.update_view(sel)

    def clear_view(self):
        sel = type('', (), {})
        sel.comment = ''
        sel.parttype = ''
        sel.size = ''
        sel.value = '0'
        sel.idx = ''
        sel.date = ''
        sel.trans = None
        self.update_view(sel)

    def update_view(self, sel):
        self.comment_field.delete("1.0", tk.END)
        self.comment_field.insert("1.0", sel.comment)
        self.value.delete(0, tk.END)
        self.value.insert(0, sel.value)
        self.idval.config(state="normal")
        self.size.delete(0, tk.END)
        self.size.insert(0, sel.size)
        self.idval.config(state="normal")
        self.idval.delete(0, tk.END)
        self.idval.insert(0, str(sel.idx))
        self.idval.config(state="readonly")
        self.date.config(state="normal")
        self.date.delete(0, tk.END)
        self.date.insert(0, str(sel.date))
        self.date.config(state="readonly")
        self.trans.config(state="normal")
        self.trans.delete(0, tk.END)
        self.trans.insert(0, self.print_trans(sel.trans))
        self.trans.config(state="readonly")
        self.type.config(state="normal")
        self.type.delete(0, tk.END)
        self.type.insert(0, sel.parttype)
        self.type.config(state="readonly")

