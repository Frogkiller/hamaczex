import backend

old = backend.DataModel()
new = backend.DataModel()

old.load()
for _, x in old.items.items.items():
    item = backend.Item(x.parttype, x.comment, x.size, x.value, x.trans, x.date)
    item.set_id(x.idx)
    new.items.put(item)

for _, y in old.trans.items.items():
    tran = backend.Transaction(y.state, y.comment, y.client, y.items, y.date, '', y.shipping,
                 y.value)
    tran.set_id(y.idx)
    new.trans.put(tran)

for _, z in old.clients.items.items():
    cli = backend.Client(z.source, z.comment, z.nick, z.name, z.surname, z.address, z.phone, z.transactions, z.date)
    cli.set_id(z.idx)
    new.clients.put(cli)

new.dump()

