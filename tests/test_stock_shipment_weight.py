#!/usr/bin/env python
# This file is part stock_shipment_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction


class StockShipmentWeightTestCase(unittest.TestCase):
    'Test Stock Shipment Weight module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('stock_shipment_weight')

    def test0005views(self):
        'Test views'
        test_view('stock_shipment_weight')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockShipmentWeightTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
