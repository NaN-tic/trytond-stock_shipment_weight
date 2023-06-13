# This file is part stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pyson import Eval, Id
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.modules.stock_shipment_measurements.stock import MeasurementsMixin


class ShipmentManualWeightMixin(object):
    __slots__ = ()

    manual_weight = fields.Float('Manual Weight', digits='weight_uom',
        states={
            'readonly': Eval('state').in_(['cancelled', 'done']),
        }, depends=['state'])

    @classmethod
    def __register__(cls, module_name):
        sql_table = cls.__table__()
        table = cls.__table_handler__(module_name)

        transaction = Transaction()
        cursor = transaction.connection.cursor()

        weight = table.column_exist('weight')

        super().__register__(module_name)

        if weight:
            cursor.execute(*sql_table.update(
                    columns=[sql_table.manual_weight],
                    values=[sql_table.weight]))
            table.drop_column('weight')
            table.drop_column('weight_uom')


class ShipmentIn(ShipmentManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'


class ShipmentInReturn(ShipmentManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.in.return'


class ShipmentOut(ShipmentManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'


class ShipmentOutReturn(ShipmentManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'


class ShipmentInternal(MeasurementsMixin, ShipmentManualWeightMixin,
        metaclass=PoolMeta):
    __name__ = 'stock.shipment.internal'

    @classmethod
    def _measurements_location_condition(cls, shipment, move, location):
        return move.from_location == location.id
