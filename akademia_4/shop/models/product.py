from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ShopProduct(models.Model):
    _name = 'shop.product'
    _rec_name = 'product'

    product = fields.Char(string='Product')
    purchase_price = fields.Float(string='Purchase Price', required=True)
    selling_price = fields.Float(string='Sell Price', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    description = fields.Text(string='Description')
    category_ids = fields.Many2many('shop.category', string='Categories')


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

    name = fields.Char(string='Category')
    description = fields.Text(string='Description')
