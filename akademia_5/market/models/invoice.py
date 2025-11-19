# -*- coding: utf-8 -*-
from odoo import fields, models, api


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
    total = fields.Float(string='', digits=(16, 4), compute='_calc_total', store=True)
    invoice_line_ids = fields.One2many(comodel_name='market.invoice.line', inverse_name='invoice_id',
                                       string='Invoice Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', required=True)

    @api.depends('invoice_line_ids')
    def _calc_total(self):
        for rec in self:
            # s = 0
            # for line in rec.invoice_line_ids:
            #     s += line.total
            # self.total = s
            rec.total = sum(self.invoice_line_ids.mapped('total'))

    def confirm_invoice(self):
        self.state = 'done'
        if self.invoice_type == 'in':
            for invoice_line in self.invoice_line_ids:
                invoice_line.product_id.quantity += invoice_line.quantity
        else:
            for invoice_line in self.invoice_line_ids:
                invoice_line.product_id.quantity -= invoice_line.quantity

    def pay_invoice(self):
        self.state = 'paid'


class MarketInvoiceLine(models.Model):
    _name = 'market.invoice.line'

    product_id = fields.Many2one(comodel_name='market.product', string='Product')
    invoice_id = fields.Many2one(comodel_name='market.invoice', string='Invoice')
    quantity = fields.Float(string='Quantity', digits=(16, 4), default=1)
    price = fields.Float(string='Price', digits=(16, 2))
    total = fields.Float(string='Total', digits=(16, 2), compute='_calc_total')

    _sql_constraints = [
        ('quantity', 'CHECK(quantity>=0)', 'Quantity must be positive'),
    ]

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.invoice_id.invoice_type == 'in':
            self.price = self.product_id.purchase_price
        else:
            self.price = self.product_id.sell_price

    @api.depends('price', 'quantity')
    def _calc_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity
