==============================
Stock Shipment Weight Scenario
==============================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date.today()

Install stock_shipment_weight::

    >>> config = activate_modules('stock_shipment_weight')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create parties::

    >>> Party = Model.get('party.party')
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()
    >>> customer = Party(name='Customer')
    >>> customer.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> gram, = ProductUom.find([('name', '=', 'Gram')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal('10')
    >>> template.cost_price_method = 'fixed'
    >>> template.weight = 10
    >>> template.weight_uom = gram
    >>> product, = template.products
    >>> product.cost_price = Decimal('5')
    >>> template.save()
    >>> product, = template.products

Create Customer Shipment::

    >>> Location = Model.get('stock.location')
    >>> ShipmentOut = Model.get('stock.shipment.out')
    >>> Move = Model.get('stock.move')
    >>> customer_loc, = Location.find([('type', '=', 'customer')], limit=1)
    >>> shipment = ShipmentOut()
    >>> shipment.customer = customer
    >>> outgoing_move = Move()
    >>> shipment.outgoing_moves.append(outgoing_move)
    >>> outgoing_move.product = product
    >>> outgoing_move.uom = unit
    >>> outgoing_move.quantity = 2
    >>> outgoing_move.from_location = shipment.warehouse.output_location
    >>> outgoing_move.to_location = customer_loc
    >>> outgoing_move.company = company
    >>> outgoing_move.unit_price = Decimal('1')
    >>> outgoing_move.currency = company.currency
    >>> shipment.save()
    >>> shipment.weight_func == 20
    True

Create Customer Return Shipment::

    >>> ShipmentOutReturn = Model.get('stock.shipment.out.return')
    >>> shipment = ShipmentOutReturn()
    >>> shipment.customer = customer
    >>> incoming_move = Move()
    >>> shipment.incoming_moves.append(incoming_move)
    >>> incoming_move.product = product
    >>> incoming_move.uom = unit
    >>> incoming_move.quantity = 2
    >>> incoming_move.from_location = customer_loc
    >>> incoming_move.to_location = shipment.warehouse.input_location
    >>> incoming_move.company = company
    >>> incoming_move.unit_price = Decimal('1')
    >>> incoming_move.currency = company.currency
    >>> shipment.save()
    >>> shipment.click('receive')
    >>> shipment.weight_func == 20
    True
