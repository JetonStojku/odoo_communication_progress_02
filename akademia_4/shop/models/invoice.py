# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ShopInvoice(models.Model):
    """ This model represents invoice."""
    _name = 'shop.invoice'

    invoice_nr = fields.Char(string='Invoice Nr.', required=True)
    client_id = fields.Many2one(comodel_name='shop.client', string='Client', requirement=True)
    employee_id = fields.Many2one('shop.employee', string='Employee')
    total = fields.Float(string='Total', digits=(16, 2), compute='_compute_total', store=True)
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
    invoice_line_ids = fields.One2many('shop.invoice.line', 'invoice_id', string='Invoice lines')

    @api.depends('invoice_line_ids')
    def _compute_total(self):
        for rec in self:
            # total = 0
            # for line in rec.invoice_line_ids:
            #     total += line.total
            # rec.total = total
            rec.total = sum(rec.invoice_line_ids.mapped('total'))


class ShopInvoiceLine(models.Model):
    _name = 'shop.invoice.line'

    invoice_id = fields.Many2one(comodel_name='shop.invoice', string='Invoice', required=True)
    product_id = fields.Many2one('shop.product', string='Product')
    quantity = fields.Float(string='Quantity', digits=(16, 2))
    price = fields.Float(string='Price', digits=(16, 2))
    total = fields.Float(string='Total', digits=(16, 2), compute='_compute_total')

    @api.depends('price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity

    @api.onchange('product_id')
    def _product_id_onchange(self):
        self.price = self.product_id.selling_price
