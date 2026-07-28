from odoo import fields, models, api


class SellingStoreProduct(models.Model):
    _name = 'selling_store.product'

    product = fields.Char(string='Product Name', required=True)
    quantity = fields.Float(string='Quantity', default=0, required=True)
    buy_price = fields.Float(string='Buy Price', default=0, required=True)
    sell_price = fields.Float(string='Sell Price', default=0, required=True)
    get_points = fields.Boolean(string='Get Points', default=True, required=True)
    category_ids = fields.Many2many(comodel_name='selling_store.category', string='Category')
