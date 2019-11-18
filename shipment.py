# This file is part stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pyson import Eval, Id
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOut', 'ShipmentOutReturn']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'
    weight_uom = fields.Many2One('product.uom', 'Weight Uom',
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        states={
            'readonly': Eval('state').in_(['cancel', 'done']),
        }, depends=['state'])
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')
    weight = fields.Float('Weight', digits=(16, Eval('weight_digits', 2)),
        states={
            'readonly': Eval('state').in_(['cancel', 'done']),
        }, depends=['state', 'weight_digits'])
    weight_lines = fields.Function(fields.Float('Weight of Moves',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'get_weight_lines')
    weight_func = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_func')

    @classmethod
    def get_weight_lines(cls, shipments, names):
        pool = Pool()
        Config = pool.get('stock.configuration')
        Uom = pool.get('product.uom')
        Move = pool.get('stock.move')

        origins = Move._get_origin()
        keep_origin = True if 'stock.move' in origins else False

        config = Config(1)
        if config.weight_uom:
            default_uom = config.weight_uom
        else:
            default_uom, = Uom.search([('symbol', '=', 'g')], limit=1)

        wlines = dict((s.id, 0.0) for s in shipments)
        for shipment in shipments:
            to_uom = shipment.weight_uom or default_uom
            digits = shipment.weight_digits
            weight = Decimal(0.0)
            moves = (shipment.inventory_moves
                if (keep_origin and shipment.inventory_moves)
                else shipment.outgoing_moves)
            for move in moves:
                if move.quantity and move.product and move.product.weight:
                    from_uom = move.product.weight_uom
                    weight += Decimal(Uom.compute_qty(from_uom,
                        move.product.weight * move.quantity, to_uom,
                        round=False))
            wlines[shipment.id] = float(weight.quantize(
                Decimal(str(10.0 ** -digits))))
        return {'weight_lines': wlines}

    @fields.depends('weight', 'weight_lines')
    def on_change_with_weight_func(self, name=None):
        if self.weight:
            return self.weight
        return self.weight_lines

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2


class ShipmentOutReturn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'
    weight_uom = fields.Many2One('product.uom', 'Weight Uom',
            states={
                'readonly': Eval('state') != 'draft',
            }, depends=['state'])
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')
    weight = fields.Float('Weight', digits=(16, Eval('weight_digits', 2)),
            states={
                'readonly': Eval('state') != 'draft',
            }, depends=['state', 'weight_digits'])
    weight_lines = fields.Function(fields.Float('Weight of Moves',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'get_weight_lines')
    weight_func = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_func')

    @classmethod
    def get_weight_lines(cls, shipments, names):
        pool = Pool()
        Config = pool.get('stock.configuration')
        Uom = pool.get('product.uom')
        Move = pool.get('stock.move')

        config = Config(1)
        if config.weight_uom:
            default_uom = config.weight_uom
        else:
            default_uom, = Uom.search([('symbol', '=', 'g')], limit=1)

        origins = Move._get_origin()
        keep_origin = True if 'stock.move' in origins else False

        wlines = dict((s.id, 0.0) for s in shipments)
        for shipment in shipments:
            to_uom = shipment.weight_uom or default_uom
            digits = shipment.weight_digits
            weight = Decimal(0.0)
            moves = (shipment.inventory_moves
                if (keep_origin and shipment.inventory_moves)
                else shipment.incoming_moves)
            for move in moves:
                if move.quantity and move.product and move.product.weight:
                    from_uom = move.product.weight_uom
                    weight += Decimal(Uom.compute_qty(from_uom,
                        move.product.weight * move.quantity, to_uom,
                        round=False))
            wlines[shipment.id] = float(weight.quantize(
                Decimal(str(10.0 ** -digits))))
        return {'weight_lines': wlines}

    @fields.depends('weight', 'weight_lines')
    def on_change_with_weight_func(self, name=None):
        if self.weight:
            return self.weight
        return self.weight_lines

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2
