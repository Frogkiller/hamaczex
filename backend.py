import math
import datetime
from prices import *

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
        self.items.add(Item(*rest))

    def add_tans(self, *rest):
        self.trans.add(Transaction(*rest))

    def add_client(self, *rest):
        self.clients.add(Client(*rest))


class ItemList:
    def __init__(self):
        self.items = dict()

    def add(self, item):
        new_id = len(self.items)
        self.items[new_id] = item
        item.set_id(new_id)

    def put(self, item):
        self.items[item.iid] = self.item

    def get(self, idx):
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)


class Item:
    def __init__(self, parttype=str(), comment='', size=0, value=0, tranz=None, date=datetime.date.today()):
        self.parttype = parttype
        self.comment = comment
        self.size = size
        self.value = value
        self.tranz = tranz
        self.date = date
        self.iid = None

    def set_id(self, iid):
        self.iid = iid


class Transaction:
    def __init__(self, parttype=str(), comment='', client=None, items=ItemList(), date=datetime.date.today()):
        self.parttype = parttype
        self.comment = comment
        self.client = client
        self.items = items
        self.date = date
        self.iid = None

    def set_id(self, iid):
        self.iid = iid


class Client:
    def __init__(self, parttype=str(), comment='', nick='', name='', surname='', address='', phone='',
                 transactions=ItemList(), date=datetime.date.today()):
        self.parttype = parttype
        self.comment = comment
        self.nick = nick
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.transactions = transactions
        self.date = date
        self.iid = None

    def set_id(self, iid):
        self.iid = iid