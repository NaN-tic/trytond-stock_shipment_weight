# This file is part stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import shipment
from . import package

def register():
    Pool.register(
        shipment.ShipmentIn,
        shipment.ShipmentInReturn,
        shipment.ShipmentInternal,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        module='stock_shipment_weight', type_='model')
    Pool.register(
        package.PackageType,
        package.Package,
        depends=['stock_package'],
        module='stock_shipment_weight', type_='model')
