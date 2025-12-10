# -*- coding: utf-8 -*-
from odoo import fields, models, api


class MarketInvoice(models.Model):
    _inherit = 'market.invoice'

    point = fields.Float(related='client_id.point', readonly=True)

    def apply_discount(self):
        # for line in self.invoice_line_ids:
        #     line.discount = '5'
        self.invoice_line_ids.write({'discount': '5'})


class MarketInvoiceLine(models.Model):
    _inherit = 'market.invoice.line'

    discount = fields.Selection([
        ('0', '0%'),
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%'),
        ('20', '20%'),
    ], string='Discount', required=True, default='0')
    total = fields.Float(string='Total', digits=(16, 2), compute='_compute_total')

    @api.depends('price', 'quantity', 'discount')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity * (1 - int(rec.discount) / 100)
