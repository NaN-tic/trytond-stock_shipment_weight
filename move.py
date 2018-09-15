# This file is part of the stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Move']


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'
    weight = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']),
        'on_change_with_weight')
    weight_uom = fields.Function(fields.Many2One('product.uom', 'Weight Uom'),
        'on_change_with_weight_uom')
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')

    @fields.depends('product', 'quantity')
    def on_change_with_weight(self, name=None):
        return (self.product.weight * self.quantity if self.product and
                self.product.weight and self.quantity else None)

    @fields.depends('product')
    def on_change_with_weight_uom(self, name=None):
        return (self.product.weight_uom.id if self.product and
                self.product.weight_uom else None)

    @fields.depends('product')
    def on_change_with_weight_digits(self, name=None):
        return self.product.weight_digits if self.product else None
