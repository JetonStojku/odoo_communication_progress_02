# -*- coding: utf-8 -*-
from odoo import fields, models


class MarketClient(models.Model):
    """ This model represents client."""
    _name = 'market.client'

    name = fields.Char(string='Client Name', required=True)
    surname = fields.Char(string='Client Surname', required=True)
    client_code = fields.Char(string='Code')
    birthday = fields.Date(string='Birthday')
    point = fields.Float(string='Points', digits=(16, 2))
