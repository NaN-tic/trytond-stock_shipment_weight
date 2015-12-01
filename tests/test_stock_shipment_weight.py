# This file is part of the stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockShipmentWeightTestCase(ModuleTestCase):
    'Test Stock Shipment Weight module'
    module = 'stock_shipment_weight'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockShipmentWeightTestCase))
    return suite