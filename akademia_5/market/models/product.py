# -*- coding: utf-8 -*-

from odoo import fields, models


class MarketProduct(models.Model):
    _name = 'market.product'
    _description = 'Product'

    product = fields.Char(string='Product name', required=True)
    quantity = fields.Float(string='Quantity', digits=(16, 6), default=0)
    purchase_price = fields.Float(string='Purchase price', digits=(12, 4))
    sell_price = fields.Float(string='Sell price', digits=(12, 4))
    category_ids = fields.Many2many(comodel_name='market.category', string='')


class MarketCategory(models.Model):
    _name = 'market.category'

    category = fields.Char(string='Category name')
