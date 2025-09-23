from odoo import fields, models


class ShopClient(models.Model):
    _name = 'shop.client'

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    birthday = fields.Date(string='Birthday')
    address = fields.Char(string='Address')
    client_id = fields.Char(string='Client ID', required=True)
    point = fields.Integer(string='Points', default=0, readonly=True)
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone number')
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
