from odoo import fields, models, api


class SellingStoreCategory(models.Model):
    _name = 'selling_store.category'

    name = fields.Char(string='Category Name')
    description = fields.Char(string='Description')
