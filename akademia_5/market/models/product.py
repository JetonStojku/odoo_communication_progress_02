# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MarketProduct(models.Model):
    _name = 'market.product'
    _description = 'Product'
    _rec_name = 'product'

    product = fields.Char(string='Product name', required=True)
    quantity = fields.Float(string='Quantity', digits=(16, 6), default=0)
    purchase_price = fields.Float(string='Purchase price', digits=(12, 4))
    sell_price = fields.Float(string='Sell price', digits=(12, 4))
    category_ids = fields.Many2many(comodel_name='market.category', string='')

    # _sql_constraints = [
    #     ('quantity', 'CHECK(quantity>=0)', 'Quantity must be positive'),
    # ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for product in self:
            if product.quantity < 0:
                raise ValidationError(f'Quantity must be positive, {product.product}: {product.quantity}')


class MarketCategory(models.Model):
    _name = 'market.category'
    _rec_name = 'category'

    category = fields.Char(string='Category name')
