import datetime as dt
import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.modules.stock_package.exceptions import PackageError
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = dt.date.today()

        # Activate modules
        activate_modules(['stock_package', 'stock_shipment_weight'])

        # Create company
        _ = create_company()
        company = get_company()

        # Create customer
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()

        # Create product
        ProductUom = Model.get('product.uom')
        ProductTemplate = Model.get('product.template')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        template = ProductTemplate()
        template.name = 'Product'
        template.default_uom = unit
        template.type = 'goods'
        template.list_price = Decimal('20')
        template.save()
        product, = template.products

        # Get stock locations
        Location = Model.get('stock.location')
        warehouse_loc, = Location.find([('code', '=', 'WH')])
        customer_loc, = Location.find([('code', '=', 'CUS')])
        output_loc, = Location.find([('code', '=', 'OUT')])

        # Create Shipment Out
        ShipmentOut = Model.get('stock.shipment.out')
        shipment_out = ShipmentOut()
        shipment_out.planned_date = today
        shipment_out.customer = customer
        shipment_out.warehouse = warehouse_loc
        shipment_out.company = company

        # Add two shipment lines of same product
        StockMove = Model.get('stock.move')
        shipment_out.outgoing_moves.extend([StockMove(), StockMove()])
        for move in shipment_out.outgoing_moves:
            move.product = product
            move.uom = unit
            move.quantity = 1
            move.from_location = output_loc
            move.to_location = customer_loc
            move.company = company
            move.unit_price = Decimal('1')
            move.currency = company.currency
        shipment_out.save()

        # Pack shipment
        shipment_out.click('wait')
        shipment_out.click('assign_force')
        shipment_out.click('pick')

        # Package products
        PackageType = Model.get('stock.package.type')
        box = PackageType(name='box')
        box.manual_weight_uom, = ProductUom.find([('name', '=', "Kilogram")])
        box.save()
        package1 = shipment_out.packages.new(type=box)
        package1.manual_weight = 80.0
        package_child = package1.children.new(shipment=shipment_out, type=box)
        package_child.manual_weight = 100
        moves = package_child.moves.find()
        self.assertEqual(len(moves), 2)
        package_child.moves.append(moves[0])

        with self.assertRaises(PackageError):
            shipment_out.click('pack')

        package2 = shipment_out.packages.new(type=box)
        package2.manual_weight = 30.0
        moves = package2.moves.find()
        self.assertEqual(len(moves), 1)

        package2.moves.append(moves[0])
        shipment_out.click('pack')
        self.assertEqual([(package.manual_weight, package.weight)
                          for package in shipment_out.packages],
                          [(80.0, None), (100.0, None), (30.0, None)])
        self.assertEqual(
            sum(package.total_weight for package in shipment_out.packages
                if package.parent == None), 210.0)
