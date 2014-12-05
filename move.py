# This file is part of the stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta
__all__ = ['Move']

__metaclass__ = PoolMeta


class Move:
    __name__ = 'stock.move'
    weight = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']),
        'get_product_field', searcher='search_product_field')
    weight_uom = fields.Function(fields.Many2One('product.uom', 'Weight Uom'),
        'get_product_field', searcher='search_product_field')
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'get_product_field', searcher='search_product_field')

    def get_product_field(self, name):
        value = getattr(self.product, name)
        if name == 'weight_uom' and value != None:
            value = value.id
        return value

    @classmethod
    def search_product_field(cls, name, clause):
        return [('product.' + name,) + tuple(clause[1:])]
