#!/usr/bin/env python
# -*- coding: utf-8 -*-
sym = map(lambda x: chr(ord('0') + x), range(10))
sym1 = map(lambda x: chr(ord('A') + x), range(26))
sym.extend(sym1)
sym.remove('1')
sym.remove('I')
bits = 34

# e.g.
# T1
# ST1P2A8EK4JDE
# ST1P2538253601568

# S1
# BS1A37TVTE8W
# BS1A312080218798 (8G)

# W1
# A (4G) 31(product pcs)
# W1A3113072600000000
# W1A317AWA7ZNN4
# W1A3113072699999999
# W1A317AWCETXUK


def enc(_sn):
    ret = []
    i = int(_sn)
    x = i
    while (x % bits) or (x / bits):
        ret.insert(0, sym[x % bits])
        x = (x / bits)
    return ''.join(ret)


def dec(_sn):
    print _sn
    ret = 0
    for x in _sn:
        c = sym.index(x)
        ret = ret * bits + c
    print ret
    return ret


class SnEnCrypter(object):

    def __init__(self, _str_part, _num_part):
        self.str_part = _str_part
        self.num_part = _num_part

    def do_enc(self):
        return '%s%s' % (self.str_part, enc(self.num_part))

    def do_dec(self):
        return '%s%s' % (self.str_part, dec(self.num_part))


def en_csn(product_code, hardware_code, production_date, pcs_id):
    _str_part = '%s%s' % (product_code, hardware_code)
    _num_part = '%s%s' % (production_date.strftime('%y%m%d'), pcs_id)
    return SnEnCrypter(_str_part, _num_part).do_enc()


def de_csn(product_code, hardware_code, sn):
    _str_part = '%s%s' % (product_code, hardware_code)
    _num_part = sn[len(_str_part):]
    return SnEnCrypter(_str_part, _num_part).do_dec()

if __name__ == '__main__':
    from datetime import datetime
    sn = en_csn('C1', 'Y1', datetime.now(), 211)
    print sn
    print de_csn('C1', 'Y1', sn)
