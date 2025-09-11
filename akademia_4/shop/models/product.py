from odoo import fields, models


class ShopProduct(models.Model):
    _name = 'shop.product'

    name = fields.Char(string='Product')
    purchase_price = fields.Float(string='Purchase Price', required=True)
    selling_price = fields.Float(string='Sell Price', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    description = fields.Text(string='Description')
    category_ids = fields.Many2many('shop.category', string='Categories')


class ShopCategory(models.Model):
    _name = 'shop.category'

    name = fields.Char(string='Category')
    description = fields.Text(string='Description')
