import math
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
    return price


def cuba_tri_calc(szer, dl, wys, tkan, wata):
    size = szer*dl + szer*wys + wys*dl + math.sqrt(dl*dl+szer*szer)
    price = mats_price(size, tkan, wata)
    if size < 3700:
        price += size * value_kostka_tr_small
    else:
        price += size * value_kostka_tr_med
    price = ceiling_half(price)
    return price


def pig_calc(szer, dl, wys, tkan, wata):
    size = szer*dl + (szer*wys + wys*dl)*2
    price = mats_price(size, tkan, wata)
    if size < 3500:
        price += size * value_swinka_small
    else:
        price += size * value_swinka_big
    price = ceiling_half(price)
    return price


def ham_calc(szer, dl, tkan, wata):
    size = szer*dl
    price = mats_price(size, tkan, wata)
    if size < 1000:
        price += size * value_hamak_mini
    else:
        price += size * value_hamak
    price = ceiling_half(price)
    return price


class ItemList:
    def __init__(self):
        self.items = dict()

    def add(self, item):
        self.items[len(self.items)] = item

    def get(self, idx):
        return self.items[idx]



class Item:
    def __init__(self, parttype, comment, size, value, tranz, date):
        self.parttype = parttype
        self.comment = comment
        self.size = size
        self.value = value
        self.tranz = tranz
        self.date = date

    def __init__(self):
        self.parttype = str()
        self.comment = str()
        self.size = int()
        self.value = int()
        self.tranz = None # TODO: create tranz class and link here
        self.date = int()

