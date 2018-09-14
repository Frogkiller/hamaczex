import math
import pickle
import datetime
from prices import *
import uuid

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


def cube_calc(szer, dl, wys, tkan, wata):
    size = (szer*dl + szer*wys + wys*dl)*2
    price = mats_price(size, tkan, wata)
    if size < 2600:
        price += size * value_kostka_small
    elif size <3700:
        price += size * value_kostka_med
    else:
        price += size * value_kostka_big
    price = ceiling_half(price)
    return price, size


def cuba_tri_calc(szer, dl, wys, tkan, wata):
    size = szer*dl + szer*wys + wys*dl + math.sqrt(dl*dl+szer*szer)
    price = mats_price(size, tkan, wata)
    if size < 3700:
        price += size * value_kostka_tr_small
    else:
        price += size * value_kostka_tr_med
    price = ceiling_half(price)
    return price, size


def pig_calc(szer, dl, wys, tkan, wata):
    size = szer*dl + (szer*wys + wys*dl)*2
    price = mats_price(size, tkan, wata)
    if size < 3500:
        price += size * value_swinka_small
    else:
        price += size * value_swinka_big
    price = ceiling_half(price)
    return price, size


def ham_calc(szer, dl, tkan, wata):
    size = szer*dl
    price = mats_price(size, tkan, wata)
    if size < 1000:
        price += size * value_hamak_mini
    else:
        price += size * value_hamak
    price = ceiling_half(price)
    return price, size


class DataModel:
    def __init__(self):
        self.items = ItemList()
        self.trans = ItemList()
        self.clients = ItemList()

    def add_item(self, *rest):
        return self.items.add(Item(*rest))

    def add_trans(self, *rest):
        return self.trans.add(Transaction(*rest))

    def add_client(self, *rest):
        return self.clients.add(Client(*rest))

    def delete_trans(self, idx):
        self.trans.delete(idx)

    def update_trans(self, trans):
        return self.trans.put(trans)

    def conn_item_trans(self, ite, tra):
        self.trans.get(force_uuid(tra)).add_item(force_uuid(ite))
        self.items.get(force_uuid(ite)).set_trans(force_uuid(tra))

    def conn_trans_cli(self, tra, cli):
        self.clients.get(force_uuid(cli)).add_trans(force_uuid(tra))
        self.trans.get(force_uuid(tra)).set_cli(force_uuid(cli))

    def dump(self):
        filehandler = open("database.obj", "wb")
        pickle.dump(self.items, filehandler)
        pickle.dump(self.trans, filehandler)
        pickle.dump(self.clients, filehandler)
        filehandler.close()

    def load(self):
        filehandler = open("database.obj", "rb")
        self.items = pickle.load(filehandler)
        self.trans = pickle.load(filehandler)
        self.clients = pickle.load(filehandler)
        filehandler.close()


def force_uuid(idx):
    if type(idx) is str:
        return uuid.UUID(idx)
    else:
        return idx


class ItemList:
    def __init__(self):
        self.items = dict()

    def add(self, item):
        new_id = uuid.uuid4()
        self.items[new_id] = item
        item.set_id(new_id)
        return item

    def put(self, item):
        self.items[item.idx] = item

    def get(self, idx):
        return self.items[force_uuid(idx)]

    def delete(self, idx):
        del self.items[force_uuid(idx)]

    def __iter__(self):
        return iter(self.items)


class Item:
    def __init__(self, parttype='', comment='', size='', value=0, tranz=None, date=datetime.date.today()):
        self.parttype = parttype
        self.comment = comment
        self.size = size
        self.value = value
        self.tranz = tranz
        self.date = date
        self.idx = None

    def set_id(self, idx):
        self.idx = idx

    def set_trans(self, idx):
        self.tranz = idx


class Transaction:
    def __init__(self, state=None, comment='', client=None, items=None, date=datetime.date.today()):
        self.state = state
        self.comment = comment
        self.client = client
        if items is None:
            items = set()
        self.items = items
        self.date = date
        self.idx = None

    def set_id(self, idx):
        self.idx = idx

    def add_item(self, idx):
        self.items.add(idx)

    def rm_item(self, idx):
        self.items.remove(idx)

    def set_cli(self, idx):
        self.client = idx


class Client:
    def __init__(self, source='', comment='', nick='', name='', surname='', address='', phone='',
                 transactions=None, date=datetime.date.today()):
        self.source = source
        self.comment = comment
        self.nick = nick
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        if transactions is None:
            transactions = set()
        self.transactions = transactions
        self.date = date
        self.idx = None

    def set_id(self, idx):
        self.idx = idx

    def add_trans(self, idx):
        self.transactions.add(idx)

    def rm_trans(self, idx):
        self.transactions.remove(idx)