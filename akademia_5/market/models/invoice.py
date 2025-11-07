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
    invoice_line_ids = fields.One2many(comodel_name='market.invoice.line', inverse_name='invoice_id',
                                       string='Invoice Lines')


class MarketInvoiceLine(models.Model):
    _name = 'market.invoice.line'

    product_id = fields.Many2one(comodel_name='market.product', string='Product')
    invoice_id = fields.Many2one(comodel_name='market.invoice', string='Invoice')
    quantity = fields.Float(string='Quantity', digits=(16, 4), quantity=1)
    price = fields.Float(string='Price', digits=(16, 2))
    total = fields.Float(string='Total', digits=(16, 2))
