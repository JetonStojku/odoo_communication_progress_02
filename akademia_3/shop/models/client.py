from odoo import fields, models


class ShopClient(models.Model):
    _name = 'shop.client'
    _description = 'Shop Client'

    name = fields.Char(string='Client Name', required=True)
    surname = fields.Char(string='Client Surname', required=True)
    points = fields.Integer(string='Points', required=True, default=0, readonly=True)
    phone_number = fields.Char(string='Phone number', required=True)
    email = fields.Char(string='Email')
