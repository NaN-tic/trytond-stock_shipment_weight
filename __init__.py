# This file is part stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import shipment
from . import move

def register():
    Pool.register(
        configuration.Configuration,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        move.Move,
        module='stock_shipment_weight', type_='model')
