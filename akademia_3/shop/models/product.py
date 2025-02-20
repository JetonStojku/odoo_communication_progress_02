from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ShopProduct(models.Model):
    _name = 'shop.product'

    name = fields.Char(string='Product Name', required=True)
    purchase_price = fields.Float(string='Purchase Price', required=True)
    selling_price = fields.Float(string='Sell Price', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    category_ids = fields.Many2many(comodel_name='shop.category', string='Category', required=True)

    # _sql_constraints = [
    #     ('quantity', 'CHECK(quantity>=0)', 'Quantity must be positive'),
    # ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for product in self:
            if product.quantity < 0:
                raise ValidationError('Quantity must be positive')


class ShopCategory(models.Model):
    _name = 'shop.category'

    name = fields.Char(string='Category Name', required=True)
