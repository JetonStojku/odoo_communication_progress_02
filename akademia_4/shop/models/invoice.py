# -*- coding: utf-8 -*-
from odoo import fields, models


class ShopInvoice(models.Model):
    """ This model represents invoice."""
    _name = 'shop.invoice'

    invoice_nr = fields.Char(string='Invoice Nr.', required=True)
    client_id = fields.Many2one(comodel_name='shop.client', string='Client', requirement=True)
    employee_id = fields.Many2one('shop.employee', string='Employee')
    total = fields.Float(string='Total', digits=(16, 2))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('paid', 'Paid'),
    ], string='Status', default='draft')

    payment_type = fields.Selection(
        string='Payment type',
        selection=[('cash', 'Cash'),
                   ('card', 'Card'),
                   ('point', 'Point')],
        required=False, )
    invoice_line_ids = fields.One2many('shop.invoice.line', 'invoice_id', string='')


class ShopInvoiceLine(models.Model):
    _name = 'shop.invoice.line'

    invoice_id = fields.Many2one(comodel_name='shop.invoice', string='Invoice', required=True)
    product_id = fields.Many2one('shop.product', string='Product')
    quantity = fields.Float(string='Quantity', digits=(16, 2))
    price = fields.Float(string='Price', digits=(16, 2))
    total = fields.Float(string='Total', digits=(16, 2))
