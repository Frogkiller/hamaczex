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

    def delete_item(self, idx):
        parent = self.items.get(idx).trans
        if parent is not None:
            self.trans.get(parent).items.remove(force_uuid(idx))
        self.items.delete(idx)

    def delete_trans(self, idx):
        parent = self.trans.get(idx).client
        if parent is not None:
            self.clients.get(parent).transactions.remove(force_uuid(idx))
        childrens = self.trans.get(idx).items
        for child in childrens:
            self.items.get(child).trans = None
        self.trans.delete(idx)

    def delete_cli(self, idx):
        childrens = self.clients.get(idx).transactions
        for child in childrens:
            self.trans.get(child).client = None
        self.clients.delete(idx)

    def update_item(self, it):
        return self.items.put(it)

    def update_trans(self, trans):
        return self.trans.put(trans)

    def update_cli(self, cli):
        return self.clients.put(cli)

    def conn_item_trans(self, ite, tra):
        transer = self.trans.get(force_uuid(tra))
        item = self.items.get(force_uuid(ite))
        if item.trans is None:
            transer.add_item(force_uuid(ite))
            item.set_trans(force_uuid(tra))
            transer.value = str(float(transer.value) + item.value)

    def conn_trans_cli(self, tra, cli):
        clienter = self.clients.get(force_uuid(cli))
        transer = self.trans.get(force_uuid(tra))
        if transer.client is None:
            clienter.add_trans(force_uuid(tra))
            transer.set_cli(force_uuid(cli))

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

    def get_cli(self, idx):
        try:
            el = self.clients.get(force_uuid(idx))
        except KeyError:
            el = None
        return el

    def get_trans(self, idx):
        try:
            el = self.trans.get(force_uuid(idx))
        except KeyError:
            el = None
        return el

    def get_item(self, idx):
        try:
            el = self.items.get(force_uuid(idx))
        except KeyError:
            el = None
        return el

    def print_cli(self, idx):
        if idx is not None:
            el = self.get_cli(idx)
            return el.name + ' ' + el.surname
        else:
            return ''


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
    def __init__(self, parttype='', comment='', size='', value=0, trans=None, date=datetime.date.today()):
        self.parttype = parttype
        self.comment = comment
        self.size = size
        self.value = value
        self.trans = trans
        self.date = date
        self.idx = None

    def set_id(self, idx):
        self.idx = idx

    def set_trans(self, idx):
        self.trans = idx


states = {"New": 0, "Prepared": 1, "Paid": 2, "Sent": 3, "Done": 4}
shippings = {"Collection": 0, "Eco": 1, "Prio": 2, "InPost": 3, "Pobranie": 4}
shippings_price = {"Collection": 0, "Eco": 5, "Prio": 10, "InPost": 12, "Pobranie": 15}
sources = {"OLX": 0, "Facebook": 1, "Other": 2}


class Transaction:
    def __init__(self, state=None, comment='', client=None, items=None, date='', date_fin='', shipping=None,
                 value=0):
        self.state = state
        self.comment = comment
        self.client = client
        if items is None:
            items = set()
        self.items = items
        self.date = date
        self.date_fin = date_fin
        self.idx = None
        self.shipping = shipping
        self.value = value

    def set_id(self, idx):
        self.idx = idx

    def add_item(self, idx):
        self.items.add(idx)

    def rm_item(self, idx):
        self.items.remove(idx)

    def set_cli(self, idx):
        self.client = idx

    def add_value(self):
        pass


class Client:
    def __init__(self, source='', comment='', nick='', name='', surname='', address='', phone='',
                 transactions=None, date=datetime.date.today()):
        self.source = source #4
        self.comment = comment #8
        self.nick = nick #1
        self.name = name #2
        self.surname = surname #3
        self.phone = phone #5
        self.address = address #6
        if transactions is None:
            transactions = set()
        self.transactions = transactions #7
        self.date = date
        self.idx = None

    def set_id(self, idx):
        self.idx = idx

    def add_trans(self, idx):
        self.transactions.add(idx)

    def rm_trans(self, idx):
        self.transactions.remove(idx)