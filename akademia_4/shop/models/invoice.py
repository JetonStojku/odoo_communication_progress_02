# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.api import ondelete
from odoo.exceptions import ValidationError, UserError


class ShopInvoice(models.Model):
    """ This model represents invoice."""
    _name = 'shop.invoice'

    invoice_nr = fields.Char(string='Invoice Nr.', required=True, default='New...')
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
    invoice_type = fields.Selection([('in', 'In'), ('out', 'Out')], string='Status', default='out', required=True)

    @api.depends('invoice_line_ids')
    def _compute_total(self):
        for rec in self:
            # total = 0
            # for line in rec.invoice_line_ids:
            #     total += line.total
            # rec.total = total
            rec.total = sum(rec.invoice_line_ids.mapped('total'))

    def done_status(self):
        self.state = 'done'
        if self.invoice_type == 'in':
            for line in self.invoice_line_ids:
                line.product_id.quantity += line.quantity
        else:
            for line in self.invoice_line_ids:
                line.product_id.quantity -= line.quantity
            self.paid_status()

    def paid_status(self):
        self.state = 'paid'
        if self.invoice_type == 'out':
            if self.payment_type == 'point':
                if self.client_id.point >= self.total:
                    self.client_id.point -= self.total
                else:
                    raise ValidationError("You don't have enough points")
            else:
                self.client_id.point += self.total / 100

    @api.model
    def create(self, values):
        if values['invoice_type'] == 'out':
            code = self.env['ir.sequence'].next_by_code('out.invoice.cp')
        else:
            code = self.env['ir.sequence'].next_by_code('in.invoice.cp')
        values['invoice_nr'] = code
        res = super(ShopInvoice, self).create(values)
        return res

    def write(self, values):
        test = self
        res = super(ShopInvoice, self).write(values)
        test = self
        return res

    def unlink(self):
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError('Invoice can not be deleted')
        res = super(ShopInvoice, self).unlink()
        return res


class ShopInvoiceLine(models.Model):
    _name = 'shop.invoice.line'

    invoice_id = fields.Many2one(comodel_name='shop.invoice', string='Invoice', required=True, ondelete='cascade')
    product_id = fields.Many2one('shop.product', string='Product')
    quantity = fields.Float(string='Quantity', digits=(16, 2), default=1)
    price = fields.Float(string='Price', digits=(16, 2))
    total = fields.Float(string='Total', digits=(16, 2), compute='_compute_total')

    @api.depends('price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity

    @api.onchange('product_id')
    def _product_id_onchange(self):
        if self.invoice_id.invoice_type == 'out':
            self.price = self.product_id.selling_price
        else:
            self.price = self.product_id.purchase_price
