# -*- coding: utf-8 -*-
from odoo import fields, models


class MarketInvoice(models.Model):
    """ This model represents invoice."""
    _name = 'market.invoice'

    invoice_code = fields.Char(string='Invoice Number', required=True, defualt='New')
    invoice_date = fields.Datetime(string='Invoice date', default=lambda self: fields.Datetime.now())
    invoice_type = fields.Selection([
        ('in', 'Purchase'),
        ('out', 'Sell')
    ], string='Status', default='out')
    client_id = fields.Many2one(comodel_name='market.client', string='Client')
    employee_id = fields.Many2one(comodel_name='market.employee', string='Employee')
    total = fields.Float(string='', digits=(16, 4))
