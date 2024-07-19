# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval, Id


class PackageType(metaclass=PoolMeta):
    __name__ = 'stock.package.type'
    manual_weight = fields.Float(
        "Manual Weight", digits='manual_weight_uom',
        help="The manual weight of the package when empty.")
    manual_weight_uom = fields.Many2One(
        'product.uom', "Manual Weight UOM",
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        states={
            'required': Bool(Eval('manual_weight')),
            })


class Package(metaclass=PoolMeta):
    __name__ = 'stock.package'
    manual_weight = fields.Float('Manual Weight')
    manual_weight_uom = fields.Many2One(
        'product.uom', "Manual Weight UOM",
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        states={
            'required': Bool(Eval('weight')),
            })

    @fields.depends('type')
    def on_change_type(self):
        super().on_change_type()
        # weight_uom is not default option in stock_package module.
        if self.type:
            self.manual_weight_uom = self.type.manual_weight_uom
