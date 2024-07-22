# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval, Id


class ManualWeightMixin:
    __slots__ = ()

    manual_weight = fields.Float(
        "Manual Weight", digits='manual_weight_uom',
        help="The manual weight of the package when empty.")
    manual_weight_uom = fields.Many2One(
        'product.uom', "Manual Weight UOM",
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        states={
            'required': Bool(Eval('manual_weight')),
            })

    @classmethod
    def __register__(cls, module_name):
        table = cls.__table_handler__(module_name)

        # Migration from 6.8: rename weight to manual_weight
        if (table.column_exist('weight')
                and not table.column_exist('manual_weight')):
            table.column_rename('weight', 'manual_weight')
            table.column_rename('weight_uom', 'manual_weight_uom')
        super().__register__(module_name)


class PackageType(ManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.package.type'


class Package(ManualWeightMixin, metaclass=PoolMeta):
    __name__ = 'stock.package'

    @fields.depends('type')
    def on_change_type(self):
        super().on_change_type()
        # weight_uom is not default option in stock_package module.
        if self.type:
            self.manual_weight_uom = self.type.manual_weight_uom
