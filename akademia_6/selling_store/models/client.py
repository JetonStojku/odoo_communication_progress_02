from odoo import fields, models, api


class SellingStoreClient(models.Model):
    _name = 'selling_store.client'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    email = fields.Char(string='Email', required=False)
    phone_number = fields.Char(string='Phone Number')
    birthday = fields.Date(string='Birthday', required=False)
    address = fields.Char(string='Address')
    points = fields.Float(string='Points')
