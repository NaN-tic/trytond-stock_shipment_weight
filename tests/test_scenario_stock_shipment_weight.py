import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
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

        # Install stock_shipment_weight
        activate_modules(['stock_shipment_weight'])

        # Create company
        _ = create_company()
        company = get_company()

        # Create parties
        Party = Model.get('party.party')
        supplier = Party(name='Supplier')
        supplier.save()
        customer = Party(name='Customer')
        customer.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        gram, = ProductUom.find([('name', '=', 'Gram')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.list_price = Decimal('10')
        template.cost_price_method = 'fixed'
        template.weight = 10
        template.weight_uom = gram
        product, = template.products
        product.cost_price = Decimal('5')
        template.save()
        product, = template.products

        # Locations
        Location = Model.get('stock.location')
        customer_loc, = Location.find([('type', '=', 'customer')], limit=1)
        storage_loc, = Location.find([('type', '=', 'storage')], limit=1)
        lost_loc, = Location.find([('type', '=', 'lost_found')], limit=1)

        # Create Customer Shipment
        ShipmentOut = Model.get('stock.shipment.out')
        Move = Model.get('stock.move')
        shipment = ShipmentOut()
        shipment.customer = customer
        outgoing_move = Move()
        shipment.outgoing_moves.append(outgoing_move)
        outgoing_move.product = product
        outgoing_move.unit = unit
        outgoing_move.quantity = 2
        outgoing_move.from_location = shipment.warehouse.output_location
        outgoing_move.to_location = customer_loc
        outgoing_move.company = company
        outgoing_move.unit_price = Decimal('1')
        outgoing_move.currency = company.currency
        shipment.save()
        shipment.manual_weight = 10
        self.assertEqual(shipment.weight, 0.02)

        # Create Customer Return Shipment
        ShipmentOutReturn = Model.get('stock.shipment.out.return')
        shipment = ShipmentOutReturn()
        shipment.customer = customer
        incoming_move = Move()
        shipment.incoming_moves.append(incoming_move)
        incoming_move.product = product
        incoming_move.unit = unit
        incoming_move.quantity = 2
        incoming_move.from_location = customer_loc
        incoming_move.to_location = shipment.warehouse.input_location
        incoming_move.company = company
        incoming_move.unit_price = Decimal('1')
        incoming_move.currency = company.currency
        shipment.save()
        shipment.click('receive')
        shipment.manual_weight = 10
        self.assertEqual(shipment.weight, 0.02)

        # Create Internal Shipment
        ShipmentInternal = Model.get('stock.shipment.internal')
        shipment = ShipmentInternal()
        shipment.from_location = storage_loc
        shipment.to_location = lost_loc
        incoming_move = Move()
        shipment.incoming_moves.append(incoming_move)
        incoming_move.from_location = shipment.from_location
        incoming_move.to_location = lost_loc
        incoming_move.product = product
        incoming_move.unit = unit
        incoming_move.quantity = 2
        incoming_move.company = company
        shipment.save()
        self.assertEqual(shipment.weight, 0.02)